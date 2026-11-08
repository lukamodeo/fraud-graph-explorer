# src/fraud_graph_explorer/config/settings.py

# Fraud Graph Explorer
# Copyright (C) 2026 Luca Amodeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import mimetypes
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# This points to: fraud-graph-explorer/src/fraud_graph_explorer/
# (Standard Django BASE_DIR, useful for finding things INSIDE the package)
BASE_DIR = Path(__file__).resolve().parent.parent

# This points to: fraud-graph-explorer/
# (The true project root, useful for finding things OUTSIDE the package, like media/ or pyproject.toml)
PROJECT_ROOT = BASE_DIR.parent.parent

# Media files (PDFs)
MEDIA_URL = '/media/'
# Safely join the project root to the 'media' folder name
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# Load .env file from project root
load_dotenv(PROJECT_ROOT / '.env')

# Read SECRET_KEY from environment (with a clear error if missing)
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY: raise ValueError( f"SECRET_KEY is not set. Add 'SECRET_KEY=...' to your .env file at {PROJECT_ROOT / '.env'}" )

# Enable translation system (required for get_language() to work)
USE_I18N = True
USE_L10N = True

# Default language if browser doesn't match
LANGUAGE_CODE = 'en-gb'

# Supported languages (which browser languages to accept)
LANGUAGES = [
    ('it', 'Italian'),
    ('de', 'German'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('en-gb', 'British English'),
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'fraud_graph_explorer.sheet_crafter',
    'fraud_graph_explorer.graph_explorer',
    'axes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',    # <== after Session, before Common !!!
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware', # <== should be LAST, after session/auth middleware
]


ROOT_URLCONF = 'fraud_graph_explorer.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Point Django to the new centralized templates folder
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'fraud_graph_explorer.config.context_processors.lockout_translations',
            ],
        },
    },
]

WSGI_APPLICATION = 'fraud_graph_explorer.config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DB_ENGINE = os.environ.get('DB_ENGINE', '')

if DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'fraud_graph'),
            'USER': os.environ.get('DB_USER', 'fraud_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
elif DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'fraud_graph'),
            'USER': os.environ.get('DB_USER', 'fraud_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'  # Changed to en-gb to match UI dictionary fallback

# Which languages we support
LANGUAGES = [
    ('it', 'Italian'),
    ('de', 'German'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('en-gb', 'British English'),
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Where collectstatic copies files to (production only)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Tell Django that .ttf files are font files, not generic binary files
mimetypes.add_type("font/ttf", ".ttf", True)
mimetypes.add_type("font/woff", ".woff", True)
mimetypes.add_type("font/woff2", ".woff2", True)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─── Authentication backends ───
# AxesStandaloneBackend goes FIRST so it runs before the real auth check.
# If the IP is locked, it returns None (login fails) without even
# checking the password — so brute-force attempts can't progress.
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ─── Authentication settings ───
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/explorer/'
LOGOUT_REDIRECT_URL = '/login/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

_allowed_hosts_raw = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(',') if h.strip()]

# Security settings for production
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# ─── django-axes configuration ───
AXES_ENABLED = os.environ.get('AXES_ENABLED', str(not DEBUG) ).lower() in ('true', '1')     # enable in production, disable in dev
IPWARE_PROXY_COUNT = int(os.environ.get('IPWARE_PROXY_COUNT', 0))                           # 1 reverse proxy (Nginx) in front of Django
AXES_FAILURE_LIMIT = 5                                                                      # 5 failed attempts => lockout
AXES_COOLOFF_TIME = timedelta(hours=1)                                                      # locked for 1 hour (user's request)
AXES_LOCKOUT_PARAMETERS = ["ip_address"]                                                    # lock by IP only (not IP+username)
AXES_RESET_ON_SUCCESS = True                                                                # reset counter on successful login
AXES_LOCKOUT_TEMPLATE = "registration/lockout.html"                                         # custom lockout page (optional, see below)