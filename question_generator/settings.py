import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'channels',
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'question_generator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'question_generator.wsgi.application'
ASGI_APPLICATION = 'question_generator.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


# In question_generator/settings.py
CELERY_BROKER_URL = 'redis://localhost:6380/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6380/0'

# Channel Layers (if using)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6380)],
        },
    },
}

# # Celery Configuration
# CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
# CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# # Channels
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [config('REDIS_URL', default='redis://localhost:6379/0')],
#         },
#     },
# }

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# LLM API Keys
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
ANTHROPIC_API_KEY = config('ANTHROPIC_API_KEY', default='')
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')

# Change Redis URLs to use port 6380
CELERY_BROKER_URL = 'redis://localhost:6380/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6380/0'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Additional language support
LANGUAGES = [
    ('en', 'English'),
    ('hi', 'Hindi (हिंदी)'),
    ('te', 'Telugu (తెలుగు)'),
    ('ur', 'Urdu (اردو)'),
    ('ar', 'Arabic (العربية)'),
    ('es', 'Spanish (Español)'),
    ('fr', 'French (Français)'),
    ('de', 'German (Deutsch)'),
    ('zh', 'Chinese (中文)'),
    ('ja', 'Japanese (日本語)'),
    ('ko', 'Korean (한국어)'),
    ('ru', 'Russian (Русский)'),
    ('pt', 'Portuguese (Português)'),
    ('it', 'Italian (Italiano)'),
    ('nl', 'Dutch (Nederlands)'),
    ('sv', 'Swedish (Svenska)'),
    ('da', 'Danish (Dansk)'),
    ('no', 'Norwegian (Norsk)'),
    ('fi', 'Finnish (Suomi)'),
    ('pl', 'Polish (Polski)'),
    ('tr', 'Turkish (Türkçe)'),
    ('th', 'Thai (ไทย)'),
    ('vi', 'Vietnamese (Tiếng Việt)'),
    ('id', 'Indonesian (Bahasa Indonesia)'),
    ('ms', 'Malay (Bahasa Melayu)'),
    ('bn', 'Bengali (বাংলা)'),
    ('ta', 'Tamil (தமிழ்)'),
    ('ml', 'Malayalam (മലയാളം)'),
    ('kn', 'Kannada (ಕನ್ನಡ)'),
    ('gu', 'Gujarati (ગુજરાતી)'),
    ('mr', 'Marathi (मराठी)'),
    ('pa', 'Punjabi (ਪੰਜਾਬੀ)'),
    ('or', 'Odia (ଓଡ଼ିଆ)'),
    ('as', 'Assamese (অসমীয়া)'),
]

# Locale paths
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Font support for different scripts
FONT_PATHS = {
    'devanagari': 'fonts/NotoSansDevanagari-Regular.ttf',  # Hindi, Marathi, etc.
    'telugu': 'fonts/NotoSansTelugu-Regular.ttf',
    'arabic': 'fonts/NotoSansArabic-Regular.ttf',  # Arabic, Urdu
    'chinese': 'fonts/NotoSansCJK-Regular.ttf',
    'default': 'fonts/NotoSans-Regular.ttf'
}

# Math rendering settings
MATH_RENDERER = 'mathjax'  # or 'katex'
MATH_DELIMITERS = {
    'inline': ['$', '$'],
    'display': ['$$', '$$'],
    'block': ['\\[', '\\]']
}