<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  pageName: String
})

const pageContent = ref(null)
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
  const cachedContent = sessionStorage.getItem(cacheKey)
  
  if (cachedContent) {
    hasError.value = false
    pageContent.value = cachedContent
  }

  // Fetch in background to update cache if needed, or if not cached yet
  if (!cachedContent) {
    isLoading.value = true
  }
  
  hasError.value = false

  try {
    const response = await fetch(`/api/method/web_pages.api.get_custom_web_pages?name=${encodeURIComponent(props.pageName)}`)
    const data = await response.json()
    if (data.message && data.message.content) {
      pageContent.value = data.message.content
      sessionStorage.setItem(cacheKey, data.message.content)
    } else if (!cachedContent) {
      hasError.value = true
      pageContent.value = null
    }
  } catch (error) {
    console.error('Failed to load page:', error)
    if (!cachedContent) {
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
    <div v-if="hasError" class="empty-state">
      <h3>Page Not Found</h3>
      <p>Please create this page and link it on the menu.</p>
    </div>
    <div v-else class="page-content" v-html="pageContent">
    </div>
  </div>
</template>

<style scoped>
.dynamic-page-wrapper {
  padding: 2rem;
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
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
