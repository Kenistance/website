"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta # ADDED: Import timedelta for JWT settings

load_dotenv()   # Load variables from .env file if present

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-default-key')   # default is fallback, replace in prod

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'website3-ho1y.onrender.com,localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt', # ADDED: simplejwt for JWT authentication

    # apps
    'portfolio',
    'enquiry',
    'chat',
    'project_requests',
    'payments',
    'users',
    'blog',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # Must be high in the order
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # ADDED: This line allows for project-wide templates
        'APP_DIRS': True, # Ensures app-specific templates (like users/templates/email) are found
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CRITICAL: Set the custom user model - THIS WAS MISSING!
AUTH_USER_MODEL = 'users.CustomUser'


# CORS settings - allow your React dev server origin here
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://website-git-main-kenistances-projects.vercel.app",
    "https://website-bv36edoeb-kenistances-projects.vercel.app",
    "https://website3-ho1y.onrender.com",
# Change if React runs on different port or add more URLs
]
CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "https://website-git-main-kenistances-projects.vercel.app",
    "https://website-bv36edoeb-kenistances-projects.vercel.app",
    "https://website3-ho1y.onrender.com",
]


# Email settings for enquiry notifications and password reset (UPDATED)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com') # Use environment variable, fallback to gmail
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587)) # Use environment variable, fallback to 587
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True' # Use environment variable, fallback to True
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True' # Add SSL option, fallback to False

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ADDED: Frontend URL for password reset link
FRONTEND_PASSWORD_RESET_URL = os.getenv('FRONTEND_PASSWORD_RESET_URL', 'http://localhost:5173/reset-password')


# Payment Settings
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'your_stripe_secret_key')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'your_stripe_publishable_key')

# M-Pesa Settings
MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT', 'sandbox')   # 'sandbox' or 'production'
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY', 'Vq1GjoIdaLKAZfyWhov8HL8IAjNCwfNCqGBXczvnvTDM8Wxm') # Using getenv
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET', 'UyYovjELndltcaQt4NfRJglZAv9aEXJUGzezOir6kUJ11qOCINPlWHerN7gOgYpP') # Using getenv
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')   # Your business shortcode
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')   # Sandbox passkey
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL', 'https://website3-ho1y.onrender.com/api/payments/mpesa-callback/') # Using getenv

# M-Pesa API URLs
if MPESA_ENVIRONMENT == 'sandbox':
    MPESA_BASE_URL = 'https://sandbox.safaricom.co.ke'
else:
    MPESA_BASE_URL = 'https://api.safaricom.co.ke'

MPESA_ACCESS_TOKEN_URL = f'{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials'
MPESA_STK_PUSH_URL = f'{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest'

MEDIA_ROOT = BASE_DIR / 'media'   # if not set already

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication', # ADDED: JWT Authentication
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# ADDED: Simple JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Access token valid for 60 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),   # Refresh token valid for 1 day
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',), # This is crucial: expect 'Bearer' in header
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# Logging Configuration for debugging payments
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'payments.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'payments': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory if it doesn't exist
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

MEDIA_URL = '/media/'

