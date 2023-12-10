// エラーメッセージを表示する関数
export function showErrorMessage(message) {
    const errorMessageContainer = document.getElementById('error-message-container');
    errorMessageContainer.textContent = message;
    errorMessageContainer.style.display = 'block';
}

// エラーメッセージをクリアする関数
export function clearErrorMessage() {
    const errorMessageContainer = document.getElementById('error-message-container');
    errorMessageContainer.textContent = '';
    errorMessageContainer.style.display = 'none';
}
