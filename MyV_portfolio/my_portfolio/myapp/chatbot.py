# chatbot.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()  # これにより .env ファイルの内容が環境変数に読み込まれます

# .env ファイルが上のディレクトリにあるため、そのパスを設定
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# スクリプトファイルのあるディレクトリのパスを取得
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"スクリプトディレクトリ: {script_directory}")

# テンプレートファイルへの相対パスを設定
TEMPLATE_PATH = os.path.join(script_directory, "template.txt")
SYSTEM_TEMPLATE_PATH = os.path.join(script_directory, "system_template.txt")

# OpenAI APIキーを定義
API_KEY = os.getenv('OPENAI_API_KEY')

# テンプレートを読み込む関数
def load_template(path: str):
    with open(path, 'r') as f:
        template = f.read()
    return template

# テンプレートを読み込み、変数を初期化
template = load_template(TEMPLATE_PATH)
system_template = load_template(SYSTEM_TEMPLATE_PATH)

# プロンプトを編集する関数
def edit_prompt(template: str, text: str, token="{query}"):
    return template.replace(token, text)

# プロンプトに対するレスポンスを取得する関数
def prompt_response(prompt: str, system_prompt: str):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + API_KEY,
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}, {"role": "system", "content": system_prompt}],
        "max_tokens": 200,
        "temperature": 1,
        "top_p": 1,
    }
    
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
        response.raise_for_status()  # これによりHTTPエラー時に例外が発生します。
    except requests.exceptions.RequestException as e:  # すべてのリクエストエラーをキャッチ
        print(f"リクエスト中にエラーが発生しました: {e}")
        return {"error": f"リクエスト中にエラーが発生しました: {e}"}
    
    return response.json()

# レスポンスの前処理を行う関数
def preprocess_response(res):
    if "error" in res:
        print(f"APIエラー: {res['error']}")
        return f"エラーが発生しました: {res['error']}"
    elif 'choices' not in res or not res['choices']:
        print("不正なレスポンス: 'choices' キーがありません。")
        return "エラーが発生しました: 'choices' キーがレスポンスに含まれていません。"
    text = res['choices'][0]['message']['content']
    return text

# ユーザーからの入力に対するチャットボットの応答を取得する関数
def get_chat_response(text: str, user_prompt: str):
    prompt = edit_prompt(user_prompt, text)
    res = prompt_response(prompt, system_template)
    res_text = preprocess_response(res)
    return res_text
