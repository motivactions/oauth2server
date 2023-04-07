import base64
import hashlib
import random
import string
import logging
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse

from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from oauth2_provider.models import Application
from rest_framework_api_key.models import APIKey
from auths.generators import decode_jwt

User = get_user_model()

logger = logging.getLogger("django.request")

code_verifier = "".join(
    random.choice(string.ascii_uppercase + string.digits)
    for _ in range(random.randint(43, 128))
)
code_verifier = base64.urlsafe_b64encode(code_verifier.encode("utf-8"))
code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8").rstrip("=")

client_id = "ZWqE7FLFMHw3YWCiUoMTrNz6EOqaa64ltqKpu8Lg"
client_secret = "s1Xe0tJlJUjOM8bDhz7RCkarnO27P71LiRoGYatmBY13D8oXPIv5yBb9gDtFT8bVJIWd6TaNRowZpTZSWQYKvbYFIC6skn9UpdEPBE7TVNFxhLlQ4mCz7maKjFBVDfwN"  # NOQA


class TestCase(LiveServerTestCase):
    def setUp(self) -> None:
        self.previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        api_key_instance, api_key = APIKey.objects.create_key(name="test_api_key")
        self.api_key_instance = api_key_instance
        self.api_key = api_key
        self.user = User.objects.create_user(
            username="demo_user",
            password="demo_password",
            email="demo@gmail.com",
            first_name="Jhon",
            last_name="Doe",
            is_superuser=True,
        )
        self.application = Application(
            user=self.user,
            name="superapps",
            client_id=client_id,
            client_type=Application.CLIENT_CONFIDENTIAL,
            redirect_uris="http://127.0.0.1:8000/accounts/authentics/login/callback/",
            skip_authorization=True,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            client_secret=client_secret,
        )
        self.application.save()
        return super().setUp()

    def tearDown(self) -> None:
        logger.setLevel(self.previous_level)
        return super().tearDown()

    def test_authentication_and_authorization(self):
        # Get authorization token
        params = {
            "response_type": "code",
            "code_challenge": code_challenge,
            "code_verifier": code_verifier,
            "code_challenge_method": "S256",
            "client_id": self.application.client_id,
            "redirect_uri": self.application.default_redirect_uri,
        }
        path = "/api/oauth/authorize/"
        url = path + "?" + urlencode(params)
        self.client.force_login(user=self.user)
        resp = self.client.get(url)

        parsed_url = urlparse(resp.url)
        authorization_code = parse_qs(parsed_url.query).get("code")[0]

        # Get access token
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": authorization_code,
            "code_verifier": code_verifier.decode("utf-8"),
            "redirect_uri": self.application.default_redirect_uri,
            "grant_type": "authorization_code",
        }
        resp = self.client.post("/api/oauth/token/", data=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "access_token")

        # Access protected endpoint
        access_token = resp.json()["access_token"]
        refresh_token = resp.json()["refresh_token"]

        token_data = decode_jwt(access_token)
        self.assertIn("identity", token_data)
        self.assertIn("email", token_data["identity"])

        # Test expiration
        to_utc = datetime.utcfromtimestamp
        created_in = to_utc(token_data["iat"]).strftime("%Y-%m-%dT%H:%M:%SZ")
        expired_in = to_utc(token_data["exp"]).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.assertGreater(expired_in, created_in)

        headers = {
            "HTTP_X_API_KEY": self.api_key,
            "HTTP_AUTHORIZATION": f"Bearer {access_token}",
            "HTTP_CONTENT_TYPE": "application/json",
        }
        resp = self.client.get("/api/oauth/profile/", **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '"username":"demo_user"')

        resp = self.client.get("/api/oauth/profile/", **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '"username":"demo_user"')

        # Refresh the token
        # test get authorization token
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        resp = self.client.post("/api/oauth/token/", data=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "access_token")
        self.assertContains(resp, "refresh_token")

        new_access_token = resp.json()["access_token"]

        headers = {
            "HTTP_X_API_KEY": self.api_key,
            "HTTP_AUTHORIZATION": f"Bearer {new_access_token}",
            "HTTP_CONTENT_TYPE": "application/json",
        }
        resp = self.client.get("/api/oauth/profile/", **headers)
        self.assertEqual(resp.status_code, 200)

        # test revoke token
        resp = self.client.post(
            "/api/oauth/revoke_token/",
            data={
                "token": new_access_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
            headers=headers,
        )
        self.assertEqual(resp.status_code, 200)

        headers = {
            "HTTP_X_API_KEY": self.api_key,
            "HTTP_AUTHORIZATION": f"Bearer {new_access_token}",
            "HTTP_CONTENT_TYPE": "application/json",
        }
        resp = self.client.get("/api/oauth/profile/", **headers)
        self.assertEqual(resp.status_code, 401)
