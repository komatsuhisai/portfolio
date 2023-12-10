from django.shortcuts import render, redirect, get_object_or_404
from django.db import DatabaseError
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django import forms
from .forms import SignUpForm
from .tokens import account_activation_token  # トークンを検証するための関数
from .models import Character  # Character モデルをインポート



import json
import logging
import uuid
import base64

from .models import User, EmailConfirmationToken
from .tokens import account_activation_token
from .tts_service import stream_tts_response
from .chatbot import get_chat_response
logger = logging.getLogger(__name__)

User = get_user_model()

def account_complete(request):
    # ユーザーがこのビューにアクセスした時点で、アクティベーションは既に完了していると仮定します。
    # 追加のコンテキストは特に必要ありませんが、必要に応じて追加できます。
    return render(request, 'account_complete.html')

# メールによるアカウント登録確認の完了
def complete_registration(request, uidb64, token):
    # URLからUIDとトークンをデコード
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # ユーザーが存在し、トークンが有効な場合
    if user is not None and account_activation_token.check_token(user, token):
        # アクティベーションフォームが送信された場合
        if request.method == 'POST':
            form = SignUpForm(request.POST, hide_email=True)
            if form.is_valid():
                user.username = form.cleaned_data['username']
                user.set_password(form.cleaned_data['password1'])
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('account_complete')
            else:
                # フォームの入力に問題がある場合、フォームとエラーを再表示します。
                return render(request, 'activation_success.html', {'form': form})
        else:
            # GETリクエストでアクセスされた場合、hide_email=Trueを設定してフォームを提供します。
            form = SignUpForm(hide_email=True)
            return render(request, 'activation_success.html', {'form': form})
    else:
        # ユーザーが見つからないか、トークンが無効の場合
        return redirect('some_view_for_invalid_or_expired_token')








def successful_activation(request):
    # アカウントのアクティベーションが成功した場合のビュー
    return render(request, 'activation_success.html')

def already_active(request):
    # ユーザーアカウントがすでにアクティブな場合のビュー
    return render(request, 'activation_already_active.html')

def invalid_or_expired_token(request):
    # アクティベーショントークンが無効または期限切れの場合のビュー
    return render(request, 'activation_invalid_or_expired_token.html')







# プレサインアップ処理
class PreSignupForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')

def pre_signup(request):
    if request.method == 'POST':
        form = PreSignupForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                user, created = User.objects.get_or_create(email=email)
                if created:
                    user.is_active = False
                    user.save()
                    logger.debug("新規ユーザーを作成し、非アクティブに設定しました: %s", email)
                else:
                    logger.debug("既存のユーザーを取得しました: %s", email)

                # ユーザーのIDをBase64エンコード
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                # 新しいトークンを作成
                token = account_activation_token.make_token(user)

                # 正しいURLを生成
                complete_url = request.build_absolute_uri(
                    reverse('complete_registration', kwargs={'uidb64': uidb64, 'token': token})
                )
                logger.debug("完了URL: %s", complete_url)

                subject = 'メールアドレスの確認'
                message = f'以下のリンクをクリックして登録を完了してください:\n{complete_url}'
                logger.debug("メールを送信します: %s", email)

                send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                logger.debug("メール送信完了: %s", email)

                return redirect('check_your_email')

            except Exception as e:
                logger.error("pre_signupでエラーが発生しました: %s", e)
                return render(request, 'error.html', {'error': str(e)})
        else:
            logger.warning("無効なフォームデータが送信されました: %s", form.errors)
    else:
        form = PreSignupForm()

    return render(request, 'pre_signup.html', {'form': form})






def check_your_email(request):
    # メール確認案内ページをレンダリングするだけ
    return render(request, 'check_your_email.html')



