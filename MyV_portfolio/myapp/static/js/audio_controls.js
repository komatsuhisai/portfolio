// audio_controls.js
let audioEnabled = true; // 音声が有効かどうかの状態
let currentVolume = 100; // 現在の音量（0から100の範囲）
const audioElements = []; // オーディオ要素の参照を保持する配列

// オーディオが有効かどうかを設定する関数
export function setAudioEnabled(enable) {
    audioEnabled = enable;
    audioElements.forEach(audio => {
        audio.muted = !enable;
    });
    // アイコンの状態を更新
    const audioToggleButton = document.querySelector('.toggle-audio');
    if (audioToggleButton) {
        audioToggleButton.innerHTML = enable ? '<i class="fas fa-volume-up"></i>' : '<i class="fas fa-volume-mute"></i>';
    }
}

// 音量を設定する関数
export function setVolume(volume) {
    currentVolume = volume;
    const volumeLevel = volume / 100;
    audioElements.forEach(audio => {
        audio.volume = volumeLevel;
    });

    // ボリュームをローカルストレージに保存
    localStorage.setItem('volume', volume);
}

// オーディオ要素を追加する関数
export function addAudioElement(audio) {
    audioElements.push(audio);
    audio.muted = !audioEnabled;
    audio.volume = currentVolume / 100;
}

// DOMが読み込まれた後にイベントリスナーを設定する
document.addEventListener('DOMContentLoaded', () => {
    const audioToggleButton = document.querySelector('.toggle-audio');
    const volumeSlider = document.querySelector('.volume-slider');

    // ローカルストレージからボリュームを読み込む
    const savedVolume = localStorage.getItem('volume');
    if (savedVolume !== null) {
        currentVolume = savedVolume;
        volumeSlider.value = savedVolume;
        setVolume(savedVolume); // スライダーとオーディオ要素の両方に適用
    }

    // オーディオトグルボタンのクリックイベント
    audioToggleButton.addEventListener('click', (event) => {
        event.preventDefault(); // デフォルトのフォーム送信をキャンセル
        setAudioEnabled(!audioEnabled);
    });

    // 音量スライダーの入力イベント
    if (volumeSlider) {
        volumeSlider.addEventListener('input', () => {
            setVolume(volumeSlider.value);
        });
    }
});

