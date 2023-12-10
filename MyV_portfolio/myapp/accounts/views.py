from django.shortcuts import render
# PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteViewを追加
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import EmailMessage



class index(LoginRequiredMixin, generic.TemplateView):
    template_name = 'myapp/templates/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "top"
        return context



class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context



class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'accounts/password_change_done.html'

# --- ここから追加
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/reset/subject.txt'
    email_template_name = 'accounts/mail_template/reset/message.txt'
    template_name = 'myapp/templates/accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'accounts/password_reset_done.html'
    
class PasswordResetDone(PasswordResetDoneView):
        template_name = 'accounts/password_reset_done.html'





class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_confirm.html'

# --- ここまで

