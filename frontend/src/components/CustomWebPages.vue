<template>
  <div class="custom-web-pages-container">
    <!-- List View -->
    <div v-if="!selectedPage" class="pages-list-view">
      <div class="list-header">
        <h3>Custom Web Pages</h3>
        <p class="subtitle">Select a layout to load dynamic content and styles</p>
      </div>

      <div v-if="loadingList" class="loading-state">
        <div class="spinner"></div>
        <p>Loading pages...</p>
      </div>
      
      <div v-else-if="listError" class="error-state">
        <p>{{ listError }}</p>
      </div>

      <div v-else-if="pagesList.length === 0" class="empty-state">
        <p>No custom web pages available. Create one in the desk dashboard first.</p>
      </div>

      <div v-else class="pages-grid">
        <div 
          v-for="page in pagesList" 
          :key="page.name" 
          class="page-select-card"
          @click="selectPage(page.name)"
        >
          <div class="card-glow"></div>
          <div class="card-body">
            <span class="card-meta">Layout Template</span>
            <h4>{{ page.title }}</h4>
            <span class="view-btn">
              View Page 
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Page View -->
    <div v-else class="active-page-view">
      <div class="page-view-header">
        <button class="back-btn" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="back-icon">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Back to Directory
        </button>
        <h2>{{ selectedPage.title }}</h2>
      </div>

      <!-- Main Page Content -->
      <div v-if="selectedPage.content" class="main-page-content" v-html="selectedPage.content"></div>

      <!-- Horizontal Tabs Group -->
      <div v-if="horizontalPages.length > 0" class="horizontal-group">
        <nav class="sections-navbar">
          <button 
            v-for="(sec, idx) in horizontalPages" 
            :key="idx"
            :class="['section-nav-link', { active: activeHorizontalIdx === idx }]"
            @click="activeHorizontalIdx = idx"
          >
            {{ sec.page_title }}
          </button>
        </nav>
        <div class="horizontal-viewport" v-if="horizontalPages[activeHorizontalIdx]">
          <div v-html="horizontalPages[activeHorizontalIdx].content" class="section-html-content"></div>
        </div>
      </div>

      <!-- Vertical Tabs Group -->
      <div v-if="verticalPages.length > 0" class="vertical-group">
        <div class="viewport-wrapper">
          <aside class="vertical-sidebar">
            <div class="sidebar-links">
              <button 
                v-for="(sec, idx) in verticalPages" 
                :key="idx"
                :class="['sidebar-nav-link', { active: activeVerticalIdx === idx }]"
                @click="activeVerticalIdx = idx"
              >
                <svg class="tab-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                {{ sec.page_title }}
              </button>
            </div>
          </aside>

          <!-- Active Section Viewport -->
          <div class="section-viewport" v-if="verticalPages[activeVerticalIdx]">
            <div v-html="verticalPages[activeVerticalIdx].content" class="section-html-content"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'

const loadingList = ref(false)
const listError = ref(null)
const pagesList = ref([])
const selectedPageName = ref(null)
const selectedPage = ref(null)
const activeHorizontalIdx = ref(0)
const activeVerticalIdx = ref(0)

let styleTags = []
let scriptTags = []

const horizontalPages = computed(() => {
  return selectedPage.value?.tabs?.filter(p => p.tab_type === 'Horizontal') || []
})

const verticalPages = computed(() => {
  return selectedPage.value?.tabs?.filter(p => p.tab_type === 'Vertical') || []
})

const activeSections = computed(() => {
  const sections = []
  if (horizontalPages.value.length > 0 && horizontalPages.value[activeHorizontalIdx.value]) {
    sections.push(horizontalPages.value[activeHorizontalIdx.value])
  }
  if (verticalPages.value.length > 0 && verticalPages.value[activeVerticalIdx.value]) {
    sections.push(verticalPages.value[activeVerticalIdx.value])
  }
  return sections
})

const fetchPagesList = async () => {
  loadingList.value = true
  listError.value = null
  try {
    const res = await fetch('/api/method/web_pages.api.get_custom_web_pages')
    if (!res.ok) throw new Error('Failed to load pages list')
    const data = await res.json()
    pagesList.value = data.message || []
  } catch (e) {
    console.error(e)
    listError.value = 'Could not load custom web pages.'
  } finally {
    loadingList.value = false
  }
}

