const toggleBtn = document.getElementById('toggleBtn');
const sidebar = document.getElementById('sidebar');
const chevronLeft = document.getElementById('chevronLeft');
const chevronRight = document.getElementById('chevronRight');

// Set correct chevron on load
function updateChevron() {
  if (sidebar.classList.contains('collapsed')) {
    chevronLeft.style.display = 'none';
    chevronRight.style.display = 'block';
  } else {
    chevronLeft.style.display = 'block';
    chevronRight.style.display = 'none';
  }
}

// Handle initial state (already applied by inline script)
document.addEventListener('DOMContentLoaded', () => {
  if (document.documentElement.classList.contains('sidebar-collapsed')) {
    sidebar.classList.add('collapsed');
  }
  updateChevron();
});

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('collapsed');
  const isCollapsed = sidebar.classList.contains('collapsed');
  
  if (isCollapsed) {
    document.documentElement.classList.add('sidebar-collapsed');
  } else {
    document.documentElement.classList.remove('sidebar-collapsed');
  }
  
  localStorage.setItem('sidebar-collapsed', isCollapsed);
  updateChevron();
});
