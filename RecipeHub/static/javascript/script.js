document.addEventListener('DOMContentLoaded', function () {
  // Ищем все элементы с классом fade-in
  const fadeInElements = document.querySelectorAll('.fade-in');

  // Функция для проверки видимости элемента
  function checkVisibility() {
    const windowHeight = window.innerHeight; // Высота окна браузера

    fadeInElements.forEach(element => {
      const elementTop = element.getBoundingClientRect().top; // Получаем расстояние до верхней границы элемента
      const elementVisible = 100; // Начало появления элемента (чем больше число, тем позже элемент появляется)

      // Если элемент виден (его верхняя граница находится в пределах окна)
      if (elementTop < windowHeight - elementVisible) {
        element.classList.add('visible'); // Добавляем класс для анимации
      }
    });
  }

  // Проверяем видимость элементов при загрузке страницы
  checkVisibility();

  // Проверяем видимость элементов при прокрутке
  window.addEventListener('scroll', checkVisibility);
});
