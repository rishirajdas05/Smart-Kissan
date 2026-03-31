from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-this-in-production")

# Temporarily TRUE on Render to see the actual 500 error
# Change back to: DEBUG = 'RENDER' not in os.environ  after fixing
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "smart-kissan.onrender.com",
    "smart-kissan-2jyj.onrender.com",
    "*",  # allow all temporarily to debug
]

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    "https://smart-kissan.onrender.com",
    "https://smart-kissan-2jyj.onrender.com",
]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
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

SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

LOGIN_REDIRECT_URL          = "/home/"
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

TIME_ZONE    = "Asia/Kolkata"
USE_I18N     = True
USE_TZ       = True
LOCALE_PATHS = [BASE_DIR / "locale"]

SESSION_ENGINE = "django.contrib.sessions.backends.db"

STATIC_URL  = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Security headers — disabled while debugging
# Restore after fixing 500 error:
# if not DEBUG:
#     SECURE_PROXY_SSL_HEADER     = ("HTTP_X_FORWARDED_PROTO", "https")
#     SECURE_SSL_REDIRECT         = True
#     SESSION_COOKIE_SECURE       = True
#     CSRF_COOKIE_SECURE          = True
#     SECURE_BROWSER_XSS_FILTER   = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
#     X_FRAME_OPTIONS             = "DENY"