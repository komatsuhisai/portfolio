# # character_form_reset.py 
# from .forms import CharacterForm
# from .models import Character
# from django.shortcuts import render, redirect

# def upload_character_images(request):
#     character, created = Character.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         if 'action' in request.POST and request.POST['action'] == 'reset_defaults':
#             # デフォルト画像をファイルオブジェクトとして開く
#             default_body_image = open('path/to/default/body_image.png', 'rb')
#             default_closed_eyes_image = open('path/to/default/closed_eyes_image.png', 'rb')
#             # ImageField にファイルオブジェクトを割り当てる
#             character.body_image.save('default_body_image.png', File(default_body_image), save=False)
#             character.closed_eyes_image.save('default_closed_eyes_image.png', File(default_closed_eyes_image), save=False)
#             # その他のフィールドにも同様の操作を行う...
#             character.save()
#             # すべてのファイルを閉じる
#             default_body_image.close()
#             default_closed_eyes_image.close()
#             return redirect('upload_character_images')
#         else:
#             form = CharacterForm(request.POST, request.FILES, instance=character)
#             if form.is_valid():
#                 form.save()
#                 return redirect('upload_character_images')  # URLの名前を修正しました
#     else:
#         form = CharacterForm(instance=character)

#     return render(request, 'character_form.html', {'form': form})
