from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.templatetags.static import static

from .models import Character
class CharacterForm(forms.ModelForm):
    # 既存のフィールド
    selected_color = forms.CharField(
        max_length=7, 
        widget=forms.TextInput(attrs={'type': 'color'}), 
        required=False
    )
    clear_background_color = forms.BooleanField(
        required=False,
        label='背景色をクリア'
    )
    BACKGROUND_CHOICES = [
        ('room.jpg', '部屋'),
        ('school.jpg', '学校'),
        ('cyber.jpg', '電子空間'),
        ('stream.png', '動く背景'),
        ('symbol.gif', '配信中')
    ]
    background_choice = forms.ChoiceField(
        choices=BACKGROUND_CHOICES,
        required=False,
        label='運営が提供する背景画像'
    )

    # 新しいプロンプトフィールドを追加
    gpt_prompt1 = forms.CharField(
        max_length=500, 
        required=False, 
        widget=forms.Textarea, 
        label='プロンプト1'
    )
    gpt_prompt2 = forms.CharField(
        max_length=500, 
        required=False, 
        widget=forms.Textarea, 
        label='プロンプト2'
    )
    gpt_prompt3 = forms.CharField(
        max_length=500, 
        required=False, 
        widget=forms.Textarea, 
        label='プロンプト3'
    )

    def __init__(self, *args, **kwargs):
        super(CharacterForm, self).__init__(*args, **kwargs)
        # 背景画像の選択肢を動的に設定
        self.fields['background_choice'].choices = [
            (static('images/room.jpg'), '部屋'),
            (static('images/school.jpg'), '学校'),
            (static('images/cyber.jpg'), '電子空間'),
            (static('images/stream.png'), '動く背景'),
            (static('images/symbol.gif'), '配信中')
        ]

    class Meta:
        model = Character
        fields = [
            # 既存のフィールドを列挙
            'body_image', 'closed_eyes_image', 'open_eyes_image',
            'open_mouth_image', 'half_open_mouth_image', 'closed_mouth_image',
            'background_image', 'selected_color', 'clear_background_color',
            'background_choice',
            # 新しいプロンプトフィールドを追加
            'gpt_prompt1', 'gpt_prompt2', 'gpt_prompt3'
        ]

# Userモデルに対するカスタムサインアップフォーム
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
    
    def __init__(self, *args, **kwargs):
        hide_email = kwargs.pop('hide_email', False)
        super(SignUpForm, self).__init__(*args, **kwargs)

        if hide_email:
            self.fields['email'].widget = forms.HiddenInput()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("このユーザー名は既に使用されています。")
        return username