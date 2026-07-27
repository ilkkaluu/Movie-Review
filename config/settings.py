from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

# A05 Security Misconfiguration demo:
# To make the fix active, comment this line and uncomment the secure host configuration below.
ALLOWED_HOSTS = ["*"]

# Fix for A05 Security Misconfiguration:
#ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if os.environ.get("DJANGO_ALLOWED_HOSTS") else []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# A09 Security Logging and Monitoring Failures demo:
# Exact source: this settings module does not define application security
# logging or audit trails for authentication, authorization, or other sensitive
# actions.
#
# Switching between flawed and fixed demo modes:
# - Flawed mode: keep SECURITY_EVENT_LOGGING_ENABLED = False.
# - Fixed mode: set SECURITY_EVENT_LOGGING_ENABLED = True.

SECURITY_EVENT_LOGGING_ENABLED = True

# Fix for A09 Security Logging and Monitoring Failures:
#LOGGING = {
#	"version": 1,
#	"disable_existing_loggers": False,
#	"handlers": {
#		"console": {
#			"class": "logging.StreamHandler",
#		},
#	},
#	"loggers": {
#		"pages.security": {
#			"handlers": ["console"],
#			"level": "INFO",
#			"propagate": False,
#		},
#	},
#}
