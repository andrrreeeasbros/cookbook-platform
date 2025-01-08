document.addEventListener("DOMContentLoaded", function() {
  const contactModal = document.getElementById("contactModal");
  const openContactModalBtn = document.getElementById("openContactModal");
  const closeContactModal = document.getElementById("closeContactModal");

  function openContactModal() {
    contactModal.style.display = "flex";
    history.pushState(null, null, window.location.href);
  }

  function closeContactModalWindow() {
    contactModal.style.display = "none";
    history.pushState(null, null, window.location.href.split('#')[0]);
  }

  openContactModalBtn.addEventListener("click", openContactModal);
  closeContactModal.addEventListener("click", closeContactModalWindow);

  window.addEventListener("click", function(event) {
    if (event.target === contactModal) {
      closeContactModalWindow();
    }
  });
});
