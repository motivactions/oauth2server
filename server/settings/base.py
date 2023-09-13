import os
import sentry_sdk
from urllib.parse import urlparse
from sentry_sdk.integrations.django import DjangoIntegration
from .environ import BASE_DIR, PROJECT_DIR, env  # NOQA

PROJECT_NAME = env("PROJECT_NAME")

SITE_ID = 1
SITE_DOMAIN = env("SITE_DOMAIN")
BASE_URL = env("BASE_URL")
USE_TLS = env("USE_TLS")


INSTALLED_APPS = [
    # apps
    "boards",
    # "boards.themes.default",
    # "simpel",
    "auths",
    # REST
    "server.api",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    # other deps
    "mptt",
    "widget_tweaks",
    "easy_thumbnails",
    "import_export",
    "django_filters",
    "phonenumber_field",
    "django_celery_beat",
    "django_celery_results",
    # django
    # "django.contrib.gis",
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    # Authentication
    "oauth2_provider",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "django_cleanup",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
]

ROOT_URLCONF = "server.settings.urls"
WSGI_APPLICATION = "server.wsgi.application"

##############################################################################
# TEMPLATES
##############################################################################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
            # os.path.join(BASE_DIR, "dash", "oauth_dash", "dist"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


##############################################################################
# DATABASE
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
##############################################################################

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

##############################################################################
# AUTHENTICATIONS
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
##############################################################################

if USE_TLS:
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"  # or https
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_USERNAME_BLACKLIST = []
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_ADAPTER = "auths.adapter.AccountAdapter"
ACCOUNT_FORMS = {
    "login": "allauth.account.forms.LoginForm",
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "reset_password": "allauth.account.forms.ResetPasswordForm",
    "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    # "signup": "auths.forms.SignupForm",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
}

AUTH_USER_MODEL = "auths.User"
AUTH_VALIDATORS = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": AUTH_VALIDATORS + "UserAttributeSimilarityValidator"},
    {"NAME": AUTH_VALIDATORS + "MinimumLengthValidator"},
    {"NAME": AUTH_VALIDATORS + "CommonPasswordValidator"},
    {"NAME": AUTH_VALIDATORS + "NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "oauth2_provider.backends.OAuth2Backend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": env("GOOGLE_CLIENT_ID"),
            "secret": env("GOOGLE_CLIENT_SECRET"),
            "key": env("GOOGLE_API_KEY"),
        }
    },
    "facebook": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": env("FB_CLIENT_ID"),
            "secret": env("FB_CLIENT_SECRET"),
            "key": env("FB_CLIENT_KEY"),
        }
    },
}

JWT_JWS_ALGORITHMS = "RS256"

JWT_PRIVATE_KEY_ISSUER = """
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAmnOhxvP1rKOUu3Hb40qy131kkWosERrQmiVMBILnnxMDBcma
9w7oGlvezAK/4LEHMkRK5fmgQq6dZozbkdiVy06yUl0exTN2zipFxBEymWLN3oEf
OQ2TEE9UvJeOeKBR8FVWTwAlNZcpClc9jeIAz6Toy5YLU9sPGL7NwiYFcndC3+dp
xRTVD1rmkSVe0pb4s4i/p7s3/03dsbqmI6hPSIot3QG3rrVlODtcieKuA8/sO8WG
o4qIEn8+DRr6I/jBM+jWRhplqYZBdH1ad2w1DXyX6qHqG/tFrjudILlk/AB81k30
sL+6tpSSe2bTVd1c1JIJcGt1UBWfOpffSNT75wIDAQABAoIBAAeva0RYDUhq11LA
Zp2XsPByB9gIfWrYd7rD0lWDIf1TV9oo3vIeJsRw/9QM6vlGNcJ1jXiGBEhtId3h
cmd+bG2yW8MnaQmM9wNpLRGFfYwOU4oXyLLxDvlHyUKdE/TCnXEk/edubWuOOveN
wb1Wmo26ee7vZ17jzot/qwNXGvxICRuG31uvzKrnLmCPoFhDXxOptnzqAZQuk9XD
VRvGKNHcyFAMuYtxPEQbgIMsOlitRAsNgKwuQ6q6d5B9bNNdIIfKHp8BiRqei9Cf
fTe7IxX3x9K3KkkGHUWKKBqXsdh2E3S/FMfwG9BZihrw9i1MBNbdm1SVBj14nsEk
172gfgECgYEAy5MSg1WpVs9vFBJ0R8tjX4Npg7wN7OtjPYgPyvsN/Pgx/k1reEnl
fML3R8wKrZzUG6Bow7sGTdeqjJb+sDXU/UMFIEYGiu/amXaPPN7PF4GNzOh/A9BQ
gsxN7XaouTDwZtolDRTyuT/9aYC8Js2S5qJm2mh9xRqc2OKY0mF2POcCgYEAwjoS
JFSjSAbwgq1SlD/7XPkbiFV1/PO3wQdtPawTP7TwT9bJYqD2jf6+a1tDgrnBvoas
TpdFM3qkyHdeDMrlNNXpaNJMNhdaSt+ambFkm3VBeT9Kn1BEcq3Y1Q07G2m5gMOE
Pc3Q80vvcNnEulQmLrA12EUOC7SAXzVoaUP8aQECgYBCQm1tJ+2FHuElpFgKoi2H
AgvO39+cdIUJmwag55QG+XW0Mti+/zZdpEu+J7B2D6yODWjsBCyqG38cYW0mR286
u5yog4JPqH/7ITa/9jlrijRwNGBbCmuaFwtqNgv2svIcV/ZlSqMyHpzJwSf8bT7a
KJPXlNkS1XWltiNNnoFQkwKBgC5v3eiLx+Ivro8/y0+goIORF5EYBbatupBPK0Ik
gxGnPBGKo+mN3IUElBhs4I4/xV+9KTM9HZF6UC2RxI3AcN6aCk1CgnAoUzE1luwK
Kqi0dyv7AudmNIdKo14E5M3gEDcGB/cS31NcI2pS1qNJ/TsKbEVB9WK9DDg3N7h7
Rb0BAoGAd6ETlFRQQns5h7Ftjd+YR1Mj73/OUAjLWNKLzqokMUNAW7/hYPV7H2hA
flaK4n3SGB4DQjQDHdh7IKr7HJsCn9ZXY0jnQrbiRZjLrG1+1MA7pZMvpj+Pfu1p
/qvSS0Y1oj5W7USIB/qN1ArWbplub9UmRCJ8v4aU6RCKWaLlIuE=
-----END RSA PRIVATE KEY-----
"""