const selectPage = async (name) => {
  selectedPageName.value = name
  selectedPage.value = null
  activeHorizontalIdx.value = 0
  activeVerticalIdx.value = 0
  
  try {
    const res = await fetch(`/api/method/web_pages.api.get_custom_web_pages?name=${encodeURIComponent(name)}`)
    if (!res.ok) throw new Error('Failed to load page details')
    const data = await res.json()
    selectedPage.value = data.message || null
  } catch (e) {
    console.error(e)
    alert('Error loading page details')
  }
}

const goBack = () => {
  selectedPageName.value = null
  selectedPage.value = null
  cleanupEffects()
}

const cleanupEffects = () => {
  styleTags.forEach(t => t.remove())
  scriptTags.forEach(t => t.remove())
  styleTags = []
  scriptTags = []
}

const applyStylesAndScripts = (sections) => {
  cleanupEffects()
  if (!sections || sections.length === 0) return

  sections.forEach((section, index) => {
    if (section.css) {
      const s = document.createElement('style')
      s.id = 'vue-dynamic-css-' + index
      s.textContent = section.css
      document.head.appendChild(s)
      styleTags.push(s)
    }
  })
}

watch(activeSections, (newSecs) => {
  applyStylesAndScripts(newSecs)
}, { immediate: true })

onUnmounted(() => {
  cleanupEffects()
})

fetchPagesList()
</script>

<style scoped>
.custom-web-pages-container {
  padding: 1.5rem 0;
  color: #1f2937;
}

.list-header {
  margin-bottom: 2rem;
}

.list-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: #111827;
}

.subtitle {
  color: #6b7280;
  font-size: 0.95rem;
  margin: 0.25rem 0 0 0;
}

.loading-state, .error-state, .empty-state {
  text-align: center;
  padding: 3rem 1rem;
  background: #f9fafb;
  border: 1px dashed #e5e7eb;
  border-radius: 12px;
  color: #6b7280;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 1rem auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Cards Grid */
.pages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.25rem;
}

.page-select-card {
  position: relative;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.page-select-card:hover {
  border-color: #3b82f6;
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.08);
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at top right, rgba(59, 130, 246, 0.05), transparent 70%);
  pointer-events: none;
}

.card-meta {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #3b82f6;
  font-weight: 600;
  display: block;
  margin-bottom: 0.25rem;
}

.page-select-card h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0 0 1.5rem 0;
}

.view-btn {
  font-size: 0.88rem;
  color: #4b5563;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  transition: color 0.3s;
}

.page-select-card:hover .view-btn {
  color: #3b82f6;
}

.view-btn svg {
  transition: transform 0.3s;
}

.page-select-card:hover .view-btn svg {
  transform: translateX(4px);
}

/* Active Page Viewer */
.active-page-view {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-view-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.page-view-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.main-page-content {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  color: #374151;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 0.5rem 0.88rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.88rem;
  font-weight: 500;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.back-icon {
  transition: transform 0.3s;
}

.back-btn:hover .back-icon {
  transform: translateX(-2px);
}

.horizontal-group {
  margin-bottom: 3rem;
}

.sections-navbar {
  display: inline-flex;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.section-nav-link {
  background: transparent;
  border: none;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #475569;
  transition: all 0.3s;
  border-radius: 8px;
  font-size: 0.95rem;
}

.section-nav-link:hover {
  color: #0f172a;
}

.section-nav-link.active {
  background: #ffffff;
  color: #2563eb;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.horizontal-viewport {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

/* Vertical Tabs Premium Styling */
.viewport-wrapper {
  display: flex;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.vertical-sidebar {
  flex: 0 0 320px;
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.sidebar-links {
  display: flex;
  flex-direction: column;
}

.sidebar-nav-link {
  background: transparent;
  border: none;
  border-bottom: 1px solid #e2e8f0;
  padding: 1.25rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #334155;
  transition: all 0.2s;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.95rem;
  border-left: 4px solid transparent;
}

.tab-icon {
  width: 16px;
  height: 16px;
  color: #94a3b8;
  transition: color 0.2s;
}

.sidebar-nav-link:hover {
  background: #f1f5f9;
}

.sidebar-nav-link.active {
  background: #ffffff;
  color: #1e3a8a;
  border-left-color: #1e3a8a;
}

.sidebar-nav-link.active .tab-icon {
  color: #1e3a8a;
}

.section-viewport {
  flex: 1;
  padding: 2.5rem;
  background: #ffffff;
}

.section-html-content {
  color: #334155;
  line-height: 1.7;
}

@media (max-width: 768px) {
  .viewport-wrapper {
    flex-direction: column;
  }
  .vertical-sidebar {
    flex: none;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
}
</style>
