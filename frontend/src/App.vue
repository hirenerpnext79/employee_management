<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import VCard from './components/VCard.vue'
import HnsHeader from './components/HnsHeader.vue'
import HnsFooter from './components/HnsFooter.vue'
import HnsHome from './components/HnsHome.vue'
import HnsCustomPage from './components/HnsCustomPage.vue'
import HNSWebPage from './components/HNSWebPage.vue'
import GlobalToast from './components/GlobalToast.vue'

const parseRoute = () => {
  const urlParams = new URLSearchParams(window.location.search)
  let t = urlParams.get('token')
  let path = window.location.pathname.replace(/^\/|\/$/g, '')
  let hashPage = window.location.hash.replace(/^#\/?/, '').split('?')[0]
  
  let pageName = ''

  if (!t) {
    const parts = path.split('/')
    if (parts.length >= 2) {
      t = parts[0]
      pageName = parts.slice(1).join('/')
    } else if (parts.length === 1 && parts[0]) {
      if (/^\d+$/.test(parts[0])) {
        t = parts[0]
      } else {
        pageName = parts[0]
      }
    }
  } else {
    pageName = path
  }

  if (hashPage && hashPage !== '/') {
    pageName = hashPage
  }

  return { token: t, page: pageName || '/' }
}

const initialRouteData = parseRoute()
const token = ref(initialRouteData.token)
const currentRoute = ref(initialRouteData.page === '/' ? '/' : `/${initialRouteData.page}`)

const handleLocationChange = () => {
  const data = parseRoute()
  currentRoute.value = data.page === '/' ? '/' : `/${data.page}`
  
  if (currentRoute.value === '/') token.value = null;
  else token.value = data.token;

  let expectedPath = data.token ? `/${data.token}` : (data.page !== '/' ? `/${data.page}` : '/');

  const urlParams = new URLSearchParams(window.location.search)
  urlParams.delete('token')
  const searchStr = urlParams.toString()
  const expectedSearch = searchStr ? `?${searchStr}` : ''

  const expectedHash = (data.token && data.page !== '/') ? `#/${data.page}` : ''
  const expectedUrl = expectedPath + expectedSearch + expectedHash

  if (window.location.pathname + window.location.search + window.location.hash !== expectedUrl) {
      window.history.replaceState({}, '', expectedUrl)
  }
}

const handleLinkClick = (e) => {
  const link = e.target.closest('a')
  if (link?.href?.startsWith(window.location.origin) && !link.getAttribute('target') && !link.hasAttribute('download')) {
    e.preventDefault()
    window.history.pushState({}, '', link.href)
    handleLocationChange()
  }
}

onMounted(() => {
  window.addEventListener('popstate', handleLocationChange)
  window.addEventListener('hashchange', handleLocationChange)
  window.addEventListener('click', handleLinkClick)
})

onUnmounted(() => {
  window.removeEventListener('popstate', handleLocationChange)
  window.removeEventListener('hashchange', handleLocationChange)
  window.removeEventListener('click', handleLinkClick)
})

const isDynamicPage = computed(() => currentRoute.value !== '/')

const dynamicPageName = computed(() => {
  if (!isDynamicPage.value) return null;
  const path = currentRoute.value.replace(/^\//, '').split('?')[0]
  return path ? decodeURIComponent(path) : 'empty'
})

const isHnsWebPageRoute = ref(false);
const checkingRoute = ref(false);

const checkRouteType = async (pageName) => {
  if (!pageName || pageName === 'empty') return;
  checkingRoute.value = true;
  try {
    const res = await fetch(`/api/method/employee_management.api.get_custom_web_pages?name=${encodeURIComponent(pageName)}`);
    const data = await res.json();
    isHnsWebPageRoute.value = !!(res.ok && data?.message);
  } catch {
    isHnsWebPageRoute.value = false;
  } finally {
    checkingRoute.value = false;
  }
}

watch(dynamicPageName, (newVal) => {
  if (newVal && newVal !== 'empty') checkRouteType(newVal);
}, { immediate: true });

</script>

<template>
  <div class="hns-app-wrapper">
    <GlobalToast />
    <HnsHeader v-if="!token && !isHnsWebPageRoute" :currentRoute="currentRoute" />
    <transition name="page-fade" mode="out-in">
      <div v-if="currentRoute === '/' && !token" class="full-width-container" key="home">
        <HnsHome />
      </div>
      <div v-else-if="currentRoute === '/' && token" class="content-container" key="vcard">
        <VCard :token="token" />
      </div>
      <div v-else-if="checkingRoute" class="loading-state full-width-container" key="checking">
         <div style="display: flex; justify-content: center; padding: 50px;">Loading...</div>
      </div>
      <div v-else-if="isDynamicPage && (token || isHnsWebPageRoute)" class="full-width-container" :key="dynamicPageName || 'vcard_custom'">
        <HNSWebPage :pageName="dynamicPageName" />
      </div>
      <div v-else-if="isDynamicPage && !token && !isHnsWebPageRoute" class="full-width-container" :key="dynamicPageName || 'custom'">
        <HnsCustomPage :pageName="dynamicPageName" />
      </div>
    </transition>
    <HnsFooter v-if="!token && !isHnsWebPageRoute" />
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
  box-sizing: border-box;
}
.full-width-container {
  width: 100%;
  flex: 1;
}

@media (max-width: 640px) {
  .content-container {
    padding: 0;
  }
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
