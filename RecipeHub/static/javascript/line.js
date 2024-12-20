document.addEventListener('DOMContentLoaded', function() {
    const line = new Line('.line-animation', {
      path: [
        { x: 0, y: 0 }, 
        { x: 100, y: 0 } 
      ],
      duration: 1000,
      easing: 'ease-out' 
    });
    line.play(); 
  });