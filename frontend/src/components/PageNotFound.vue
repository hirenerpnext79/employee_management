<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  pageName: String
})

const pageContent = ref(null)
const pageCss = ref(null)
const isLoading = ref(false)
const hasError = ref(false)

const loadPage = async () => {
  if (!props.pageName || props.pageName === 'empty') {
    hasError.value = true
    pageContent.value = null
    return
  }

  // Use sessionStorage to cache pages for immediate loading
  const cacheKey = `hns_page_${props.pageName}`
  const cachedData = sessionStorage.getItem(cacheKey)
  
  if (cachedData) {
    try {
      const parsed = JSON.parse(cachedData)
      hasError.value = false
      pageContent.value = parsed.content
      pageCss.value = parsed.css
    } catch (e) {
      hasError.value = false
      pageContent.value = cachedData
      pageCss.value = null
    }
  }

  // Fetch in background to update cache if needed, or if not cached yet
  if (!cachedData) {
    isLoading.value = true
  }
  
  hasError.value = false

  try {
    const response = await fetch(`/api/method/web_pages.api.get_custom_web_pages?name=${encodeURIComponent(props.pageName)}`)
    const data = await response.json()
    if (data.message && data.message.content) {
      pageContent.value = data.message.content
      pageCss.value = data.message.css || null
      sessionStorage.setItem(cacheKey, JSON.stringify({ content: pageContent.value, css: pageCss.value }))
    } else if (!cachedData) {
      hasError.value = true
      pageContent.value = null
    }
  } catch (error) {
    console.error('Failed to load page:', error)
    if (!cachedData) {
      hasError.value = true
      pageContent.value = null
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadPage()
})

watch(() => props.pageName, () => {
  loadPage()
})
</script>

<template>
  <div class="dynamic-page-wrapper">
    <div v-if="hasError" class="empty-state-wrapper">
      <div class="empty-state">
        <h3>Page Not Found</h3>
        <p>Please create this page and link it on the menu.</p>
      </div>
    </div>
    <div v-else class="page-content">
      <component :is="'style'" v-if="pageCss" v-html="pageCss"></component>
      <div v-html="pageContent"></div>
    </div>
  </div>
</template>

<style scoped>
.dynamic-page-wrapper {
  min-height: 400px;
}

.empty-state-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background-color: #f8f9fa;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1rem;
}

.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  color: #64748b;
}

.page-content {
  color: #334155;
  line-height: 1.6;
}
</style>
