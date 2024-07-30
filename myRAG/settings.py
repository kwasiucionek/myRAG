from pathlib import Path
import environ
import os

# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / '.env')

# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Parse database connection url strings
# like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    'default': env.db(),
}

# E-mail settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'user@gmail.com'
EMAIL_HOST_PASSWORD = 'tour passwd'
DEFAULT_FROM_EMAIL = 'kwasiek@gmail.com'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

#CSRF_TRUSTED_ORIGINS = ['http://example.com']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'documents.apps.DocumentsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.mfa',
    'pgvector',
    'rest_framework',
    'django_celery_results',
    'django_celery_beat',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'myRAG.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
            ],
        },
    },
]

WSGI_APPLICATION = 'myRAG.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Konfiguracje konta
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# URL do przekierowania po zalogowaniu
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': 'XXX',
            'secret': 'YOU SECRET',
            'key': ''
        }
    }
}

# Konfiguracja MFA
MFA_ENABLED = True
ACCOUNT_MFA_ENABLED = True
ACCOUNT_MFA_MODEL = 'allauth.mfa.models.TOTPDevice'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_REQUIRED = True

MFA_SUPPORTED_TYPES = ['totp', 'recovery_codes']

ACCOUNT_RATE_LIMITS = {
    'login': '5/m',  # Pozwól na 5 prób logowania na minutę
    'login_failed': '5/m',  # Pozwól na 5 nieudanych prób logowania na minutę
    'signup': '10/h',  # Pozwól na 10 rejestracji na godzinę
    'password_reset': '5/h',  # Pozwól na 5 resetów hasła na godzinę
    'mfa': {
        'authenticate': '10/m',  # Pozwól na 10 prób MFA na minutę
    },
    'email_verification': '5/m'  # Pozwól na 5 prób weryfikacji email na minutę
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Ścieżka do katalogu, w którym będą zapisywane przesyłane pliki
MEDIA_ROOT = BASE_DIR / 'docs'
MEDIA_URL = '/docs/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OPENAI_API_KEY = env('OPENAI_API_KEY')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "myRAG",
    "site_header": "myRAG",
    "site_brand": "myRAG",
    "site_logo": "logo.png",
    "site_logo_classes": "img-circle",
    #"dark_mode_theme": "darkly",  # Example theme
    "welcome_sign": "Witaj w myRAG",
    "copyright": "Krzysztof Wasiucionek",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    ],
    "order_with_respect_to": ["auth", "documents"],
    "custom_links": {
        "documents": [
            {
                "name": "Lista dokumentów",
                "url": "documents:document_list",
                "icon": "fas fa-file-alt",
            },
            {
                "name": "Porozmawiaj z myRAG",
                "url": "documents:search",
                "icon": "fas fa-search",
            },
            {
                "name": "Dodaj dokument",
                "url": "documents:upload_document",
                "icon": "fas fa-upload",
            }
        ]
    },
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "documents": "fas fa-book",  # Ikona dla aplikacji documents
        "documents.document": "fas fa-file-alt",
    },
    #"hide_models": ["documents.document", "documents.documentvector"],  # Ukryj modele dla wszystkich użytkowników
    # "hide_apps": ["documents"],  # Ukryj aplikację documents dla wszystkich użytkowników
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,
    "language_chooser": False,
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myRAG'
    }
}

CACHE_TTL = 60 * 15  # Cache timeout in seconds (15 minutes)

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Warsaw'
