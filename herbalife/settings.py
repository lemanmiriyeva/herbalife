from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-mfcdtx+_cx77me^zp@jzf^*awvl9!6q=^+oos)&rtr)2#f3zyg')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'jet',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'core.middleware.StoreMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'herbalife.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'herbalife.wsgi.application'

# ─── DATABASE (PostgreSQL) ───────────────────────────────────────────────────
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME':     os.environ.get('DB_NAME',     'herbalife_db'),
#         'USER':     os.environ.get('DB_USER',     'herbalife_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'herbalife_pass'),
#         'HOST':     os.environ.get('DB_HOST',     'db'),   # docker-compose service adı
#         'PORT':     os.environ.get('DB_PORT',     '5432'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to your database file
    }
}
# ─── LOCALISATION ────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'az'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('az', _('Azerbaijani')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ─── STATIC / MEDIA ──────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'   # collectstatic üçün
MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── AUTH / SESSION ──────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 604800  # 7 gün
AUTH_USER_MODEL = 'core.User'
USE_X_FORWARDED_HOST = True

# ─── MODELTRANSLATION ────────────────────────────────────────────────────────
MODELTRANSLATION_DEFAULT_LANGUAGE = 'az'

# ─── PAYPAL ──────────────────────────────────────────────────────────────────
PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')  # deploy-da 'live' et

PAYPAL_SANDBOX_CLIENT_ID = os.environ.get('PAYPAL_SANDBOX_CLIENT_ID', 'AcAtu5E_zcM9ZrkHm8Zkansh58qCuv2SNI5p1LWido9V3NGg06FyVU9dH85PMTnH2y0CbDHLEn4whRbS')
PAYPAL_SANDBOX_SECRET    = os.environ.get('PAYPAL_SANDBOX_SECRET',    'EPoKHuXrubI8a6rliN02DcipeIS5_8U0sgQR4Vvzyg6Z-Vn7wUKaf3b_q4cgmBG0nsjxa3FcFG_CZc2z')

PAYPAL_LIVE_CLIENT_ID = os.environ.get('PAYPAL_LIVE_CLIENT_ID', 'YOUR_LIVE_CLIENT_ID')
PAYPAL_LIVE_SECRET    = os.environ.get('PAYPAL_LIVE_SECRET',    'YOUR_LIVE_SECRET')

PAYPAL_AZN_TO_USD_RATE = float(os.environ.get('PAYPAL_AZN_TO_USD_RATE', '0.59'))