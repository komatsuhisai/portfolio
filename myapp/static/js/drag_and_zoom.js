// ドラッグ機能
function dragElement(element) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  element.onmousedown = dragMouseDown;

  function dragMouseDown(e) {
    e.preventDefault();
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e.preventDefault();
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    element.style.top = (element.offsetTop - pos2) + "px";
    element.style.left = (element.offsetLeft - pos1) + "px";
    
    // ドラッグ中に位置を保存
    saveCharacterPosition(element.style.left, element.style.top);
  }

  function closeDragElement() {
    document.onmouseup = null;
    document.onmousemove = null;
  }
}

// ズーム機能
function zoomElement(element) {
  var scale = 1;
  var zoomSensitivity = 0.001;

  element.onwheel = function(event) {
    event.preventDefault();
    scale += event.deltaY * -zoomSensitivity;
    scale = Math.min(Math.max(.125, scale), 4);
    element.style.transform = 'scale(' + scale + ')';
    
    // ズーム中に位置とズームを保存
    saveCharacterPosition(element.style.left, element.style.top);
    saveCharacterZoom(scale);
  };
}

// 位置をローカルストレージに保存
function saveCharacterPosition(left, top) {
  localStorage.setItem('characterPosition', JSON.stringify({ left: left, top: top }));
}

// ズームをローカルストレージに保存
function saveCharacterZoom(scale) {
  localStorage.setItem('characterZoom', scale.toString());
}

// 要素にドラッグとズーム機能を適用
var character = document.getElementById("character");
dragElement(character);
zoomElement(character);

// ページ読み込み時に要素の位置とズームを復元
document.addEventListener('DOMContentLoaded', function() {
  var savedPosition = localStorage.getItem('characterPosition');
  if (savedPosition) {
    var position = JSON.parse(savedPosition);
    character.style.left = position.left;
    character.style.top = position.top;
  }

  var savedZoom = localStorage.getItem('characterZoom');
  if (savedZoom) {
    var zoom = parseFloat(savedZoom);
    character.style.transform = 'scale(' + zoom + ')';
  }
});


function dragElementMobile(element) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

  // 要素の position スタイルを absolute に設定
  element.style.position = 'absolute';

  element.ontouchstart = function(e) {
    e.preventDefault();
    pos3 = e.touches[0].clientX;
    pos4 = e.touches[0].clientY;
    document.ontouchend = closeDragElementMobile;
    document.ontouchmove = elementDragMobile;
  };

  function elementDragMobile(e) {
    e.preventDefault();

    // ビューポートに対する要素の現在位置を取得
    var rect = element.getBoundingClientRect();

    pos1 = pos3 - e.touches[0].clientX;
    pos2 = pos4 - e.touches[0].clientY;
    pos3 = e.touches[0].clientX;
    pos4 = e.touches[0].clientY;

    // 要素の新しい位置を設定
    element.style.top = (rect.top - pos2) + "px";
    element.style.left = (rect.left - pos1) + "px";
    saveCharacterPosition(element.style.left, element.style.top);
  }

  function closeDragElementMobile() {
    document.ontouchend = null;
    document.ontouchmove = null;
  }
}

// 画面幅が600px以下の場合にモバイル用ドラッグ機能を適用
if (window.innerWidth <= 600) {
  dragElementMobile(character);
} else {
  dragElement(character);
}


// 位置とズームをローカルストレージに保存する関数にエラーハンドリングを追加
function safeLocalStorageSetItem(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch (error) {
    console.error("ローカルストレージへの保存エラー:", error);
  }
}

// 上記の関数を使用して位置とズームを保存
function saveCharacterPosition(left, top) {
  safeLocalStorageSetItem('characterPosition', JSON.stringify({ left: left, top: top }));
}

function saveCharacterZoom(scale) {
  safeLocalStorageSetItem('characterZoom', scale.toString());
}

// 画面幅に応じて適切なドラッグ機能を適用する関数
function applyDragFunction() {
  if (window.innerWidth <= 600) {
    dragElementMobile(character);
  } else {
    dragElement(character);
  }
}

// ウィンドウリサイズ時にドラッグ機能を再適用
window.onresize = applyDragFunction;

// ページ読み込み時に適切なドラッグ機能を適用
applyDragFunction();