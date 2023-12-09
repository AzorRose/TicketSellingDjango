// Получаем элементы 
const city = document.querySelector('.selected-city');
const popup = document.querySelector('.popup');

// Показываем popup
function showPopup() {
  popup.style.display = 'block';
}

// Скрываем popup
function hidePopup(event) {

  // Проверяем, что событие произошло на popup
  if (!event.target.classList.contains('popup')) return;

  // Останавливаем всплытие события
  event.stopPropagation();

  // Скрываем popup
  popup.style.display = 'none';
  
}

// Вешаем обработчики
city.onmouseover = showPopup;
popup.onmouseout = hidePopup;
