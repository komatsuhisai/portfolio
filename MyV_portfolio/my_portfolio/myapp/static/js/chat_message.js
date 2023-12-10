//chat_message.js

export function appendMessage(message, isUser){
    // 新しいメッセージ要素を作成する
    var newMessageElement = document.createElement('div');
  
    // メッセージの種類に応じてクラスを設定する
    newMessageElement.className = isUser ? 'message user-message' : 'message bot-message';
  
    // メッセージ要素にテキスト内容を設定する
    newMessageElement.textContent = message;
  
    // メッセージを追加するためのコンテナ要素を選択する
    var messageContainer = document.getElementById('message-container');
  
    // コンテナに新しいメッセージ要素を追加する
    messageContainer.appendChild(newMessageElement);
    
    // スクロールを最新のメッセージに合わせる
    messageContainer.scrollTop = messageContainer.scrollHeight;
  }
  
  // 使用例:
  // ユーザーのメッセージを追加
  // appendMessage('こんにちは、チャットボットさん！', true);
  
  // ボットのメッセージを追加
  // appendMessage('何か手伝えることはありますか？', false);
  