<script setup>
import { ref } from 'vue'

defineProps({
  item: {
    type: Object,
    required: true
  },
  currentRoute: String
})

const isOpen = ref(false)
</script>

<template>
  <div class="menu-item-container" @mouseenter="isOpen = true" @mouseleave="isOpen = false">
    <a 
      :href="item.page_url || '#'" 
      class="nav-link"
      :class="{ 'has-children': item.children && item.children.length > 0, 'active': currentRoute === item.page_url }"
    >
      {{ item.label }}
      <svg v-if="item.children && item.children.length > 0" class="dropdown-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </a>
    <div v-if="item.children && item.children.length > 0" v-show="isOpen" class="dropdown-menu">
      <HnsMenuItem 
        v-for="child in item.children" 
        :key="child.label" 
        :item="child" 
        :currentRoute="currentRoute"
      />
    </div>
  </div>
</template>

<style scoped>
.menu-item-container {
  position: relative;
  display: flex;
}

.dropdown-menu .menu-item-container {
  width: 100%;
}

.nav-link {
  color: #334155;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  padding: 0.6rem 1rem;
  white-space: nowrap;
  width: 100%;
  border-radius: 6px;
}

.nav-link:hover, .nav-link.active {
  color: #0f172a;
  background-color: #f1f5f9;
}

.dropdown-menu .nav-link:hover {
  background-color: #f8fafc;
}

.dropdown-icon {
  width: 1rem;
  height: 1rem;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: white;
  min-width: 200px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border-radius: 0.375rem;
  border: 1px solid #e2e8f0;
  z-index: 50;
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
}

/* For nested dropdowns (2nd level onwards), show on the right */
.dropdown-menu .menu-item-container .dropdown-menu {
  top: 0;
  left: 100%;
  margin-left: -4px;
}

/* Adjust dropdown icon rotation for side menus */
.dropdown-menu .dropdown-icon {
  transform: rotate(-90deg);
}
</style>
