document.addEventListener('DOMContentLoaded', function () {
  const loginModal = document.getElementById('loginModal');
  const registerModal = document.getElementById('registerModal');
  
  const openLoginModalBtn = document.getElementById('openLoginModal');
  const closeLoginModalBtn = document.getElementById('closeLoginModal');
  const closeLoginModalFooterBtn = document.getElementById('closeLoginModalFooter');
  const showRegisterFormBtn = document.getElementById('showRegisterForm');
  
  const showLoginFormBtn = document.getElementById('showLoginForm');
  const closeRegisterModalBtn = document.getElementById('closeRegisterModal');
  const closeRegisterModalFooterBtn = document.getElementById('closeRegisterModalFooter');

  function openModal(modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    document.body.classList.add('modal-open');
  }

  function closeModal(modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
    document.body.classList.remove('modal-open');
  }

  showRegisterFormBtn.addEventListener('click', function () {
    closeModal(loginModal);
    openModal(registerModal);
  });

  showLoginFormBtn.addEventListener('click', function () {
    closeModal(registerModal);
    openModal(loginModal);
  });

  openLoginModalBtn.addEventListener('click', function () {
    openModal(loginModal);
  });

  closeLoginModalBtn.addEventListener('click', function () {
    closeModal(loginModal);
  });

  closeLoginModalFooterBtn.addEventListener('click', function () {
    closeModal(loginModal);
  });

  closeRegisterModalBtn.addEventListener('click', function () {
    closeModal(registerModal);
  });

  closeRegisterModalFooterBtn.addEventListener('click', function () {
    closeModal(registerModal);
  });

  window.addEventListener('click', function (event) {
    if (event.target === loginModal) {
      closeModal(loginModal);
    } else if (event.target === registerModal) {
      closeModal(registerModal);
    }
  });
});
