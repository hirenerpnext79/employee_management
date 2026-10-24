<script setup>
import { ref, onMounted } from 'vue'
import HnsMenuItem from './HnsMenuItem.vue'
import { showError } from '../utils/toastHandler'

defineProps({
  currentRoute: String
})

const menuItems = ref([])
const isMobileMenuOpen = ref(false)
const topBarHTML = ref('')
const topBarCSS = ref('')

const cachedMenu = sessionStorage.getItem('hns_header_menu')
if (cachedMenu) {
  try {
    const parsed = JSON.parse(cachedMenu)
    menuItems.value = parsed.menu_items || []
    topBarHTML.value = parsed.top_bar || ''
    topBarCSS.value = parsed.top_bar_css || ''
  } catch (e) {}
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

onMounted(async () => {
  try {
    const response = await fetch('/api/method/web_pages.api.get_menu_tree', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ menu_type: 'Header' }),
    })
    const data = await response.json()
    if (data.message) {
      menuItems.value = data.message.menu_items || []
      topBarHTML.value = data.message.top_bar || ''
      topBarCSS.value = data.message.top_bar_css || ''
      sessionStorage.setItem('hns_header_menu', JSON.stringify(data.message))
    }
  } catch (error) {
    console.error('Error fetching menu:', error)
    if (!menuItems.value || menuItems.value.length === 0) {
      menuItems.value = [
        { label: 'Home', page_url: '#/', children: [] },
        { label: 'About Us', page_url: '#about', children: [] }
      ]
    }
  }
})
</script>

<template>
  <component is="style" v-if="topBarCSS">{{ topBarCSS }}</component>
  
  <div v-if="topBarHTML" v-html="topBarHTML"></div>

  <header class="hns-header">
    <div class="header-container">
      <div class="logo-section">
        <a href="/" class="logo-link" style="text-decoration: none; color: inherit;">
          <div class="logo">HNS India</div>
        </a>
      </div>
      <!-- Mobile menu toggle button -->
      <button class="mobile-menu-toggle" @click="toggleMobileMenu" aria-label="Toggle navigation">
        <span class="hamburger-line" :class="{ 'open': isMobileMenuOpen }"></span>
        <span class="hamburger-line" :class="{ 'open': isMobileMenuOpen }"></span>
        <span class="hamburger-line" :class="{ 'open': isMobileMenuOpen }"></span>
      </button>

      <nav class="nav-links" :class="{ 'mobile-active': isMobileMenuOpen }">
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

.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 21px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 101;
}

.hamburger-line {
  width: 100%;
  height: 3px;
  background-color: #1e293b;
  border-radius: 10px;
  transition: all 0.3s ease-in-out;
}

.hamburger-line.open:nth-child(1) {
  transform: translateY(9px) rotate(45deg);
}

.hamburger-line.open:nth-child(2) {
  opacity: 0;
}

.hamburger-line.open:nth-child(3) {
  transform: translateY(-9px) rotate(-45deg);
}

@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }
  
  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: #ffffff;
    flex-direction: column;
    padding: 1rem 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
  
  .nav-links.mobile-active {
    display: flex;
  }
  
  .action-buttons {
    display: none;
  }
}
</style>
