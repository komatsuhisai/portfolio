// eyes_animation.js

document.addEventListener('DOMContentLoaded', function() {
  try {
    const eyeImage = document.getElementById('eye-image');
    if (!eyeImage) {
      console.error('eyeImage 要素が見つかりません。');
      return;
    }

    // window.staticFilePaths オブジェクトから画像のURLを取得する
    const eyesOpen = window.staticFilePaths.eyesOpen;
    const eyesClosed = window.staticFilePaths.eyesClosed;

    eyeImage.src = eyesOpen; // 初期状態として開いた目の画像を設定

    // ランダムな間隔で目パチアニメーションを制御する関数
    function startEyeBlinking() {
      const minBlinkInterval = 200; // 最短で2秒後に点滅
      const maxBlinkInterval = 5000; // 最長で10秒後に点滅
      const closeDuration = 200; // 目を閉じるのは200ミリ秒間

      function blink() {
        eyeImage.src = eyesClosed; // 目を閉じる

        setTimeout(() => {
          eyeImage.src = eyesOpen; // 目を開く
          scheduleNextBlink(); // 次の点滅までの間隔をランダムに設定
        }, closeDuration);
      }

      function scheduleNextBlink() {
        const randomInterval = Math.random() * (maxBlinkInterval - minBlinkInterval) + minBlinkInterval;
        setTimeout(blink, randomInterval);
      }

      scheduleNextBlink(); // 初回の点滅をスケジュール
    }

    startEyeBlinking();
  } catch (error) {
    console.error('目パチアニメーションのスクリプトでエラーが発生しました:', error);
  }
});

