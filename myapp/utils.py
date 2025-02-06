# utils.py

import httpx
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError






# app.pyのTTSストリーミングに使用される非同期GETリクエスト関数。
async def fetch_async_get(url, params):
    """
    非同期HTTP GETリクエストを実行します。
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.content

# テキスト入力の検証用のユーティリティ関数。
def validate_text_input(text):
    """
    テキスト入力を特定の条件（長さ、文字など）で検証します。
    必要に応じてカスタマイズ可能です。
    """
    if not text:
        raise ValueError("テキスト入力は空にできません。")
    if len(text) > 500:
        raise ValueError("テキスト入力が長すぎます。")
    return text

# TTSエンドポイントのURLを検証するためのユーティリティ関数。
def validate_url(url):
    """
    TTSサービスのURLを検証します。
    """
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        raise ValueError("TTSサービスのURLが無効です。")
    return url

# テキストを分割するための関数。
def split_text(text, max_length=100):
    """
    与えられたテキストを指定された最大長で分割します。
    """
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

# chat.pyで使用される関数。
def get_chat_response(user_input):
    """
    チャットボットからの応答を生成します。
    実際のチャットアプリケーションやAIモデルとの対話ロジックにこれを置き換えてください。
    """
    return "エコー: " + user_input

# TTSサービスに送る前にテキストを処理するか変換する必要があれば、ここに関数を追加します。
def preprocess_text_for_tts(text):
    """
    TTS用のテキストを前処理します。特殊文字の処理、クリーニングなどを行います。
    """
    text = text.replace('\n', ' ').strip()
    return text
