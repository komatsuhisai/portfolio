# 小松久威のポートフォリオ

## 『MyV』の説明
自分の好きなAIと会話して動かせるアプリ「MyV」のコードです。
MyVは、ユーザーがイラストをアップロードすることで自由にAIの見た目を変更、
プロンプトを変えることで性格、音声も複数から選ぶことができます。

詳しくはhome.htmlの説明をご覧ください（デザインはまだプロトタイプ段階です）。
https://github.com/komatsuhisai/portfolio/blob/main/MyV_portfolio/myapp/templates/home.html

## 主要な部分
ChatGPT関連のテキスト処理
https://github.com/komatsuhisai/portfolio/blob/main/MyV_portfolio/myapp/chatbot.py

tts関連の音声処理
https://github.com/komatsuhisai/portfolio/blob/main/MyV_portfolio/myapp/tts.py
https://github.com/komatsuhisai/portfolio/blob/main/MyV_portfolio/myapp/tts_service.py

## 最も苦労した部分
なんといってもユーザーからのinput（メッセージ入力）を、CahtGPTで処理し音声変換したのち、
レスポンスとしてクライアントに反映させた部分です。

## その他の説明
開発段階ではmanage.pyまでもうひとつ階層を挟んでいました（venvなど）。
ポートフォリオとしては乱雑と感じ、そのほか余計なファイルやディレクトリなども削除。
現在は.envを除けば主要なファイルは揃っている状態で、アプリとしての機能は完成済みです。

本来はデプロイ後に転職活動を行おうと思っていたのですが、
現在の職場でのスキルアップが飽和状態になっていることに大きな危機感を感じ、
やや急ぎ足気味ではありますが現在に至っています。

ここまでご覧いただきありがとうございました。
何卒よろしくお願い申し上げます。
