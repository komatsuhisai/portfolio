// ローディングアイコンを取得
const loader = document.querySelector('.loader');

// チャットエリアを監視するためのオブザーバーを設定
const chatArea = document.querySelector('#message-container');
const observer = new MutationObserver(mutations => {
  mutations.forEach(mutation => {
    if (mutation.type === 'childList') {
      // メッセージが追加されたので、ローダーを非表示にする
      loader.style.display = 'none';
    }
  });
});

// オブザーバーの設定を指定
const config = { childList: true };

// チャットエリアにオブザーバーを適用
observer.observe(chatArea, config);

// チャットフォームの送信イベントハンドラを追加
const chatForm = document.getElementById('chat-form');

chatForm.addEventListener('submit', () => {
  // フォームが送信されたので、ローダーを表示
  loader.style.display = 'block';
});
