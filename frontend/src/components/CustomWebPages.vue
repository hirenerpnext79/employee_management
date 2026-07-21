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

      <!-- Top Navbar (For Horizontal Tabs Group) -->
      <nav v-if="hasHorizontalTabs" class="sections-navbar">
        <div class="nav-group-header">Horizontal Tabs</div>
        <button 
          v-for="(sec, idx) in selectedPage.pages" 
          :key="idx"
          v-show="sec.tab_type === 'Horizontal'"
          :class="['section-nav-link', { active: activeSectionIdx === idx }]"
          @click="activeSectionIdx = idx"
        >
          {{ sec.page_title }}
        </button>
      </nav>

      <!-- Viewport Wrapper (Vertical Sidebar + Main Viewport) -->
      <div class="viewport-wrapper">
        <!-- Sidebar Navbar (For Vertical Tabs Group) -->
        <aside v-if="hasVerticalTabs" class="vertical-sidebar">
          <div class="sidebar-header">Vertical Tabs</div>
          <div class="sidebar-links">
            <button 
              v-for="(sec, idx) in selectedPage.pages" 
              :key="idx"
              v-show="sec.tab_type === 'Vertical'"
              :class="['sidebar-nav-link', { active: activeSectionIdx === idx }]"
              @click="activeSectionIdx = idx"
            >
              {{ sec.page_title }}
            </button>
          </div>
        </aside>

        <!-- Active Section Viewport -->
        <div v-if="activeSection" class="section-viewport">
          <div v-html="activeSection.content" class="section-html-content"></div>
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
const activeSectionIdx = ref(0)

let styleTag = null
let scriptTag = null

const activeSection = computed(() => {
  if (selectedPage.value && selectedPage.value.pages) {
    return selectedPage.value.pages[activeSectionIdx.value]
  }
  return null
})

const hasHorizontalTabs = computed(() => {
  return selectedPage.value?.pages?.some(p => p.tab_type === 'Horizontal')
})

const hasVerticalTabs = computed(() => {
  return selectedPage.value?.pages?.some(p => p.tab_type === 'Vertical')
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
  activeSectionIdx.value = 0
  
  try {
    const res = await fetch(`/api/method/web_pages.api.get_custom_web_pages?name=${encodeURIComponent(name)}`)
    if (!res.ok) throw new Error('Failed to load page details')
    const data = await res.json()
    selectedPage.value = data.message || null
    
    // Auto-focus the first sorted tab of any type
    if (selectedPage.value && selectedPage.value.pages.length > 0) {
      activeSectionIdx.value = 0
    }
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
  if (styleTag) {
    styleTag.remove()
    styleTag = null
  }
  if (scriptTag) {
    scriptTag.remove()
    scriptTag = null
  }
}

const applyStylesAndScripts = (section) => {
  cleanupEffects()
  if (!section) return

  // Inject Custom Section CSS
  if (section.css) {
    styleTag = document.createElement('style')
    styleTag.id = 'vue-dynamic-section-css'
    styleTag.textContent = section.css
    document.head.appendChild(styleTag)
  }

  // Inject Custom Section JS inside IIFE
  if (section.js) {
    scriptTag = document.createElement('script')
    scriptTag.id = 'vue-dynamic-section-js'
    scriptTag.textContent = `(function() {
      try {
        ${section.js}
      } catch (e) {
        console.error("Error executing custom JS for section '${section.page_title}':", e);
      }
    })();`
    document.body.appendChild(scriptTag)
  }
}

watch(activeSection, (newSec) => {
  applyStylesAndScripts(newSec)
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

/* Tab/Section Navbar */
.sections-navbar {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: #f3f4f6;
  padding: 0.35rem 1rem;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  overflow-x: auto;
}

.nav-group-header {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #3b82f6;
  font-weight: 700;
  margin-right: 0.75rem;
  border-right: 1px solid #d1d5db;
  padding-right: 0.75rem;
  white-space: nowrap;
}

.section-nav-link {
  background: transparent;
  border: none;
  color: #6b7280;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s;
}

.section-nav-link:hover {
  color: #111827;
}

.section-nav-link.active {
  background: #ffffff;
  color: #3b82f6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Two-column layout */
.viewport-wrapper {
  display: flex;
  gap: 1.5rem;
}

/* Sidebar Navbar */
.vertical-sidebar {
  flex: 0 0 220px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  height: fit-content;
}

.sidebar-header {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #3b82f6;
  font-weight: 700;
  padding-left: 0.5rem;
}

.sidebar-links {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.sidebar-nav-link {
  background: transparent;
  border: none;
  color: #4b5563;
  padding: 0.5rem 0.88rem;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s;
  display: block;
  width: 100%;
}

.sidebar-nav-link:hover {
  background: #f3f4f6;
  color: #111827;
}

.sidebar-nav-link.active {
  background: #3b82f6;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Content Viewport */
.section-viewport {
  flex: 1;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 2rem;
  min-height: 250px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.section-html-content {
  color: #374151;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .viewport-wrapper {
    flex-direction: column;
  }
  .vertical-sidebar {
    flex: none;
    width: 100%;
  }
  .sidebar-nav-link {
    text-align: center;
  }
}
</style>
