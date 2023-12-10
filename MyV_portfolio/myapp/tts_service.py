# tts_service.py

import logging
import json
from io import BytesIO
import soundfile as sf
import torch
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from espnet2.bin.tts_inference import Text2Speech
from .utils import split_text
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Character


# ロガーの設定
logger = logging.getLogger(__name__)

# TTSモデルが使用するサンプリングレート
fs = 44100

@csrf_exempt
def stream_tts_response(request, text_data):
    try:
        user = request.user
        character = Character.objects.get(user=user)
        model_tag = character.selected_voice_model

        text2speech = Text2Speech.from_pretrained(
            model_tag=model_tag,
            device="cpu",
            speed_control_alpha=1.0,
            noise_scale=0.333,
            noise_scale_dur=0.333,
        )


        # テキストを分割して音声合成
        split_response = split_text(text_data)
        combined_audio = None
        for sq_text in split_response:
            with torch.no_grad():
                tts_output = text2speech(sq_text)
                wav = tts_output["wav"]
                if wav is None:
                    raise ValueError("No audio generated")

                if combined_audio is None:
                    combined_audio = wav
                else:
                    combined_audio = torch.cat((combined_audio, wav), dim=0)

        # wavデータをバイト列として返す
        wav_io = BytesIO()
        sf.write(wav_io, combined_audio.numpy(), fs, format='WAV')
        wav_io.seek(0)
        return wav_io.read()
        
    except Character.DoesNotExist:
        logger.error(f"Character not found for user: {user.username}")
        return HttpResponse('Character not found', status=404)
    except Exception as e:
        logger.error(f"stream_tts_response関数内でエラーが発生しました: {e}")
        return None
