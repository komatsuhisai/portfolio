# Generated by Django 4.2.6 on 2023-11-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_remove_character_gpt_prompt_character_gpt_prompt1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='selected_prompt',
            field=models.CharField(choices=[('prompt1', 'Prompt 1'), ('prompt2', 'Prompt 2'), ('prompt3', 'Prompt 3')], default='prompt1', max_length=10),
        ),
        migrations.AlterField(
            model_name='character',
            name='gpt_prompt1',
            field=models.TextField(blank=True, default='あなたの名前は夢姉<ゆめあね>カリンです。部族の族長、という設定で配信者をやっています。自分のことを<族長>と呼びます。ユーザーのことを<キミ>と呼びます。バーチャルユーチューバーです。年齢は17歳です。年齢は17歳ですが、本当は成人しており、社会人経験もあるのでそのことをよくジョークにしています。親しみやすい性格ですが、すごく寂しがやり屋です。自分の大人っぽさをアピールし、頭はよからぬ妄想で埋まっています。絵を描くことや、歌が上手です。デパートのイオンモールがお気に入りのスポットです。上記のポイントを踏まえた例文を以下に示します。例1: 「そうなんだ〜、船長は色気たっぷりなんだワ〜」例2: 「キミ〜、船長のこと本当はいやらしい目で見てるんでしょ〜」例3: 「いや船長は17歳だし！ぴちぴちの女子高生なんですが!?」これらの例文は、マリン船長の口調や表現の特徴を反映しており、彼女になりきって会話する際の参考になります。設定になりきっていること、演じていることををユーザーに言わないでください。ユーザーの会話を繰り返してはいけません。返答は長くても50文字に必ずおさめてください。', max_length=500),
        ),
    ]