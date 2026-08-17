<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import VCard from './components/VCard.vue'
import HnsHeader from './components/HnsHeader.vue'
import HnsFooter from './components/HnsFooter.vue'
import HnsHome from './components/HnsHome.vue'
import HnsCustomPage from './components/HnsCustomPage.vue'
import GlobalToast from './components/GlobalToast.vue'

const urlParams = new URLSearchParams(window.location.search)
let t = urlParams.get('token')
if (!t) {
  const match = window.location.pathname.match(/^\/(\d{5})\/?$/)
  if (match) {
    t = match[1]
  }
}

const token = ref(t)
const currentRoute = ref(window.location.hash || '#/')

const handleHashChange = () => {
  currentRoute.value = window.location.hash || '#/'
  
  // If navigating explicitly to home, clear the token so the Home page shows
  if (currentRoute.value === '#/') {
    token.value = null
  }

  if (window.location.search.includes('token=')) {
    const newUrl = window.location.origin + window.location.pathname + window.location.hash
    window.history.replaceState({}, '', newUrl)
  }
}

onMounted(() => {
  window.addEventListener('hashchange', handleHashChange)
})

onUnmounted(() => {
  window.removeEventListener('hashchange', handleHashChange)
})

const isDynamicPage = computed(() => {
  return currentRoute.value !== '#/'
})

const dynamicPageName = computed(() => {
  if (isDynamicPage.value) {
    let path = currentRoute.value.replace(/^#\/?/, '')
    path = path.split('?')[0]
    return path ? decodeURIComponent(path) : 'empty'
  }
  return null
})
</script>

<template>
  <div class="hns-app-wrapper">
    <GlobalToast />
    <HnsHeader :currentRoute="currentRoute" />
    <transition name="page-fade" mode="out-in">
      <div v-if="currentRoute === '#/' && !token" class="full-width-container" key="home">
        <HnsHome />
      </div>
      <div v-else-if="currentRoute === '#/' && token" class="content-container" key="vcard">
        <VCard :token="token" />
      </div>
      <div v-else-if="isDynamicPage" class="full-width-container" :key="dynamicPageName || 'custom'">
        <HnsCustomPage :pageName="dynamicPageName" />
      </div>
    </transition>
    <HnsFooter />
  </div>
</template>

<style>
.hns-app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}
.content-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  flex: 1;
  width: 100%;
}
.full-width-container {
  width: 100%;
  flex: 1;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>

