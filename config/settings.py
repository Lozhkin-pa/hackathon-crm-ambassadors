import os
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

# ---------------------------------------------------------LOAD ENVIRONMENT VAR
SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-pp6rfj83429fhjndu89v2702fhkuj902d2@65!+=$satw167",
)
USE_POSTGRESQL = env.bool("USE_POSTGRESQL", default=False)
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
        "[::1]",
        "testserver"
    ],
)
DB_NAME = env.str("DB_NAME", default="DB_NAME")
DB_USER = env.str("POSTGRES_USER", default="username")
DB_PASSWORD = env.str("POSTGRES_PASSWORD", default="smart-password123")
DB_HOST = env.str("DB_HOST", default="db")
DB_PORT = env.int("DB_PORT", default=5432)

# CORS_ALLOWED_ORIGINS = env.list(
#     "CORS_ALLOWED_ORIGINS",
#     default=["http://localhost:8000", "http://127.0.0.1:8000", "http://5.35.89.44:8000", "http://5.35.89.44:3000"],
# )
# CSRF_TRUSTED_ORIGINS = CORS_ORIGINS_WHITELIST = CORS_ALLOWED_ORIGINS
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ['https://crm-ambassadors.hopto.org']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="ru-RU")
TIME_ZONE = env.str("TIME_ZONE", default="Europe/Moscow")
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "django_filters",
    "drf_spectacular",
    "corsheaders",
    "notifications",
]
LOCAL_APPS = [
    "api.v1.apps.ApiConfig",
    "ambassadors.apps.AmbassadorsConfig",
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "merch.apps.MerchConfig",
    "content.apps.ContentConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


if USE_POSTGRESQL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

USE_I18N = True

USE_TZ = True

# STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "users.ExtendedUser"
# -----------------------------------------------------------------DRF SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 8,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
if DEBUG:
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
# --------------------------------------------------------------DJOSER SETTINGS
DJOSER = {
    "SERIALIZERS": {
        "current_user": "api.v1.serializers.users_serializer.CustomUserSerializer",
    },
    "LOGIN_FIELD": "email",
}
# ---------------------------------------------------------SPECTACULAR_SETTINGS
SPECTACULAR_SETTINGS = {
    "TITLE": "CRM API",
    "DESCRIPTION": (
        'API-Документация для SPA "CRM Амбассадоры".<br>'
        'Хакатон "CRM Амбассадоры" Яндекс-Практикум 2024г. Команда № 1.'
    ),
    "VERSION": "0.1.0",
    "SCHEMA_PATH_PREFIX": "/api/v1/",
    "SERVE_INCLUDE_SCHEMA": False,
}
# --------------------------------------------------------------------CONSTANTS
NAME_LENGTH = 250
STATUS_LENGTH = 50
