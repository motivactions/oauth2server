import jwt
import base64
import json
from django.conf import settings
from datetime import datetime, timedelta
from oauth2_provider.models import get_application_model
from oauth2_provider.settings import oauth2_settings
from django.core.exceptions import ImproperlyConfigured

Application = get_application_model()


def generate_payload(issuer, expires_in, **extra_data):
    """
    :param issuer: identifies the principal that issued the token.
    :type issuer: str
    :param expires_in: number of seconds that the token will be valid.
    :type expires_in: int
    :param extra_data: extra data to be added to the payload.
    :type extra_data: dict
    :rtype: dict
    """
    now = datetime.utcnow()
    issued_at = now
    expiration = now + expires_in
    payload = {
        "iss": issuer,
        "exp": expiration,
        "iat": issued_at,
    }

    if extra_data:
        payload.update(**extra_data)

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
    token_expiration = timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

    # Generate access token
    payload = {
        "scope": "read write",
        "token": "access_token",
        "token_type": "Bearer",
    }
    if request.user is not None:
        payload.update({
            "sub": request.user.pk,
            "identity": {
                "username": request.user.username,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "tags": [t.slug for t in request.user.tags.all()],
            },
        })
    access_token_payload = generate_payload("issuer", token_expiration, **payload)
    access_token = encode_jwt(access_token_payload)

    return access_token


def refresh_token_generator(request):
    """
    Create a new refresh token for the given user and application using JWT.
    """
    token_expiration = timedelta(seconds=oauth2_settings.REFRESH_TOKEN_EXPIRE_SECONDS)

    # Generate access token
    payload = {
        "sub": request.user.pk,
        "scope": "read write",
        "token": "refresh_token",
        "token_type": "Bearer",
        "identity": {
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "tags": [t.slug for t in request.user.tags.all()],
        },
    }
    refresh_token_payload = generate_payload("issuer", token_expiration, **payload)
    refresh_token = encode_jwt(refresh_token_payload)

    return refresh_token
