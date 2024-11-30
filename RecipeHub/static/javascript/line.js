document.addEventListener('DOMContentLoaded', function() {
    // Создаём линию с использованием line.js
    const line = new Line('.line-animation', {
      path: [
        { x: 0, y: 0 }, // Начальная точка
        { x: 100, y: 0 } // Конечная точка (линия будет двигаться по оси X слева направо)
      ],
      duration: 1000, // Длительность анимации в миллисекундах
      easing: 'ease-out' // Тип анимации
    });
    line.play(); // Запуск анимации
  });