document.addEventListener("DOMContentLoaded", function() {
  // Получаем элементы для модального окна регистрации
  const modal = document.getElementById("modal");
  const openModalBtn = document.getElementById("openModalBtn");
  const closeModal = document.getElementById("closeModal");

  // Функция для открытия модального окна
  function openModal() {
    modal.style.display = "flex";
    history.pushState(null, null, window.location.href);  // Изменяем URL, но не перезагружаем страницу
  }

  // Функция для закрытия модального окна
  function closeModalWindow() {
    modal.style.display = "none";
    history.pushState(null, null, window.location.href.split('#')[0]);  // Возвращаем URL без хэша
  }

  // Открытие модального окна по нажатию на кнопку
  openModalBtn.addEventListener("click", openModal);

  // Закрытие модального окна по нажатию на кнопку "Закрыть"
  closeModal.addEventListener("click", closeModalWindow);

  // Закрытие модального окна при клике вне его
  window.addEventListener("click", function(event) {
    if (event.target === modal) {
      closeModalWindow();
    }
  });
});
