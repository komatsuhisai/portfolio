// mouth_animation.js

(function() {
  // デフォルトとユーザーがアップロードした画像の要素を取得
  const defaultMouthOpenElement = document.getElementById('mouth-image-open');
  const userMouthOpenElement = document.getElementById('mouth-image-open-user');
  const defaultMouthHalfOpenElement = document.getElementById('mouth-image-half');
  const userMouthHalfOpenElement = document.getElementById('mouth-image-half-user');
  const defaultMouthCloseElement = document.getElementById('mouth-image');
  const userMouthCloseElement = document.getElementById('mouth-image-user');

  // デフォルトまたはユーザーがアップロードした要素を選択する関数
  function selectElement(defaultElement, userElement) {
    return userElement || defaultElement;
  }

  const mouthOpenElement = selectElement(defaultMouthOpenElement, userMouthOpenElement);
  const mouthHalfOpenElement = selectElement(defaultMouthHalfOpenElement, userMouthHalfOpenElement);
  const mouthCloseElement = selectElement(defaultMouthCloseElement, userMouthCloseElement);

  const originalPlayAudioFromBase64 = window.playAudioFromBase64;

  window.playAudioFromBase64 = function(base64String) {
    if (!isUserLoggedIn) return; // ユーザーがログインしていない場合は何もしない

    originalPlayAudioFromBase64(base64String);
    startMouthAnimation();
  };

  function startMouthAnimation() {
    const animationInterval = 100; // 開閉の間隔を短くする
    const animationDuration = 5000; // 合計持続時間

    let startTime = Date.now();
    let mouthState = 0; // 0: close, 1: half-open, 2: open

    function toggleMouth() {
      const currentTime = Date.now();
      if (currentTime - startTime < animationDuration) {
        switch (mouthState) {
          case 0:
            if (mouthOpenElement) mouthOpenElement.style.display = 'none';
            if (mouthHalfOpenElement) mouthHalfOpenElement.style.display = 'block';
            if (mouthCloseElement) mouthCloseElement.style.display = 'none';
            mouthState = 1;
            break;
          case 1:
            if (mouthOpenElement) mouthOpenElement.style.display = 'block';
            if (mouthHalfOpenElement) mouthHalfOpenElement.style.display = 'none';
            if (mouthCloseElement) mouthCloseElement.style.display = 'none';
            mouthState = 2;
            break;
          case 2:
            if (mouthOpenElement) mouthOpenElement.style.display = 'none';
            if (mouthHalfOpenElement) mouthHalfOpenElement.style.display = 'block';
            if (mouthCloseElement) mouthCloseElement.style.display = 'none';
            mouthState = 1;
            break;
        }
        setTimeout(toggleMouth, animationInterval);
      } else {
        if (mouthOpenElement) mouthOpenElement.style.display = 'none';
        if (mouthHalfOpenElement) mouthHalfOpenElement.style.display = 'none';
        if (mouthCloseElement) mouthCloseElement.style.display = 'block';
      }
    }

    toggleMouth(); // 口パクアニメーションを開始
  }
})();
