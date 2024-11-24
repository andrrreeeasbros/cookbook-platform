window.addEventListener('DOMContentLoaded', function () {
    const categories = document.querySelectorAll('.category-item');
    let delay = 0;
  
    categories.forEach((category, index) => {
      setTimeout(() => {
        category.classList.add('visible');
      }, delay);
      delay += 500; // Каждая категория будет появляться с задержкой в 500 мс
    });
  });
  