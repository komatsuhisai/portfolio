from django.shortcuts import render, redirect
from .models import Character
from django.contrib.auth.decorators import login_required

@login_required
def update_user_prompt(request):
    user = request.user
    character, created = Character.objects.get_or_create(user=user)

    if request.method == 'POST':
        # プロンプトの内容を更新
        character.gpt_prompt1 = request.POST.get('gpt_prompt1', character.gpt_prompt1)
        character.gpt_prompt2 = request.POST.get('gpt_prompt2', character.gpt_prompt2)
        character.gpt_prompt3 = request.POST.get('gpt_prompt3', character.gpt_prompt3)

        # 選択されたプロンプトを更新
        selected_prompt = request.POST.get('selected_prompt')
        if selected_prompt in ['prompt1', 'prompt2', 'prompt3']:
            character.selected_prompt = selected_prompt

        character.save()
        return redirect('index')  # 適切なリダイレクト先に変更

    context = {
        'current_prompt1': character.gpt_prompt1,
        'current_prompt2': character.gpt_prompt2,
        'current_prompt3': character.gpt_prompt3,
        'selected_prompt': character.selected_prompt,
        'default_prompt1': Character._meta.get_field('gpt_prompt1').get_default(),
        'default_prompt2': Character._meta.get_field('gpt_prompt2').get_default(),
        'default_prompt3': Character._meta.get_field('gpt_prompt3').get_default(),
    }
    return render(request, 'user_prompt_form.html', context)

