// api_usage.js

document.addEventListener('DOMContentLoaded', function() {
    // HTMLからAPI使用回数と最大使用回数を取得
    const apiUsageCount = parseInt(document.getElementById('api-usage-count').textContent, 10);
    const apiMaxUsageCount = parseInt(document.getElementById('api-max-usage-count').textContent, 10);

    // API使用回数が最大使用回数に達しているかチェック
    function checkApiUsageAndPromptForPayment() {
        if (apiUsageCount >= apiMaxUsageCount) {
            alert("会話の上限に達しました。続けるには課金が必要です。");
            // ここで課金ページへのリダイレクトや、課金を促すモーダルウィンドウを表示する処理を追加できます
            return true;
        }
        return false;
    }

    // ページ読み込み時にチェックを実行
    checkApiUsageAndPromptForPayment();
});
