<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import VCard from './components/VCard.vue'
import HnsHeader from './components/HnsHeader.vue'
import HnsFooter from './components/HnsFooter.vue'
import HnsHome from './components/HnsHome.vue'
import HnsCustomPage from './components/HnsCustomPage.vue'
import HNSWebPage from './components/HNSWebPage.vue'
import GlobalToast from './components/GlobalToast.vue'
import { getGlobalSessionToken, getGlobalPassword, getGlobalUser, setGlobalSession, clearGlobalSession, setStoredWebCode, clearStoredWebCode } from './utils/cookieHandler'

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

  // Only rewrite URL if legacy ?token= query was passed to root path
  if (data.token && window.location.pathname === '/' && window.location.search.includes('token')) {
    window.history.replaceState({}, '', `/${data.token}`)
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
const initialPageData = ref(null);

const webCode = computed(() => {
  const hashPart = window.location.hash.includes('?') ? window.location.hash.split('?')[1] : ''
  const hashParams = new URLSearchParams(hashPart)
  const searchParams = new URLSearchParams(window.location.search)
  const hrefPart = window.location.href.includes('?') ? window.location.href.split('?')[1] : ''
  const hrefParams = new URLSearchParams(hrefPart)
  const found = (
    hashParams.get('web_code') ||
    searchParams.get('web_code') ||
    hrefParams.get('web_code') ||
    hashParams.get('token') ||
    searchParams.get('token') ||
    hrefParams.get('token') ||
    token.value ||
    ''
  )
  if (found) {
    setStoredWebCode(found)
    return found
  }
  clearStoredWebCode()
  return ''
})

const checkRouteType = async (pageName) => {
  if (!pageName || pageName === 'empty') return;

  const routeTypeKey = `hns_route_type_${pageName}`;
  const cachedRouteType = sessionStorage.getItem(routeTypeKey);
  const hasCustomPageCache = Boolean(sessionStorage.getItem(`hns_page_${pageName}`));

  if (cachedRouteType === 'hns_portal') {
    isHnsWebPageRoute.value = true;
  } else if (cachedRouteType === 'custom' || hasCustomPageCache) {
    isHnsWebPageRoute.value = false;
  } else {
    checkingRoute.value = true;
  }

  try {
    const code = webCode.value;
    const sessionToken = getGlobalSessionToken();
    const storedPwd = getGlobalPassword();
    const storedUser = getGlobalUser();

    const payload = {
      name: pageName,
    };
    if (sessionToken) {
      payload.session_token = sessionToken;
    }
    if (storedPwd) {
      payload.password = storedPwd;
    }
    if (storedUser) {
      payload.username = storedUser;
    }
    if (code) payload.web_code = code;

    const res = await fetch('/api/method/employee_management.api.get_custom_web_pages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (res.ok && data?.message) {
      isHnsWebPageRoute.value = true;
      initialPageData.value = data.message;
      sessionStorage.setItem(routeTypeKey, 'hns_portal');
      if (data.message.session_token && data.message.is_authorized) {
        const userToSave = data.message.login_user || storedUser || data.message.employee_name || data.message.customer_name;
        const pwdToSave = storedPwd || getGlobalPassword();
        if (userToSave || pwdToSave) {
          setGlobalSession(data.message.session_token, userToSave, pwdToSave);
        }
      }
      if (data.message.session_expired && !storedPwd) {
        clearGlobalSession();
      }
    } else {
      isHnsWebPageRoute.value = false;
      initialPageData.value = null;
      sessionStorage.setItem(routeTypeKey, 'custom');
    }
  } catch {
    isHnsWebPageRoute.value = false;
    initialPageData.value = null;
    sessionStorage.setItem(routeTypeKey, 'custom');
  } finally {
    checkingRoute.value = false;
  }
}

const onLogout = () => {
  clearGlobalSession();
  initialPageData.value = null;
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
        <HNSWebPage :pageName="dynamicPageName" :initialPageData="initialPageData" :token="token" :webCode="webCode" @logout="onLogout" />
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
