document.addEventListener('DOMContentLoaded', function () {
  const fadeInElements = document.querySelectorAll('.fade-in');

  function checkVisibility() {
    const windowHeight = window.innerHeight;

    fadeInElements.forEach(element => {
      const elementTop = element.getBoundingClientRect().top;
      const elementVisible = 100;

      if (elementTop < windowHeight - elementVisible) {
        element.classList.add('visible');
      }
    });
  }

  checkVisibility();

  window.addEventListener('scroll', checkVisibility);
});
