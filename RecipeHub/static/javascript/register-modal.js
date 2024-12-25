document.addEventListener('DOMContentLoaded', function () {
  const registerModal = document.getElementById('registerModal');
  const openRegisterModalBtn = document.getElementById('openRegisterModal');
  const closeRegisterModalBtn = document.getElementById('closeRegisterModal');
  const closeRegisterModalFooterBtn = document.getElementById('closeRegisterModalFooter');

  function openModal(modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeModal(modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }

  openRegisterModalBtn.addEventListener('click', function () {
    openModal(registerModal);
  });

  closeRegisterModalBtn.addEventListener('click', function () {
    closeModal(registerModal);
  });

  closeRegisterModalFooterBtn.addEventListener('click', function () {
    closeModal(registerModal);
  });

  window.addEventListener('click', function (event) {
    if (event.target === registerModal) {
      closeModal(registerModal);
    }
  });
});
