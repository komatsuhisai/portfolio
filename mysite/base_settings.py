#base_settings.py

from pathlib import Path
import os
import environ

DJANGO_PRODUCTION=False

env = environ.Env()

environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

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

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




# Email settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')

# # Other settings...

# DEBUG = env.bool('DEBUG')
# ALLOWED_HOSTS = ['localhost', '160.16.147.187', '127.0.0.1']
# OPENAI_API_KEY = env('OPENAI_API_KEY')




# PORT = 8000







# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ログイン成功後にリダイレクトするURL
LOGIN_REDIRECT_URL = 'index'

# ログアウト後にリダイレクトするURL (ここではログインページに戻す)
LOGOUT_REDIRECT_URL = 'login'

# ログインページのURL
LOGIN_URL = 'login'















script_path = os.path.abspath(os.path.dirname(__file__))
# BASE_DIR = os.path.dirname(os.path.dirname(script_path))





LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'myapp.log',
            'formatter': 'verbose',  # ここでフォーマッタを設定
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}







# # Database configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }



# # Static files (CSS, JavaScript, Images)
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!





# Application definition





# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': env.db(),
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# # 静的ファイルの設定
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]








# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field




# settings.py (Djangoプロジェクトの設定ファイル)


# settings.py






