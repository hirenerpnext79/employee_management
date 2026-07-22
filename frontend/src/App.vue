<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import VCard from './components/VCard.vue'
import HnsHeader from './components/HnsHeader.vue'
import HnsFooter from './components/HnsFooter.vue'
import HnsAbout from './components/HnsAbout.vue'
import PageNotFound from './components/PageNotFound.vue'

const urlParams = new URLSearchParams(window.location.search)
let t = urlParams.get('token')
if (!t) {
  const match = window.location.pathname.match(/\/token=([a-f0-9]+)/)
  if (match) {
    t = match[1]
  }
}
const token = ref(t)

const currentRoute = ref(window.location.hash || '#/')

const handleHashChange = () => {
  currentRoute.value = window.location.hash || '#/'
}

onMounted(() => {
  window.addEventListener('hashchange', handleHashChange)
})

onUnmounted(() => {
  window.removeEventListener('hashchange', handleHashChange)
})

const isDynamicPage = computed(() => {
  return currentRoute.value !== '#/' && currentRoute.value !== '#about'
})

const dynamicPageName = computed(() => {
  if (isDynamicPage.value) {
    const parts = currentRoute.value.split('/')
    const lastPart = parts[parts.length - 1]
    return lastPart ? decodeURIComponent(lastPart) : 'empty'
  }
  return null
})
</script>

<template>
  <div class="hns-app-wrapper">
    <HnsHeader :currentRoute="currentRoute" />
    <div v-if="dynamicPageName === 'about-us' || currentRoute === '#about' || (!token && currentRoute === '#/')">
      <HnsAbout />
    </div>
    <div v-else-if="isDynamicPage" class="content-container">
      <PageNotFound :pageName="dynamicPageName" />
    </div>
    <div v-else class="content-container">
      <VCard :token="token" />
    </div>
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
</style>
