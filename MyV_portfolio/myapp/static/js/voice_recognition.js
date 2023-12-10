// voice_recognition.js

// マイクの状態を追跡する変数をグローバルスコープで宣言
let isMicActive = false;

// 音声認識オブジェクトを格納する変数をグローバルスコープで宣言
let recognition = null;

// エラーメッセージを表示する関数
function showErrorMessage(message) {
    const errorMessageContainer = document.getElementById('error-message-container');
    errorMessageContainer.textContent = message;
    errorMessageContainer.style.display = 'block';
}

// エラーメッセージをクリアする関数
function clearErrorMessage() {
    const errorMessageContainer = document.getElementById('error-message-container');
    errorMessageContainer.textContent = '';
    errorMessageContainer.style.display = 'none';
}

// マイクボタンの状態を更新する関数
function updateMicButtonState(active) {
    const micButton = document.getElementById('mic-button');
    isMicActive = active;
    micButton.classList.toggle('active', active);
    micButton.innerHTML = active ? '<i class="fas fa-microphone"></i>' : '<i class="fas fa-microphone-slash"></i>';
    // console.log('Updating mic button state:', active);
}

// 音声認識を停止する関数
function stopRecognition() {
    if (recognition) {
        recognition.stop();
        console.log('Recognition stopped');
    }
    updateMicButtonState(false);
    clearErrorMessage();
}

// 音声認識を開始する関数
function startRecognition() {
    if (!recognition) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.lang = 'ja-JP';
            recognition.continuous = true;
            recognition.interimResults = true;
            
            recognition.onstart = function() {
                console.log('Recognition started');
                updateMicButtonState(true);
            };

            recognition.onresult = function(event) {
                console.log('Recognition result received');
                const transcript = Array.from(event.results)
                    .map(result => result[0])
                    .map(result => result.transcript)
                    .join('');
                document.getElementById('text_input').value = transcript;
            };

            recognition.onerror = function(event) {
                console.error('Recognition error:', event.error);
                let errorMessage = '音声認識にエラーが発生しました。';
                if (event.error === 'no-speech') {
                    errorMessage = '音声が検出されませんでした。もう一度試してください。';
                }
                showErrorMessage(errorMessage);
                stopRecognition();
            };

            recognition.onend = function() {
                console.log('Recognition ended');
                stopRecognition();
            };
        } else {
            console.error("このブラウザは音声認識をサポートしていません。");
            return;
        }
    }

    if (!isMicActive) {
        recognition.start();
    }
}

// ドキュメントが読み込まれたときの処理
document.addEventListener('DOMContentLoaded', function() {
    const micButton = document.getElementById('mic-button');

    micButton.addEventListener('click', function() {
        if (isMicActive) {
            stopRecognition();
        } else {
            startRecognition();
        }
    });

    updateMicButtonState(isMicActive);
});
