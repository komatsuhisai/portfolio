from django.contrib import admin
from .models import Character  # Character モデルをインポート

# ModelAdmin クラスを継承してカスタマイズ
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('user', 'body_image', 'gpt_prompt1', 'gpt_prompt2', 'gpt_prompt3')  # 管理リストに表示したいフィールド名
    search_fields = ['user__username', 'gpt_prompt1', 'gpt_prompt2', 'gpt_prompt3']  # 検索フィールド
    list_filter = ('user',)  # フィルターとして使用したいフィールド

# admin.site.register() 関数を使って、モデルと ModelAdmin クラスを登録
admin.site.register(Character, CharacterAdmin)