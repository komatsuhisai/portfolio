# tts.py

from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from espnet2.bin.tts_inference import Text2Speech
import torch
import io
import soundfile as sf




# TTSモデルを一度だけ初期化します
fs, lang = 44100, "Japanese"
text2speech = Text2Speech.from_pretrained(
    model_tag="kan-bayashi/jsut_transformer",  # または "kan-bayashi/jsut_transformer"
    device="cpu",  # GPUがある場合は "cuda" を使用
    speed_control_alpha=1.0,
    noise_scale=0.333,
    noise_scale_dur=0.333,
)

@csrf_exempt
def tts_streamer(request):
    # POSTリクエストのみを処理します
    if request.method != "POST":
        return HttpResponse("Method Not Allowed", status=405)

    # POSTリクエストデータからテキスト入力を取得します
    text_data = request.POST.get("text_input", "").strip()
    if not text_data:
        return HttpResponse("Bad Request: No text provided", status=400)

    try:
        # 勾配計算を行わない形で音声を合成します
        with torch.no_grad():
            wav = text2speech(text_data)["wav"]

        # 一時的なメモリストリームにwavデータを書き込みます
        wav_io = io.BytesIO()
        sf.write(wav_io, wav.numpy(), fs)
        wav_io.seek(0)

        # ストリーミング応答を作成します
        response = StreamingHttpResponse(wav_io, content_type="audio/wav")
        response['Content-Disposition'] = 'inline; filename="tts_output.wav"'
        return response
    except Exception as e:
        # 例外が発生した場合、適切なHTTPレスポンスでクライアントに通知します。
        return HttpResponse(f"Internal Server Error: {str(e)}", status=500)
