// Wait until the DOM is fully loaded
window.addEventListener('DOMContentLoaded', (event) => {
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('password');
  const visibilityOn = document.getElementById('visibilityOn');
  const visibilityOff = document.getElementById('visibilityOff');

  // Default: show 'visibilityOff' (password hidden), hide 'visibilityOn'
  visibilityOn.style.display = 'none';
  visibilityOff.style.display = 'inline';

  togglePassword.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);

    if (type === 'text') {
      visibilityOn.style.display = 'inline';
      visibilityOff.style.display = 'none';
    } else {
      visibilityOn.style.display = 'none';
      visibilityOff.style.display = 'inline';
    }
  });
});
