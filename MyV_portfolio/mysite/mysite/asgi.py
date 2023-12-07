import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import sys
from pathlib import Path
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from streamlit_app.chat_router import get_router

# 現在のファイル（asgi.py）のディレクトリを取得
current_directory = Path(__file__).resolve().parent

# chat_router.py のディレクトリを取得
router_directory = current_directory / 'streamlit_app'  # ディレクトリ名のみを指定

# sys.path に chat_router.py のディレクトリを追加
sys.path.append(str(router_directory))

# ルーターを取得
router = get_router()

# FastAPIアプリケーションを作成
app = FastAPI()

# ルーターをFastAPIアプリケーションにマウント
app.include_router(router, prefix="/fastapi")

# Django ASGIアプリケーションを取得
django_application = get_asgi_application()

# Django ASGIアプリケーションをマウント
app.mount("/django", django_application)

# Django ASGIアプリケーションをFastAPI ASGIアプリケーションとして使用
application = app
