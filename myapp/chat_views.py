# chat_views.py

import json
import logging
from io import BytesIO
import soundfile as sf
from django.http import HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods

from .chatbot import get_chat_response  # chatbot.pyからget_chat_response関数をインポートします。
from .utils import preprocess_text_for_tts
from .tts_service import stream_tts_response  # 非同期関数から同期関数に変更された
from .tts import text2speech

# ロガーの設定
logger = logging.getLogger(__name__)

@require_http_methods(['POST'])  # POSTリクエストのみ許可する
def chat_with_gpt(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get('text_input')
        
         # 文字数制限のチェック
        if len(user_input) > 50:
            return HttpResponse('入力されたテキストは50文字を超えています。', status=400, content_type='text/plain')

        chat_response = get_chat_response(user_input)  # 非同期呼び出しを同期呼び出しに変更

        tts_input = preprocess_text_for_tts(chat_response)

        combined_audio_numpy = stream_tts_response(tts_input)  # 非同期呼び出しを同期呼び出しに変更

        in_memory_file = BytesIO()
        sf.write(in_memory_file, combined_audio_numpy, text2speech.fs, format='WAV')
        in_memory_file.seek(0)

        response = FileResponse(in_memory_file, as_attachment=True, filename='tts_output.wav')
        response['Content-Type'] = 'audio/wav'
        return response

    except json.JSONDecodeError as e:
        logger.exception("JSONデコードエラーが発生しました。")
        return HttpResponse('JSONデコードエラー: ' + str(e), status=400, content_type='text/plain')

    except Exception as e:
        logger.exception("予期せぬエラーが発生しました。")
        return HttpResponse('サーバーエラー: ' + str(e), status=500, content_type='text/plain')
