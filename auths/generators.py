import jwt
import base64
import json
from django.conf import settings
from datetime import datetime, timedelta
from oauth2_provider.models import get_application_model
from oauth2_provider.settings import oauth2_settings
from django.core.exceptions import ImproperlyConfigured

Application = get_application_model()
TOKEN_EXPIRE_SECONDS = oauth2_settings.REFRESH_TOKEN_EXPIRE_SECONDS


def generate_payload(issuer, user=None, token="access_token"):
    """
    :param issuer: identifies the principal that issued the token.
    :type issuer: str
    :param expires_in: number of seconds that the token will be valid.
    :type expires_in: int
    :rtype: dict
    """
    now = datetime.utcnow()
    issued_at = now
    expiration = now + timedelta(seconds=TOKEN_EXPIRE_SECONDS)
    payload = {
        "iss": issuer,
        "exp": expiration,
        "iat": issued_at,
        "token": token,
    }

    if user is not None and user.is_authenticated:
        payload.update(
            {
                "sub": user.pk,
                "identity": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            }
        )
    return payload


def encode_jwt(payload, headers=None):
    """
    :type payload: dict
    :type headers: dict, None
    :rtype: str
    """
    # RS256 in default, because hardcoded legacy
    algorithm = getattr(settings, "JWT_ENC_ALGORITHM", "RS256")
    private_key_name = "JWT_PRIVATE_KEY_{}".format(payload["iss"].upper())
    private_key = getattr(settings, private_key_name, None)
    if not private_key:
        raise ImproperlyConfigured("Missing setting {}".format(private_key_name))
    decoded = jwt.encode(payload, private_key, algorithm=algorithm, headers=headers)
    return decoded


def decode_jwt(jwt_value):
    """
    :type jwt_value: str
    """
    try:
        headers_enc, payload_enc, verify_signature = jwt_value.split(".")
    except ValueError:
        raise jwt.InvalidTokenError()

    payload_enc += "=" * (-len(payload_enc) % 4)  # add padding
    payload = json.loads(base64.b64decode(payload_enc).decode("utf-8"))

    algorithms = getattr(settings, "JWT_JWS_ALGORITHMS", ["HS256", "RS256"])
    public_key_name = "JWT_PUBLIC_KEY_{}".format(payload["iss"].upper())
    public_key = getattr(settings, public_key_name, None)
    if not public_key:
        raise ImproperlyConfigured("Missing setting {}".format(public_key_name))

    decoded = jwt.decode(jwt_value, public_key, algorithms=algorithms)
    return decoded


def access_token_generator(request, refresh_token=False):
    """
    Create a new access token for the given user and application using JWT.
    """
    user = request.user
    token_payload = generate_payload("issuer", user=user, token="access_token")
    token = encode_jwt(token_payload)
    return token


def refresh_token_generator(request):
    """
    Create a new refresh token for the given user and application using JWT.
    """
    user = request.user
    token_payload = generate_payload("issuer", user=user, token="refresh_token")
    token = encode_jwt(token_payload)
    return token
