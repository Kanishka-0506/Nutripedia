function toggleTheme() {
  const body = document.body;
  const btn = document.getElementById('toggle');
  const currentTheme = body.dataset.theme || 'light';

  if (currentTheme === 'light') {
    body.dataset.theme = 'dark';
    body.classList.add('dark-mode');
    btn.textContent = '🌙';
  } else {
    body.dataset.theme = 'light';
    body.classList.remove('dark-mode');
    btn.textContent = '🌞';
  }
}