JWT_PUBLIC_KEY_ISSUER = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmnOhxvP1rKOUu3Hb40qy
131kkWosERrQmiVMBILnnxMDBcma9w7oGlvezAK/4LEHMkRK5fmgQq6dZozbkdiV
y06yUl0exTN2zipFxBEymWLN3oEfOQ2TEE9UvJeOeKBR8FVWTwAlNZcpClc9jeIA
z6Toy5YLU9sPGL7NwiYFcndC3+dpxRTVD1rmkSVe0pb4s4i/p7s3/03dsbqmI6hP
SIot3QG3rrVlODtcieKuA8/sO8WGo4qIEn8+DRr6I/jBM+jWRhplqYZBdH1ad2w1
DXyX6qHqG/tFrjudILlk/AB81k30sL+6tpSSe2bTVd1c1JIJcGt1UBWfOpffSNT7
5wIDAQAB
-----END PUBLIC KEY-----
"""

OAUTH2_PROVIDER_APPLICATION_MODEL = "auths.Application"

OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_GENERATOR": "auths.generators.access_token_generator",
    "ACCESS_TOKEN_EXPIRE_SECONDS": 600,
    "REFRESH_TOKEN_GENERATOR": "auths.generators.refresh_token_generator",
    "REFRESH_TOKEN_EXPIRE_SECONDS": 600,
}

##############################################################################
# INTERNATIONALIZATION
# https://docs.djangoproject.com/en/4.0/topics/i18n/
##############################################################################

LANGUAGE_CODE = "id"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

##############################################################################
# STATICFILE & STORAGE
##############################################################################

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
    # os.path.join(BASE_DIR, "dash", "oauth_dash")
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
MEDIA_URL = "/media/"

##############################################################################
# SESSION & CACHE
##############################################################################

REDIS_URL = env("REDIS_URL")

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60 * 24  # Logout if inactive for 15 minutes
SESSION_SAVE_EVERY_REQUEST = True

if REDIS_URL:
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
    SESSION_CACHE_ALIAS = "default"
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        },
    }

##############################################################################
# QUEUES
##############################################################################

REDIS_SSL = env("REDIS_SSL", bool, False)
RQ_DATABASE = 1
RQ_URL = urlparse(REDIS_URL)

RQ_QUEUES = {
    "default": {
        "HOST": RQ_URL.hostname,
        "USERNAME": RQ_URL.username,
        "PASSWORD": RQ_URL.password,
        "PORT": RQ_URL.port,
        "DB": RQ_DATABASE,
        "SSL": bool(REDIS_SSL),
        "SSL_CERT_REQS": None,
    },
}


# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"

# This configures Redis as the datastore between Django + Celery
CELERY_BROKER_URL = env("CELERY_BROKER_REDIS_URL")
# if you out to use os.environ the config is:
# CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_REDIS_URL', 'redis://localhost:6379')

CELERY_RESULT_EXTENDED = True

# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"


##############################################################################
# LOGGING
##############################################################################

if env("SENTRY_DSN") not in ["", None]:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        environment=env("SENTRY_ENV"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
    )

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "django.request": {
        "handlers": ["console"],
        "level": "ERROR",
        "propagate": True,
    },
}
