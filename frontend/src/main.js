import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

async function initApp() {
  try {
    const res = await fetch('/api/method/employee_management.api.get_csrf_token');
    if (res.ok) window.csrf_token = (await res.json()).message;
  } catch (e) {
    console.error("Failed to fetch CSRF token", e);
  }

  const { fetch: originalFetch } = window;
  window.fetch = async (resource, config = {}) => {
    config.headers = { ...config.headers };
    if (window.csrf_token && window.csrf_token !== '{{ csrf_token }}') {
      config.headers['X-Frappe-CSRF-Token'] = window.csrf_token;
    }
    return originalFetch(resource, config);
  };

  createApp(App).mount('#app');
}

initApp();
