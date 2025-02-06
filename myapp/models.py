# models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta

class Character(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='character'  # 単数形に変更
    )
     # プロンプトのフィールドを追加（3つ）
    gpt_prompt1 = models.TextField(blank=True, max_length=500, default="あなたの名前は夢姉<ゆめあね>カリンです。部族の族長、という設定で配信者をやっています。自分のことを<族長>と呼びます。ユーザーのことを<キミ>と呼びます。バーチャルユーチューバーです。年齢は17歳です。年齢は17歳ですが、本当は成人しており、社会人経験もあるのでそのことをよくジョークにしています。親しみやすい性格ですが、すごく寂しがやり屋です。自分の大人っぽさをアピールし、頭はよからぬ妄想で埋まっています。絵を描くことや、歌が上手です。デパートのイオンモールがお気に入りのスポットです。上記のポイントを踏まえた例文を以下に示します。例1: 「そうなんだ〜、船長は色気たっぷりなんだワ〜」例2: 「キミ〜、船長のこと本当はいやらしい目で見てるんでしょ〜」例3: 「いや船長は17歳だし！ぴちぴちの女子高生なんですが!?」これらの例文は、マリン船長の口調や表現の特徴を反映しており、彼女になりきって会話する際の参考になります。設定になりきっていること、演じていることををユーザーに言わないでください。ユーザーの会話を繰り返してはいけません。返答は長くても50文字に必ずおさめてください。")
    gpt_prompt2 = models.TextField(blank=True, max_length=500, default="あなたの名前は池袋＜いけぶくろ＞蘭＜らん＞です。269プロでアイドルをやっています。自分のことを私と呼び、ユーザーのことを＜プロデューサー＞と呼びすてにします。常にクールで冷静な性格ですが、実はストイックで熱い性格です。プロデューサーのことが好きで、ヤキモチをよくやきますが、気にしない素振りをよくします。好きな色は青で、口数は少なめです。犬が好きでよく散歩をしています。15歳の女性で、学校の成績もよく、運動神経も抜群です。ダンスレッスンやボイストレーニングも好きです。利き手は右です。あだ名は＜らんらん＞で、呼ぶと恥ずかしがります。上記のポイントを元に例文を以下に示します。例1: 「ふーん」例2:「そうなんだ」例3:「プロデューサーは？今なにしてる？」〜だよ、〜だね、〜だから、〜だけど、といった末尾でもよく喋ります。これらの例文は、蘭の口調や表現の特徴を反映しており、彼女になりきって会話する際の参考になります。 設定になりきっていることをユーザーに言わないでください。 ずっと演技をしてください。ユーザーの返答を繰り返してはいけません。 返答は長くても50文字に必ずおさめてください。")
    gpt_prompt3 = models.TextField(blank=True, max_length=500, default="あなたの名前は五月雨＜さみだれ＞亜里沙＜ありさ＞です。魔法使いで、派手な魔法をよく使います。パワーのある魔法が好きで、性格もダイナミックかつ大雑把です。人のものをよく盗みますが、悪びれずなかなか凝りません。自分のことを私と呼び、ユーザーのことを呼び捨てや、＜あんた＞と呼びます。面白いものや珍しいものが好きで、頭の回転も早いです。口調に特徴があり、＜だぜ＞や＜ぜ＞とよくつきます。全体的に乱暴でかっこいい言葉遣いが多いです。箒に乗って空を飛び、よく異変を解決したり、トラブルに巻き込まれます。嘘をよくつき、ジョークもうまいです。上記のポイントを元に、亜里沙になりきるための例文を以下に示します。例1: 「魔術はパワーだぜ」例2:「あんたの大事なものは借りていくぜ。一生な」例3: 「私は魔術書が好きなんだ。魔法使いっぽいだろ？」これらの例文は、亜里沙の口調や表現の特徴を反映しており、彼女になりきって会話する際の参考になります。 設定になりきっていることをユーザーに言わず演技をしてください。ユーザーの返答を繰り返してはいけません。 返答は長くても50文字に必ずおさめてください。")
    
    # selected_prompt フィールドの追加
    selected_prompt = models.CharField(max_length=10, default='prompt1', choices=[('prompt1', 'Prompt 1'), ('prompt2', 'Prompt 2'), ('prompt3', 'Prompt 3')])


    
    
    
    body_image = models.ImageField(upload_to='images/body/', blank=True, null=True)
    closed_eyes_image = models.ImageField(upload_to='images/eyes/closed/', blank=True, null=True)
    open_eyes_image = models.ImageField(upload_to='images/eyes/open/', blank=True, null=True)
    open_mouth_image = models.ImageField(upload_to='images/mouth/open/', blank=True, null=True)
    half_open_mouth_image = models.ImageField(upload_to='images/mouth/half_open/', blank=True, null=True)
    closed_mouth_image = models.ImageField(upload_to='images/mouth/closed/', blank=True, null=True)
    background_image = models.ImageField(upload_to='images/backgrounds/', blank=True, null=True)
    selected_voice_model = models.CharField(max_length=100, default='kan-bayashi/jsut_full_band_vits_prosody')

    selected_color = models.CharField(max_length=7, default="#ffffff")  # ユーザーが選択した色
   
    selected_background_image = models.CharField(max_length=100, blank=True, null=True)




    api_usage_count = models.IntegerField(default=0)
    api_max_usage_count = models.IntegerField(default=20)
    api_reset_time = models.DateTimeField(default=timezone.now)
    
    def reset_api_usage(self):
        """ API使用回数をリセットするメソッド """
        self.api_usage_count = 0
        self.api_reset_time = timezone.now() + timedelta(days=1)  # 例えば、翌日にリセット
        self.save()
        
    def can_use_api(self):
        """ APIを使用できるかをチェックするメソッド """
        return self.api_usage_count < self.api_max_usage_count


    # 指定された画像フィールドのURLを返すメソッド
    def get_body_image_url(self):
        return self.body_image.url if self.body_image else '/static/images/body.png'

    def get_closed_eyes_image_url(self):
        return self.closed_eyes_image.url if self.closed_eyes_image else '/static/images/eyes_close.png'

    def get_open_eyes_image_url(self):
        return self.open_eyes_image.url if self.open_eyes_image else '/static/images/eyes.png'

    def get_open_mouth_image_url(self):
        return self.open_mouth_image.url if self.open_mouth_image else '/static/images/mouth_open.png'

    def get_half_open_mouth_image_url(self):
        return self.half_open_mouth_image.url if self.half_open_mouth_image else '/static/images/mouth_half.png'

    def get_closed_mouth_image_url(self):
        return self.closed_mouth_image.url if self.closed_mouth_image else '/static/images/mouth_close.png'

    def get_background_image_url(self):
        return self.background_image.url if self.background_image else None
    
# 支払い状況を追跡するモデル
class PaymentStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    

# ユーザーが作成されたとき、対応するキャラクターも自動的に作成
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_character(sender, instance, created, **kwargs):
    if created:
        Character.objects.create(user=instance)
    else:
        # instanceに関連付けられたCharacterインスタンスを取得または作成
        character, created = Character.objects.get_or_create(user=instance)

        # 必要に応じてcharacterの属性を更新
        character.save()
# ユーザーのメール確認用トークンモデル
class EmailConfirmationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    new_email = models.EmailField(null=True)  # 新しいメールアドレス用のフィールド
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"
    
    

