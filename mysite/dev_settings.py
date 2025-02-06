#dev_settings.py

from .base_settings import *

# 開発固有の設定
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '160.16.147.187']

from .base_settings import *


# 開発用データベース設定（SQLiteを使う場合）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'myapp/static')]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'  # 静的ファイルを収集するディレクトリ
# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STRIPE_PUBLISHABLE_KEY='pk_test_51OeWWfIfdFWutwbXrPE0cvcK0fvDbjwLM51hyAqGGBC10ixuKNtHfhDeuA7lGSrnaLZFYoios1fWSVrEw3zZ8uav00IZc3hNh3'
STRIPE_API_KEY='sk_test_51OeWWfIfdFWutwbX7Fwzx9Efx9OI60xgAk2jBm0a5XnU2yA8n8IzFoL3YAGGDjW2mK1iZF6N8gOm64OA61sTRKcv00YxmbZthc'
STRIPE_ENDPOINT_SECRET='whsec_UGFJJHMjYyyRSkJxrrjYkIYE6pfw4cFe'
MINI_PLAN_PRICE_ID = os.environ.get('price_1OiWjvIfdFWutwbXKyPDmEVP')
STANDARD_PLAN_PRICE_ID = os.environ.get('STANDARD_PLAN_PRICE_ID')
DIRECTOR_PLAN_PRICE_ID = os.environ.get('DIRECTOR_PLAN_PRICE_ID')

# # Database configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# その他開発固有の設定

