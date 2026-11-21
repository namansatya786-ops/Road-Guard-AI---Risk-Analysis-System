const navItems = document.querySelectorAll('.nav-item[data-section]');
const title = document.getElementById('page-title');

navItems.forEach((item) => {
  item.addEventListener('click', () => {
    navItems.forEach((navItem) => navItem.classList.remove('active'));
    item.classList.add('active');
    title.textContent = item.dataset.section === 'Overview'
      ? 'System Overview'
      : item.dataset.section;
  });
});

const toast = document.getElementById('toast');
function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  window.setTimeout(() => toast.classList.remove('show'), 2200);
}

document.getElementById('analysis-button').addEventListener('click', () => {
  const modal = document.getElementById('analysis-modal');
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
});

document.querySelectorAll('[data-close-modal]').forEach((element) => {
  element.addEventListener('click', () => {
    const modal = document.getElementById('analysis-modal');
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      const modal = document.getElementById('analysis-modal');
      modal.classList.remove('open');
      modal.setAttribute('aria-hidden', 'true');
    }
  });
});

document.getElementById('analysis-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const submitButton = form.querySelector('[type="submit"]');
  const resultBox = document.getElementById('prediction-result');
  const payload = Object.fromEntries(new FormData(form).entries());
  payload.speed = Number(payload.speed);
  payload.visibility = Number(payload.visibility);

  submitButton.disabled = true;
  submitButton.textContent = 'Analyzing...';
  resultBox.hidden = true;

  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Analysis failed');

    resultBox.hidden = false;
    resultBox.className = `prediction-result risk-${data.risk_level.toLowerCase()}`;
    resultBox.textContent = `${data.risk_level} risk${data.confidence !== null ? ` · ${data.confidence}% confidence` : ''}`;
    document.getElementById('updated-time').textContent = 'Just now';
    showToast('Road risk analysis complete');
  } catch (error) {
    resultBox.hidden = false;
    resultBox.className = 'prediction-result risk-error';
    resultBox.textContent = error.message;
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'Analyze Risk';
  }
});

document.getElementById('risk-filter').addEventListener('click', (event) => {
  const button = event.currentTarget;
  button.firstChild.textContent = button.textContent.includes('All')
    ? 'Critical only '
    : 'All Severity ';
});

document.getElementById('period-button').addEventListener('click', (event) => {
  const button = event.currentTarget;
  button.firstChild.textContent = button.textContent.includes('7')
    ? 'Last 30 days '
    : 'Last 7 days ';
});

document.querySelectorAll('.alert-item').forEach((alert) => {
  alert.addEventListener('click', () => showToast(`${alert.dataset.risk} alert details opened`));
});

document.querySelectorAll('.recommendation button').forEach((button) => {
  button.addEventListener('click', () => showToast('Recommendation opened'));
});

document.getElementById('view-all').addEventListener('click', () => showToast('Showing all active alerts'));

let zoom = 1;
const map = document.getElementById('risk-map');
document.getElementById('zoom-in').addEventListener('click', () => {
  zoom = Math.min(1.25, zoom + .05);
  map.querySelector('.map-svg').style.transform = `scale(${zoom})`;
});
document.getElementById('zoom-out').addEventListener('click', () => {
  zoom = Math.max(.95, zoom - .05);
  map.querySelector('.map-svg').style.transform = `scale(${zoom})`;
});
