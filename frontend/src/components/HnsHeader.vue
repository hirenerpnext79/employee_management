<script setup>
import { ref, onMounted } from 'vue'
import HnsMenuItem from './HnsMenuItem.vue'

defineProps({
  currentRoute: String
})

const menuItems = ref([])

onMounted(async () => {
  try {
    const response = await fetch('/api/method/web_pages.api.get_menu_tree')
    const data = await response.json()
    if (data.message) {
      menuItems.value = data.message
    }
  } catch (error) {
    console.error('Error fetching menu:', error)
    // Fallback to static menu if API fails
    menuItems.value = [
      { label: 'Home', page_url: '#/', children: [] },
      { label: 'About Us', page_url: '#about', children: [] }
    ]
  }
})
</script>

<template>
  <header class="hns-header">
    <div class="header-container">
      <div class="logo-section">
        <div class="logo">HNS India</div>
      </div>
      <nav class="nav-links">
        <HnsMenuItem 
          v-for="item in menuItems" 
          :key="item.label" 
          :item="item" 
          :currentRoute="currentRoute"
        />
      </nav>
    </div>
  </header>
</template>

<style scoped>
.hns-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 100;
  font-family: 'Inter', sans-serif;
}

.header-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: -0.5px;
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-links a {
  color: #475569;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s;
}

.nav-links a:hover, .nav-links a.active {
  color: #2563eb;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.login-btn {
  background: transparent;
  border: none;
  color: #475569;
  font-weight: 600;
  cursor: pointer;
  padding: 0.5rem 1rem;
}

.login-btn:hover {
  color: #1e293b;
}

.signup-btn {
  background-color: #2563eb;
  color: #ffffff;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.signup-btn:hover {
  background-color: #1d4ed8;
}

@media (max-width: 768px) {
  .nav-links, .action-buttons {
    display: none;
  }
}
</style>
