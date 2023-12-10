from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Djangoの標準Userモデルを使っている場合は、次のようになります。
        # return f"{user.pk}{timestamp}{user.is_active}"
        return f"{user.pk}{timestamp}"

account_activation_token = AccountActivationTokenGenerator()
