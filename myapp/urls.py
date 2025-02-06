# urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path
from myapp.views import index, edit_character, update_voice_model, home, check_your_email, complete_registration
from myapp.chat_views import chat_with_gpt
# from myapp.chat_response import ChatBotResponseView  # こちらが正しいインポート文です
from myapp.views import index, chat_response
from myapp.activation_success import signup_view
from myapp.character import upload_character_images, avatar_edit, load_background_color
from myapp.prompt import update_user_prompt
from myapp.tts_service import stream_tts_response
from myapp.accounts.urls import path
from myapp.accounts.views import PasswordChange


from .tts import tts_streamer
from . import views
from django.urls import include, path

from myapp.account_views import user_settings, password_settings, notification_settings, payment_info, email_change_done, change_email, change_username, confirm_email, email_confirmation_done, my_page
# urls.py
from django.urls import path
from myapp.stripe_webhooks import stripe_webhook  # stripe.py から stripe_webhook をインポート












urlpatterns = [
    path('index/', index, name='index'),
    path('chat/', chat_with_gpt, name='chat_with_gpt'),
    path('tts_streamer/', tts_streamer, name='tts_streamer'),
    path('chat-response/', chat_response, name='chat_response'),
    path('edit_character/', edit_character, name='edit_character'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # path('confirm_email/<uuid:token>/', views.confirm_email, name='confirm_email'),
    # path('resend_email/<int:user_id>/', views.resend_confirmation_email, name='resend_email'),
    # path('home/<int:user_id>/', views.resend_confirmation_email, name='resend_email'),
    path('', views.home, name='home'),  # ホームページ
    
    # メールを確認するように案内するページのパス
    path('check_your_email/', views.check_your_email, name='check_your_email'),
    path('pre_signup/', views.pre_signup, name='pre_signup'),
    path('complete_registration/<uidb64>/<token>/', views.complete_registration, name='complete_registration'),
    
    #事前トークンエラー用
    path('activation_success/', signup_view, name='some_view_for_successful_activation'),

    path('activation_invalid/', views.invalid_or_expired_token, name='some_view_for_invalid_or_expired_token'),
    
    path('account/complete/', views.account_complete, name='account_complete'),
    path('upload_character_images/', upload_character_images, name='upload_character_images'),
    path('update-prompt/', update_user_prompt, name='update_prompt'),
    path('tts/', stream_tts_response, name='tts'),  # 新しいTTS APIエンドポイント
    path('update_voice_model/', update_voice_model, name='update_voice_model'),
    path('update_selected_model/', views.update_selected_model, name='update_selected_model'),


 #パスワードリセット関連のURL
   path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',  # パスワードリセットテンプレート
        email_template_name='accounts/password_reset_email.html',  # メールテンプレート
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    path('accounts/', include('myapp.accounts.urls')),
    path('myapp/upload_character_images/', avatar_edit, name='avatar_edit'),
    path('load_background_color/', load_background_color, name='load_background_color'),
    path('update-prompt/', update_user_prompt, name='update_user_prompt'),
    
    
    path('help/', views.help_page, name='help'),
    
    
    path('settings/setting/', user_settings, name='user_settings'),
    path('settings/password/', password_settings, name='password_settings'),
    path('settings/notification/', notification_settings, name='notification_settings'),
    path('settings/payment/', payment_info, name='payment_info'),
    path('settings/email_change_done/', email_change_done, name='email_change_done'),
    path('settings/change_email/', change_email, name='change_email'),
    path('settings/change_username/', change_username, name='change_username'),
    path('confirm_email/<uuid:token>/', confirm_email, name='confirm_email'),
    path('email-confirmation-done/', email_confirmation_done, name='email_confirmation_done'),
    path('payment_info/', views.payment_info, name='payment_info'),
    path('my_page/', my_page, name='my_page'),
    path('edit_character/', edit_character, name='edit_character'),  # 変更しました

    path('tokutei/', views.tokutei, name='tokutei'),
    
    # path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
    # path('stripe/webhook-status', views.webhook_status, name='webhook_status'),



]
