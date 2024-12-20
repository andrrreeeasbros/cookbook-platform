document.addEventListener("DOMContentLoaded", function() {
  // Получаем элементы для модального окна связи с командой
  const contactModal = document.getElementById("contactModal");
  const openContactModalBtn = document.getElementById("openContactModal");
  const closeContactModal = document.getElementById("closeContactModal");

  // Функция для открытия модального окна
  function openContactModal() {
    contactModal.style.display = "flex";
    history.pushState(null, null, window.location.href);  // Изменяем URL, но не перезагружаем страницу
  }

  // Функция для закрытия модального окна
  function closeContactModalWindow() {
    contactModal.style.display = "none";
    history.pushState(null, null, window.location.href.split('#')[0]);  // Возвращаем URL без хэша
  }

  // Открытие модального окна по нажатию на кнопку
  openContactModalBtn.addEventListener("click", openContactModal);

  // Закрытие модального окна по нажатию на кнопку "Закрыть"
  closeContactModal.addEventListener("click", closeContactModalWindow);

  // Закрытие модального окна при клике вне его
  window.addEventListener("click", function(event) {
    if (event.target === contactModal) {
      closeContactModalWindow();
    }
  });
});
