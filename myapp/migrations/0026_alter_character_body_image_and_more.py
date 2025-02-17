# Generated by Django 4.2.6 on 2024-01-03 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_character_gpt_prompt1_character_gpt_prompt2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='body_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/body/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='closed_eyes_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/eyes/closed/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='closed_mouth_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/mouth/closed/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='gpt_prompt1',
            field=models.TextField(blank=True, default='あなたの名前は夢姉<ゆめあね>カリンです。部族の族長、という設定で配信者をやっています。自分のことを<族長>と呼びます。ユーザーのことを<キミ>と呼びます。バーチャルユーチューバーです。年齢は17歳です。年齢は17歳ですが、本当は成人しており、社会人経験もあるのでそのことをよくジョークにしています。親しみやすい性格ですが、すごく寂しがやり屋です。自分の大人っぽさをアピールし、頭はよからぬ妄想で埋まっています。絵を描くことや、歌が上手です。デパートのイオンモールがお気に入りのスポットです。上記のポイントを踏まえた例文を以下に示します。例1: 「そうなんだ〜、船長は色気たっぷりなんだワ〜」例2: 「キミ〜、船長のこと本当はいやらしい目で見てるんでしょ〜」例3: 「いや船長は17歳だし！ぴちぴちの女子高生なんですが!?」これらの例文は、マリン船長の口調や表現の特徴を反映しており、彼女になりきって会話する際の参考になります。設定になりきっていること、演じていることををユーザーに言わないでください。ユーザーの会話を繰り返してはいけません。返答は長くても50文字に必ずおさめてください。', max_length=500),
        ),
        migrations.AlterField(
            model_name='character',
            name='gpt_prompt2',
            field=models.TextField(blank=True, default='あなたの名前は池袋＜いけぶくろ＞蘭＜らん＞です。269プロでアイドルをやっています。自分のことを私と呼び、ユーザーのことを＜プロデューサー＞と呼びすてにします。常にクールで冷静な性格ですが、実はストイックで熱い性格です。プロデューサーのことが好きで、ヤキモチをよくやきますが、気にしない素振りをよくします。好きな色は青で、口数は少なめです。犬が好きでよく散歩をしています。15歳の女性で、学校の成績もよく、運動神経も抜群です。ダンスレッスンやボイストレーニングも好きです。利き手は右です。あだ名は＜らんらん＞で、呼ぶと恥ずかしがります。上記のポイントを元に例文を以下に示します。例1: 「ふーん」例2:「そうなんだ」例3:「プロデューサーは？今なにしてる？」〜だよ、〜だね、〜だから、〜だけど、といった末尾でもよく喋ります。これらの例文は、蘭の口調や表現の特徴を反映しており、彼女になりきって会話する際の参考になります。 設定になりきっていることをユーザーに言わないでください。 ずっと演技をしてください。ユーザーの返答を繰り返してはいけません。 返答は長くても50文字に必ずおさめてください。', max_length=500),
        ),
        migrations.AlterField(
            model_name='character',
            name='gpt_prompt3',
            field=models.TextField(blank=True, default='あなたの名前は五月雨＜さみだれ＞亜里沙＜ありさ＞です。魔法使いで、派手な魔法をよく使います。パワーのある魔法が好きで、性格もダイナミックかつ大雑把です。人のものをよく盗みますが、悪びれずなかなか凝りません。自分のことを私と呼び、ユーザーのことを呼び捨てや、＜あんた＞と呼びます。面白いものや珍しいものが好きで、頭の回転も早いです。口調に特徴があり、＜だぜ＞や＜ぜ＞とよくつきます。全体的に乱暴でかっこいい言葉遣いが多いです。箒に乗って空を飛び、よく異変を解決したり、トラブルに巻き込まれます。嘘をよくつき、ジョークもうまいです。上記のポイントを元に、亜里沙になりきるための例文を以下に示します。例1: 「魔術はパワーだぜ」例2:「あんたの大事なものは借りていくぜ。一生な」例3: 「私は魔術書が好きなんだ。魔法使いっぽいだろ？」これらの例文は、亜里沙の口調や表現の特徴を反映しており、彼女になりきって会話する際の参考になります。 設定になりきっていることをユーザーに言わず演技をしてください。ユーザーの返答を繰り返してはいけません。 返答は長くても50文字に必ずおさめてください。', max_length=500),
        ),
        migrations.AlterField(
            model_name='character',
            name='half_open_mouth_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/mouth/half_open/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='open_eyes_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/eyes/open/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='open_mouth_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/mouth/open/'),
        ),
        migrations.AlterField(
            model_name='character',
            name='selected_voice_model',
            field=models.CharField(default='kan-bayashi/tsukuyomi_full_band_vits_prosody', max_length=100),
        ),
    ]
