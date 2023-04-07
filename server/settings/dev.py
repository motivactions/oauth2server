import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # NOQA
from .base import env
from .restapi import *  # NOQA
from .restapi import REST_FRAMEWORK

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "https://oauth2.dev-tunnel.mitija.com",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]
MIDDLEWARE += [  # NOQA
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += [  # NOQA
    "debug_toolbar",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
    "rest_framework_api_key.permissions.HasAPIKey",
    "rest_framework.authentication.BasicAuthentication",
    "rest_framework.authentication.SessionAuthentication",
]

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    environment="development",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
