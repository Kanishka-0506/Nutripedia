function toggleTheme() {
  const body = document.body;
  const btn = document.getElementById('toggle');
  const box = document.querySelector('.nutrition-data');
  const footer = document.querySelector('footer');
  const currentTheme = body.dataset.theme || 'light';

  if (currentTheme === 'light') {
    body.dataset.theme = 'dark';
    body.classList.add('bg-dark', 'text-white');
    box.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
    box.style.color = 'whitesmoke';
    footer.style.backgroundColor = '#1a1a1a';
    footer.style.color = 'whitesmoke';
    btn.textContent = '🌙';
  } else {
    body.dataset.theme = 'light';
    body.classList.remove('bg-dark', 'text-white');
    box.style.backgroundColor = '';
    box.style.color = '';
    footer.style.backgroundColor = '';
    footer.style.color = '';
    btn.textContent = '🌞';
  }
}