#ログイン関連
@login_required
def add_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES)
        if form.is_valid():
            character = form.save(commit=False)  # まだデータベースには保存しない
            character.user = request.user  # ログインしているユーザーをセット
            character.save()  # これでデータベースに保存
            return redirect('index')  # 保存後にリダイレクト
    else:
        form = CharacterForm()

    return render(request, 'add_character.html', {'form': form})


#update_voice_model移動
def update_voice_model(request):
    return render(request, 'update_voice_model.html')



def index(request):
    if request.user.is_authenticated:
        try:
            character = Character.objects.get(user=request.user)
        except Character.DoesNotExist:
            character = None

        context = {
            'character': character,
            'background_color': character.selected_color if character else "#ffffff",
        }
        return render(request, 'index.html', context)
    else:
        return redirect('login')  # 未ログインの場合はログインページへリダイレクト




# def index(request):
#     if request.user.is_authenticated:
#         try:
#             character = Character.objects.get(user=request.user)  # ユーザーに関連付けられたキャラクターを取得
#         except Character.DoesNotExist:
#             character = None  # キャラクターが存在しない場合は None をセット
#         context = {'character': character}
#         return render(request, 'index.html', context)
#     else:
#         return redirect('login')  # ログインページへリダイレクト



#ホーム表示
def home(request):
    # `home.html`テンプレートを使ってレスポンスを返す
    return render(request, 'home.html')

#htmlから音声モデルを選択してデータベースに渡す
@csrf_exempt
def update_selected_model(request):
    logger.info("Received model update request")

    if request.method != 'POST':
        logger.error("Request is not POST")
        return JsonResponse({'error': 'POSTリクエストが必要です'}, status=400)

    try:
        data = json.loads(request.body)
        logger.info(f"Request data: {data}")
        selected_model = data.get('selected_model', '')

        user = request.user
        character = Character.objects.get(user=user)
        character.selected_voice_model = selected_model
        character.save()

        logger.info(f"Model updated for user {user.username}: {selected_model}")
        return JsonResponse({'success': True})

    except Character.DoesNotExist:
        logger.error("Character not found")
        return JsonResponse({'error': 'Character not found'}, status=404)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


# 音声データエンコード
@csrf_exempt
def chat_response(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POSTリクエストが必要です'}, status=400)

    try:
        data = json.loads(request.body)
        input_text = data.get('text_input', '')

        user = request.user
        character = Character.objects.get(user=user)

        if not character.can_use_api():
            return JsonResponse({'error': 'API使用制限に達しました'}, status=403)

        character.api_usage_count += 1
        character.save()

        # 選択されたプロンプトに応じてプロンプトを取得
        selected_prompt = character.selected_prompt
        if selected_prompt == 'prompt1':
            user_prompt = character.gpt_prompt1
        elif selected_prompt == 'prompt2':
            user_prompt = character.gpt_prompt2
        else:  # 'prompt3' またはデフォルト
            user_prompt = character.gpt_prompt3

        response_text = get_chat_response(input_text, user_prompt)

        audio_data = stream_tts_response(request, response_text)
        if audio_data is None:
            return JsonResponse({'error': '音声生成エラー'}, status=500)

        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return JsonResponse({'text': response_text, 'audio_base64': audio_base64}, status=200)

    except json.JSONDecodeError as e:
        logger.error('JSON解析エラー: %s', str(e), exc_info=True)
        return JsonResponse({'error': '無効なJSONデータ'}, status=400)

    except DatabaseError as e:
        logger.error('データベースエラー: %s', str(e), exc_info=True)
        return JsonResponse({'error': 'データベースエラーが発生しました'}, status=500)

    except Exception as e:
        logger.error('予期せぬエラー: %s', str(e), exc_info=True)
        return JsonResponse({'error': 'サーバーエラーが発生しました'}, status=500)
    
    

def payment_info(request):
    # ここでお支払情報に関連するデータを処理する
    # 例: ユーザーのお支払情報をデータベースから取得
    return render(request, 'settings/payment_info.html')







def help_page(request):
    # ヘルプページのビュー
    return render(request, 'help.html')

