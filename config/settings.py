"""
Django settings for config project.

MaterialSync
Smart India Hackathon deployment configuration
"""

from pathlib import Path
import os


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SECURITY
# =========================================================

# Production SECRET_KEY should come from Render environment
# variables. The fallback exists only so local development
# continues to work.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "dev-only-materialsync-secret-key-change-me",
)


# Render will set:
# DJANGO_DEBUG=False
#
# Local development remains DEBUG=True unless the environment
# variable is changed.

DEBUG = (
    os.environ.get(
        "DJANGO_DEBUG",
        "True",
    ).lower()
    == "true"
)


# Render hostname can be supplied through ALLOWED_HOSTS.
#
# Example:
# ALLOWED_HOSTS=material-sync-sih.onrender.com
#
# Comma-separated hostnames are supported.

ALLOWED_HOSTS = ["material-sy.onrender.com"]

# =========================================================
# APPLICATIONS
# =========================================================

INSTALLED_APPS = [

    "django.contrib.admin",

    "django.contrib.auth",

    "django.contrib.contenttypes",

    "django.contrib.sessions",

    "django.contrib.messages",

    "django.contrib.staticfiles",

    "rest_framework",

    "materials",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================================================
# URL / WSGI
# =========================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [

    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS":
            [],

        "APP_DIRS":
            True,

        "OPTIONS":
            {
                "context_processors":
                    [

                        "django.template.context_processors.request",

                        "django.contrib.auth.context_processors.auth",

                        "django.contrib.messages.context_processors.messages",

                    ],
            },
    },
]


# =========================================================
# DATABASE
# =========================================================

DATABASES = {

    "default":
        {
            "ENGINE":
                "django.db.backends.sqlite3",

            "NAME":
                BASE_DIR / "db.sqlite3",
        }

}


# =========================================================
# PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME":
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },

]


# =========================================================
# INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# =========================================================
# STATIC FILES
# =========================================================

STATIC_URL = "/static/"

# collectstatic will place production files here.

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================================================
# DEFAULT PRIMARY KEY
# =========================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# =========================================================
# EMAIL
# =========================================================

MAILERS = {

    "default":
        {
            "BACKEND":
                "django.core.mail.backends.console.EmailBackend",
        }

}


# =========================================================
# PRODUCTION SECURITY HEADERS
# =========================================================

# Only enable these when DEBUG=False / production.

if not DEBUG:

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"

    SECURE_REFERRER_POLICY = (
        "strict-origin-when-cross-origin"
    )

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True