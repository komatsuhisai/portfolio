# character.py


from django.contrib.staticfiles import finders
from django.core.files import File
from django.http import JsonResponse  # 新しく追加
from django.shortcuts import render, redirect
from .forms import CharacterForm
from .models import Character
from django.conf import settings
import os
import logging
from django.http import HttpResponse, JsonResponse


logger = logging.getLogger(__name__)

def upload_character_images(request):
    character, created = Character.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES, instance=character)

        if 'reset_defaults' in request.POST:
            # デフォルトの背景色にリセット
            character.selected_color = "#ffffff"
            default_images = {
                'body_image': 'images/body.png',
                'closed_eyes_image': 'images/eyes_close.png',
                'open_eyes_image': 'images/eyes.png',
                'open_mouth_image': 'images/mouth_open.png',
                'half_open_mouth_image': 'images/mouth_half.png',
                'closed_mouth_image': 'images/mouth_close.png',
                'background_image': None
            }

            for field, image_path in default_images.items():
                if image_path:
                    actual_path = finders.find(image_path)
                    if actual_path:
                        with open(actual_path, 'rb') as default_image_file:
                            getattr(character, field).save(os.path.basename(image_path), File(default_image_file), save=False)
                    else:
                        logger.error(f"Default image file for {field} not found: {image_path}")
                else:
                    setattr(character, field, None)

            character.save()
            return redirect('upload_character_images')

        # ... [残りの処理] ...


        if form.is_valid():
            form.save()
            logger.debug("Character updated: %s", character.__dict__)
            return redirect('index')
        else:
            logger.debug("Form is invalid")
            logger.debug("Errors: %s", form.errors.as_json())
    else:
        form = CharacterForm(instance=character)

    # テンプレートに背景色を渡す
     # テンプレートに渡すコンテキストに character を追加
    context = {'form': form, 'character': character}
    return render(request, 'character_form.html', context)


def load_background_color(request):
    character, _ = Character.objects.get_or_create(user=request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        selected_color = character.selected_color
        return JsonResponse({'color': selected_color})
    else:
        return HttpResponse(status=400)  # AJAX以外のリクエストを拒否

# character.py の外部に get_provided_background_images 関数を定義
def avatar_edit(request):
    # ユーザーに関連付けられたキャラクターを取得または作成
    character, _ = Character.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CharacterForm(request.POST, request.FILES, instance=character)

        if form.is_valid():
            # フォームのデータをモデルに保存
            character = form.save(commit=False)
            
            # 運営が提供する背景画像の選択を処理
            background_choice = form.cleaned_data.get('background_choice')
            if background_choice:
                character.selected_background_image = background_choice

            # その他のフォームデータを保存
            character.save()

            # フォームの送信後にリダイレクト
            return redirect('avatar_edit')  # ここは適切なリダイレクト先に変更
        else:
            # フォームが無効の場合、エラーを表示
            return render(request, 'add_character.html', {'form': form})
    else:
        # GETリクエストの場合、フォームを初期化
        form = CharacterForm(instance=character)

    return render(request, 'add_character.html', {'form': form})