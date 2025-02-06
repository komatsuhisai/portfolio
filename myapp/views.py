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
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User, Character
from django.core.files import File
from django.contrib.staticfiles import finders
import os
from django.contrib.auth.forms import UserCreationForm



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

from django import forms
from .models import Character
from django.core.files import File
from django.contrib.staticfiles import finders



class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['gpt_prompt1', 'gpt_prompt2', 'gpt_prompt3', 'selected_prompt', 'body_image', 'closed_eyes_image', 'open_eyes_image', 'open_mouth_image', 'half_open_mouth_image', 'closed_mouth_image', 'background_image', 'selected_voice_model', 'selected_color', 'selected_background_image']

def tokutei(request):
    return render(request, 'tokutei.html')


class CustomSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        
        


def account_complete(request):
    # ユーザーがこのビューにアクセスした時点で、アクティベーションは既に完了していると仮定します。
    # 追加のコンテキストは特に必要ありませんが、必要に応じて追加できます。
    return render(request, 'account_complete.html')

# メールによるアカウント登録確認の完了
def complete_registration(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = CustomSignUpForm(request.POST, instance=user)
            if form.is_valid():
                user.set_password(form.cleaned_data["password1"])
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('account_complete')
            else:
                return render(request, 'activation_success.html', {'form': form})
        else:
            form = CustomSignUpForm()
            return render(request, 'activation_success.html', {'form': form})
    else:
        return redirect('invalid_or_expired_token')




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_character(sender, instance, created, **kwargs):
    if created:
        character, character_created = Character.objects.get_or_create(user=instance)
        if character_created:
            default_images = {
                'body_image': 'images/body.png',
                'closed_eyes_image': 'images/eyes_close.png',
                'open_eyes_image': 'images/eyes_open.png',
                'open_mouth_image': 'images/mouth_open.png',
                'half_open_mouth_image': 'images/mouth_half_open.png',
                'closed_mouth_image': 'images/mouth_closed.png',
                'background_image': 'images/default_background.png'
            }

            for field_name, image_path in default_images.items():
                image_full_path = finders.find(image_path)
                if image_full_path:
                    with open(image_full_path, 'rb') as image_file:
                        file_instance = File(image_file, name=os.path.basename(image_path))
                        setattr(character, field_name, file_instance)
                else:
                    logger.error(f"Default image file not found: {image_path}")

            character.save()












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
# プレサインアップ処理
class PreSignupForm(forms.Form):
    username = forms.CharField(label='ユーザーネーム', max_length=150)
    email = forms.EmailField(label='メールアドレス')

def pre_signup(request):
    if request.method == 'POST':
        form = PreSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # ユーザーネームまたはメールアドレスが既に存在するかチェック
            if User.objects.filter(username=username).exists():
                return render(request, 'pre_signup.html', {
                    'form': form,
                    'error_message': 'このユーザーネームは既に使用されています。'
                })
            if User.objects.filter(email=email).exists():
                return render(request, 'pre_signup.html', {
                    'form': form,
                    'error_message': 'このメールアドレスは既に使用されています。'
                })

            # 新規ユーザーの作成
            user = User.objects.create(username=username, email=email, is_active=False)
            logger.debug("新規ユーザーを作成しました: %s", email)

            # アクティベーションメールの送信
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('complete_registration', kwargs={'uidb64': uidb64, 'token': token})
            )

            subject = '【MyV】メールアドレスの確認'
            message = f'MyVのご登録ありがとうございます！\n以下のリンクをクリックして登録を完了してください:\n{activation_link}'
            send_mail(subject, message, 'info@26g.me', [email], fail_silently=False)

            return redirect('check_your_email')
    else:
        form = PreSignupForm()

    return render(request, 'pre_signup.html', {'form': form})







def check_your_email(request):
    # メール確認案内ページをレンダリングするだけ
    return render(request, 'check_your_email.html')



#ログイン関連
@login_required
def edit_character(request):
    character, created = Character.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES, instance=character)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CharacterForm(instance=character)

    return render(request, 'edit_character.html', {'form': form})

#update_voice_model移動
def update_voice_model(request):
    return render(request, 'update_voice_model.html')



def index(request):
    if request.user.is_authenticated:
       if request.user.is_authenticated:
        try:
            character = Character.objects.get(user=request.user)
            # 使用可能なAPI回数が上限に達している場合、フラグをセット
            show_api_limit_reached_message = not character.can_use_api()
            # フラグの値をログに出力
            logger.info(f"API limit reached message flag: {show_api_limit_reached_message}")
        except Character.DoesNotExist:
            character = None
            show_api_limit_reached_message = False


        context = {
            'character': character,
            'background_color': character.selected_color if character else "#ffffff",
            'show_api_limit_reached_message': show_api_limit_reached_message,
        }
        return render(request, 'index.html', context)
    else:
        return redirect('login')






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
        return JsonResponse({
            'text': response_text, 
            'audio_base64': audio_base64,
            'apiUsageCount': character.api_usage_count,
            'apiMaxUsageCount': character.api_max_usage_count
        }, status=200)

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

