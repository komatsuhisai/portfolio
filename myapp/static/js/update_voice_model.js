// update_selected_model.js
// CSRFトークンを取得する関数
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

// 選択されたモデルを更新する関数
function updateSelectedModel(model) {
  console.log("Sending model update request:", model);

  fetch('/myapp/update_selected_model/', {
    method: 'POST',
    body: JSON.stringify({ selected_model: model }),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    }
  })
  .then(response => {
    console.log("Received response:", response);
    return response.json();
  })
  .then(data => {
    if (data.success) {
      console.log("Model updated successfully");
    } else {
      console.error("Error updating model:", data.error);
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// ボタンのイベントリスナー
document.getElementById('model1').addEventListener('click', function() {
  updateSelectedModel('kan-bayashi/jsut_full_band_vits_prosody');
});

document.getElementById('model2').addEventListener('click', function() {
  updateSelectedModel('kan-bayashi/tsukuyomi_full_band_vits_prosody');
});
