#accounts_views
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import EmailConfirmationToken
from django.contrib.auth.decorators import login_required
import uuid
from .models import EmailConfirmationToken
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Character
from django.http import Http404
import logging

# ロガーの設定
logger = logging.getLogger(__name__)





@login_required
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        if User.objects.filter(username=new_username).exists():
            messages.error(request, 'このユーザーネームは既に使用されています。')
        elif new_username and new_username != request.user.username:
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'ユーザーネームが更新されました。')
            return redirect('change_username')
        else:
            messages.error(request, '新しいユーザーネームを入力してください。')

    return render(request, 'settings/change_username.html')

@login_required
def user_settings(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        if new_username and new_username != request.user.username:
            # ユーザー名の更新処理
            request.user.username = new_username
            request.user.save()
            # 必要に応じてユーザーに通知するなどの追加処理をここに記述

    current_username = request.user.username
    current_email = request.user.email

    return render(request, 'settings/settings.html', {
        'current_username': current_username,
        'current_email': current_email,
    })


@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        if new_email and new_email != request.user.email:
            # 既存のトークンを検索または新しいトークンを作成
            token, created = EmailConfirmationToken.objects.get_or_create(
                user=request.user,
                defaults={'token': uuid.uuid4()}
            )
            if not created:
                # 既存のトークンを更新
                token.token = uuid.uuid4()
                token.save()

            # 確認メールのURLを生成
            confirmation_url = request.build_absolute_uri(
                '/confirm_email/{}/'.format(token.token)
            )
            # 確認メールを送信
            send_mail(
                '新しいメールアドレスの確認',
                f'新しいメールアドレスを確認するために、以下のリンクをクリックしてください: {confirmation_url}',
                'from@example.com',
                [new_email],
                fail_silently=False,
            )
            return redirect('email_change_done')

    return render(request, 'settings/change_email.html')
from django.shortcuts import render

def email_change_done(request):
    # メールアドレス変更完了ページを表示
    return render(request, 'settings/email_change_done.html')






def user_settings(request):
    

    return render(request, 'settings/settings.html')
        




def password_settings(request):
    # ここでパスワード変更に関連する処理を行います
    # 例: パスワード変更フォームの表示と処理
    return render(request, './settings/password_settings.html')


def notification_settings(request):
    # ここで通知設定に関連する処理を行います
    # 例: 通知のオプション表示と更新
    return render(request, './settings/notification_settings.html')

def payment_info(request):
    # ここで支払い情報に関連する処理を行います
    # 例: 支払い方法の表示と更新
    return render(request, './settings/payment_info.html')



@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        if new_email and new_email != request.user.email:
            # 新しいトークンを作成または既存のトークンを更新
            token, created = EmailConfirmationToken.objects.get_or_create(
                user=request.user,
                defaults={'token': uuid.uuid4(), 'new_email': new_email}
            )
            if not created:
                token.token = uuid.uuid4()
                token.new_email = new_email
                token.save()

            # 確認メールのURLを生成
            confirmation_url = request.build_absolute_uri(
                '/myapp/confirm_email/{}/'.format(token.token)
            )
            # 確認メールを送信
            send_mail(
                '新しいメールアドレスの確認',
                f'新しいメールアドレスを確認するために、以下のリンクをクリックしてください: {confirmation_url}',
                'from@example.com',
                [new_email],
                fail_silently=False,
            )
            return redirect('email_change_done')

    return render(request, 'settings/change_email.html')

@login_required
def confirm_email(request, token):
    email_token = get_object_or_404(EmailConfirmationToken, token=token)
    
    # メールアドレスの更新
    if email_token.new_email:
        user = email_token.user
        user.email = email_token.new_email
        user.save()
        messages.success(request, 'メールアドレスが正常に更新されました。')
    else:
        messages.error(request, '無効なメールアドレスです。')

    return redirect('email_confirmation_done')


def email_confirmation_done(request):
    # メール確認完了ページの表示
    return render(request, 'settings/email_confirmation_done.html')


def my_page(request):
    try:
        character = Character.objects.get(user=request.user)
        logger.debug(f"Character found: {character}")
    except Character.DoesNotExist:
        logger.error(f"Character not found for user: {request.user}")
        raise Http404("キャラクターが見つかりません。")
    
    return render(request, 'settings/my_page.html', {'character': character})