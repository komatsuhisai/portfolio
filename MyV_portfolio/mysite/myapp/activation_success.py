# activation_success.py

from django.shortcuts import render, redirect
from .forms import SignUpForm  # 確認しているフォームをインポート

def signup_view(request):
    # アクティベーションが完了しているという条件が真の場合
    # （具体的な条件はアプリケーションのロジックに依存します）
    if request.method == 'POST':
        form = SignUpForm(request.POST, hide_email=True)  # hide_emailをTrueとして渡す
        if form.is_valid():
            form.save()  # ユーザーを保存
            return redirect('login')  # ログインページへリダイレクト
    else:
        # GETリクエストの場合、またはフォームが無効だった場合には、
        # フォームを非表示にするかどうかを決定する条件に基づいて初期化します。
        # ここではシンプルに示すために常にTrueとしていますが、
        # 実際にはセッション、クエリパラメータ、トークンの確認などに基づく条件を使用するでしょう。
        form = SignUpForm(hide_email=True)

    return render(request, 'activation_success.html', {'form': form})
