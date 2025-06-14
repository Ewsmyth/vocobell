const toggleButton = document.getElementById('toggleButton');
const slideDiv = document.getElementById('slideDiv');
const closeButton = document.getElementById('closeButton');

toggleButton.addEventListener('click', () => {
  slideDiv.classList.toggle('active');
});

closeButton.addEventListener('click', () => {
  slideDiv.classList.remove('active');
});

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.copy-btn').forEach(button => {
    button.addEventListener('click', () => {
      const url = button.getAttribute('data-url');
      console.log("URL to copy:", url);  // Debug log
      navigator.clipboard.writeText(url).then(() => {
        button.innerText = "Copied!";
        setTimeout(() => button.innerText = "Copy", 2000);
      }).catch(err => {
        console.error('Failed to copy webhook: ', err);
      });
    });
  });
});
