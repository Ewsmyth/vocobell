const toggleButton = document.getElementById('toggleButton');
const slideDiv = document.getElementById('slideDiv');
const closeButton = document.getElementById('closeButton');
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('soundFileInput');
const uploadBoxContent = document.getElementById('uploadBoxContent');

toggleButton.addEventListener('click', () => {
  slideDiv.classList.toggle('active');
});

closeButton.addEventListener('click', () => {
  slideDiv.classList.remove('active');
});

// Handles the click to open the picker
uploadBox.addEventListener('click', () => fileInput.click());

// Handles file selection
fileInput.addEventListener('change', (e) => {
  handleFiles(e.target.files);
});

// Handles drag events
uploadBox.addEventListener('dragover', (e) => {
  e.preventDefault();
  uploadBox.classList.add('dragover');
});
uploadBox.addEventListener('dragleave', () => {
  uploadBox.classList.remove('dragover');
});
uploadBox.addEventListener('drop', (e) => {
  e.preventDefault();
  uploadBox.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
});
function handleFiles(files) {
  if (files.length > 0) {
    const file = files[0];
    const fileName = file.name;
    const fileType = file.type || 'unknown';

    // Update the upload box content
    uploadBoxContent.innerHTML = `
      <p><strong>Selected File:</strong></p>
      <p>${fileName}</p>
      <p>(${fileType})</p>
    `;

    // Also assign dropped files to the hidden input (important for form submission)
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;
  }
}

// Audio playback logic
document.querySelectorAll('.play-button').forEach(button => {
  button.addEventListener('click', () => {
    const filename = button.getAttribute('data-filename');
    const audioPlayer = document.getElementById('audioPlayer');
    audioPlayer.src = `/static/sounds/${filename}`;
    audioPlayer.style.display = 'block';
    audioPlayer.play();
  });
});
