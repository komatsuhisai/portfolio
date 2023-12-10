from fastapi import FastAPI
from django.core.asgi import get_asgi_application
from streamlit_app.chat_router import router  # FastAPIルーターをインポート
from fastapi.middleware.cors import CORSMiddleware  # 例: CORSミドルウェアをインポート

app = FastAPI()

# CORSミドルウェアを追加
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event('startup')
async def startup():
    # FastAPIアプリケーションの初期化

@app.on_event('shutdown')
async def shutdown():
    # FastAPIアプリケーションのシャットダウン

@app.get("/")
async def read_root():
    return {"message": "Hello, World"}

# その他のFastAPIルートハンドラをここに追加

# FastAPIアプリケーションを別のASGIアプリケーションとして実行するために、FastAPIのappインスタンスを直接使用
