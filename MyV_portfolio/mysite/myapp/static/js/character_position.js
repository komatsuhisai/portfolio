//character_position.js
document.addEventListener('DOMContentLoaded', (event) => {
    const character = document.getElementById('character');
  
    // キャラクターの位置をロード
    const savedPosition = localStorage.getItem('characterPosition');
    if (savedPosition) {
      const position = JSON.parse(savedPosition);
      character.style.left = position.left;
      character.style.top = position.top;
    }
  
    // キャラクターの位置を保存
    character.addEventListener('mouseup', () => {
      const position = { left: character.style.left, top: character.style.top };
      localStorage.setItem('characterPosition', JSON.stringify(position));
    });
  });
  