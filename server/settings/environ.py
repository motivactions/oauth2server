##############################################################################
# ENVIRONMENT VARIABLES
# List all enviroment variables used in this project.
# This list should be maintained manually.
##############################################################################
import os

import environ

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

env = environ.Env(
    DEBUG=(bool, False),
    USE_TLS=(bool, False),
    SECRET_KEY=(str, "***"),
    SITE_ID=(int, 1),
    SITE_NAME=(str, "example"),
    SITE_DOMAIN=(str, "127.0.0.1:8000"),
    PROJECT_NAME=(str, "Authentics"),
    BASE_URL=(str, "http://127.0.0.1:8000"),
    # CSRF and CORS
    ALLOW_WILD_CARD=(bool, True),
    CSRF_TRUSTED_ORIGINS=(list, ["http://127.0.0.1:8000"]),
    CORS_ALLOW_ALL_ORIGINS=(bool, 0),
    CORS_ALLOW_CREDENTIALS=(bool, 0),
    CORS_ALLOWED_ORIGINS=(list, []),
    CORS_ALLOWED_ORIGIN_REGEXES=(list, []),
    # Database & Redis
    POSTGRES_HOST=(str, "127.0.0.1"),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, "postgres"),
    POSTGRES_USER=(str, "postgres"),
    POSTGRES_PASSWORD=(str, "postgres"),
    REDIS_PASSWORD=(str, ""),
    REDIS_URL=(str, "redis://127.0.0.1:6379/0"),
    # Mail Server
    EMAIL_SUBJECT_PREFIX=(str, ""),
    SMTP_SENDER=(str, ""),
    SMTP_PASSWORD=(str, ""),
    SMTP_USERNAME=(str, ""),
    SMTP_PORT=(str, ""),
    SMTP_HOST=(str, ""),
    EMAIL_USE_TLS=(bool, True),
    # Static Files and Storage
    STORAGE_TYPE=(str, "whitenoise"),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_S3_ENDPOINT_URL=(str, ""),
    AWS_STORAGE_BUCKET_NAME=(str, ""),
    AWS_S3_URL_PROTOCOL=(str, "https:"),
    AWS_S3_CUSTOM_DOMAIN=(str, ""),
    # Logger
    SENTRY_ENV=(str, "local"),
    SENTRY_DSN=(str, ""),
    # Celery
    CELERY_BROKER_REDIS_URL=(str, "redis://127.0.0.1:6379/1"),
    # Allauth API Key
    GOOGLE_API_KEY=(str, ""),
    GOOGLE_CLIENT_ID=(str, ""),
    GOOGLE_CLIENT_SECRET=(str, ""),
    FB_CLIENT_ID=(str, ""),
    FB_CLIENT_SECRET=(str, ""),
    FB_CLIENT_KEY=(str, ""),
)
