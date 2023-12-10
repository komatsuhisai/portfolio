//drag_and_zooom.js

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
      // ズームの最小値と最大値を設定
      scale = Math.min(Math.max(.125, scale), 4);
      element.style.transform = 'scale(' + scale + ')';
    };
  }
  
  // 要素にドラッグとズーム機能を適用
  var character = document.getElementById("character");
  dragElement(character);
  zoomElement(character);
  