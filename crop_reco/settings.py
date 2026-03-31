from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this-in-production")

# Set to False on Render, True locally
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "smart-kissan.onrender.com",
    "smart-kissan-2jyj.onrender.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://smart-kissan.onrender.com",
    "https://smart-kissan-2jyj.onrender.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Required for allauth
    "django.contrib.sites",

    # allauth apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    "recommender",
]

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Skip intermediate confirmation page — go directly to Google
SOCIALACCOUNT_LOGIN_ON_GET = True

# NOTE: No APP key here — credentials are managed via Django Admin
# This avoids MultipleObjectsReturned conflict
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# After Google login → home page
LOGIN_REDIRECT_URL = "/home/"
# After logout → signup page
ACCOUNT_LOGOUT_REDIRECT_URL = "/signup/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Required for allauth
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "crop_reco.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "recommender.context_processors.nav_context",
            ],
        },
    },
]

WSGI_APPLICATION = "crop_reco.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", "English"),
    ("hi", "Hindi"),
    ("bn", "Bengali"),
    ("te", "Telugu"),
    ("mr", "Marathi"),
    ("ta", "Tamil"),
]

TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

SESSION_ENGINE = "django.contrib.sessions.backends.db"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")