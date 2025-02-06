// chat.js
import { appendMessage } from './chat_message.js';
import { addAudioElement, setAudioEnabled, setVolume } from './audio_controls.js';

document.addEventListener('DOMContentLoaded', function() {
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('text_input');
  const mouthImageOpen = document.getElementById('mouth-image-open-user') || document.getElementById('mouth-image-open');
  const mouthImageHalf = document.getElementById('mouth-image-half-user') || document.getElementById('mouth-image-half');
  const mouthImageClose = document.getElementById('mouth-image-user') || document.getElementById('mouth-image');

  // 口パクアニメーションを制御する関数
  function startLipSync() {
    const mouthStates = ['close', 'half', 'open', 'half', 'close'];
    let index = 0;
    const interval = 100;

    const intervalId = setInterval(() => {
      const currentState = mouthStates[index];
      if (currentState === 'open' && mouthImageOpen) {
        mouthImageOpen.style.display = 'block';
        mouthImageHalf.style.display = 'none';
        mouthImageClose.style.display = 'none';
      } else if (currentState === 'half' && mouthImageHalf) {
        mouthImageOpen.style.display = 'none';
        mouthImageHalf.style.display = 'block';
        mouthImageClose.style.display = 'none';
      } else if (currentState === 'close' && mouthImageClose) {
        mouthImageOpen.style.display = 'none';
        mouthImageHalf.style.display = 'none';
        mouthImageClose.style.display = 'block';
      }
      index = (index + 1) % mouthStates.length;
    }, interval);

    return () => {
      clearInterval(intervalId);
      if (mouthImageClose) mouthImageClose.style.display = 'block';
      if (mouthImageOpen) mouthImageOpen.style.display = 'none';
      if (mouthImageHalf) mouthImageHalf.style.display = 'none';
    };
  }

  // オーディオを再生する関数
  function playAudioFromBase64(base64String) {
    const audioSrc = 'data:audio/wav;base64,' + base64String;
    const audio = new Audio(audioSrc);

    let stopAnimation = startLipSync();
    setMouthZIndex(11); // 高いz-indexに設定

    addAudioElement(audio);

    audio.play().then(() => {
      // 再生が開始されたときの処理
    }).catch(e => {
      console.error('オーディオ再生に失敗しました:', e);
      if (stopAnimation) stopAnimation();
      setMouthZIndex(9); // 元のz-indexに戻す
    });

    audio.onended = () => {
      if (stopAnimation) stopAnimation();
      setMouthZIndex(9); // 元のz-indexに戻す
    };
  }

  // z-indexを設定する関数
  function setMouthZIndex(zIndex) {
    if (mouthImageOpen) mouthImageOpen.style.zIndex = zIndex;
    if (mouthImageHalf) mouthImageHalf.style.zIndex = zIndex;
    if (mouthImageClose) mouthImageClose.style.zIndex = zIndex;
  }

  









// チャットフォームの送信処理
// チャットフォームの送信処理
chatForm.onsubmit = function(e) {
  e.preventDefault(); // デフォルトのフォーム送信を防止
  const userInput = chatInput.value.trim(); // 入力値の前後の空白を削除

  // 文字数制限のチェック
  if (userInput.length > 50) {
    alert('メッセージは50文字以内で入力してください。');
    return; // ここで処理を終了
  }

  chatInput.value = ''; // チャット入力欄をクリア

  fetch('/myapp/chat-response/', {
    method: 'POST',
    body: JSON.stringify({ text_input: userInput }),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('会話回数の上限に達しました。プランを購入してください。');
    }
    return response.json();
  })
  .then(data => {
    if (data.error) {
      // API使用制限等のエラーメッセージを表示
      alert(data.error);
    } else {
      // 正常にメッセージやオーディオが取得できた場合の処理
      if (data.text) {
        appendMessage('User: ' + userInput, true);
        appendMessage('Bot: ' + data.text, false);
      }
      if (data.audio_base64) {
        playAudioFromBase64(data.audio_base64);
      }
      if (data.apiUsageCount >= data.apiMaxUsageCount) {
        // API使用回数の制限に達した場合のアラート
        alert("会話の上限に達しました。続けるには課金が必要です。");
      }
    }
  })
  .catch(error => {
    console.error('エラーが発生しました:', error.message);
    alert(error.message);
  });
};

function getCookie(name) {
  // 省略（既存のgetCookie関数のコード）
}








  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
