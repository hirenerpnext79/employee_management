<template>
  <div class="custom-page-wrapper">
    <transition name="page-fade" mode="out-in">
      <div v-if="loading" class="loading-state" key="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      
      <PageNotFound v-else-if="error" key="error" />
      
      <div v-else-if="selectedPage" class="active-page-view" :key="selectedPage.name">
      
      <!-- Hero Banner -->
      <div v-if="selectedPage.main_title" class="hero-banner" :class="{ 'no-image': !selectedPage.image }">
        <div class="hero-content">
          <h1 class="hero-title">{{ selectedPage.main_title }}</h1>
        </div>
        <div class="hero-image" v-if="selectedPage.image">
          <img :src="selectedPage.image" alt="Main Title Image" />
        </div>
      </div>

      <div class="hns-page-container">
        <!-- Video Section -->
        <div v-if="embedUrl" class="video-section">
          <iframe 
            :src="embedUrl" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen>
          </iframe>
        </div>

        <!-- Main Page Content -->
        <div v-if="selectedPage.content" class="main-page-content" v-html="selectedPage.content"></div>

      <!-- Grouped Tabs Display -->
      <div v-for="(group, gIdx) in groupedTabs" :key="gIdx" class="tab-group-section">
        <h2 v-if="group.name && group.name !== 'Default Group'" class="group-title">{{ group.name }}</h2>

        <!-- Horizontal Tabs Group -->
        <div v-if="group.horizontal.length > 0" class="horizontal-group">
          <nav class="sections-navbar">
            <button 
              v-for="(sec, idx) in group.horizontal" 
              :key="idx"
              :class="['section-nav-link', { active: activeHorizontalIndices[group.name] === idx }]"
              @click="activeHorizontalIndices[group.name] = idx"
            >
              {{ sec.page_title }}
            </button>
          </nav>
          <div class="horizontal-viewport" v-if="group.horizontal[activeHorizontalIndices[group.name] || 0]">
            <div class="tab-layout" :class="{ 'has-media': group.horizontal[activeHorizontalIndices[group.name] || 0].image || getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] || 0].video_url) }">
              <!-- Tab Media -->
              <div v-if="group.horizontal[activeHorizontalIndices[group.name] || 0].image || getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] || 0].video_url)" class="tab-media-wrapper">
                <img v-if="group.horizontal[activeHorizontalIndices[group.name] || 0].image" :src="group.horizontal[activeHorizontalIndices[group.name] || 0].image" :alt="group.horizontal[activeHorizontalIndices[group.name] || 0].page_title" />
                <iframe v-else-if="getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] || 0].video_url)" 
                  :src="getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] || 0].video_url)" 
                  title="YouTube video player" 
                  frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                  allowfullscreen>
                </iframe>
              </div>
              <!-- Tab Content -->
              <div v-html="group.horizontal[activeHorizontalIndices[group.name] || 0].content" class="section-html-content"></div>
            </div>
          </div>
        </div>

        <!-- Vertical Tabs Group -->
        <div v-if="group.vertical.length > 0" class="vertical-group">
          <div class="viewport-wrapper">
            <aside class="vertical-sidebar">
              <div class="sidebar-links">
                <button 
                  v-for="(sec, idx) in group.vertical" 
                  :key="idx"
                  :class="['sidebar-nav-link', { active: activeVerticalIndices[group.name] === idx }]"
                  @click="activeVerticalIndices[group.name] = idx"
                >
                  <svg class="tab-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                  {{ sec.page_title }}
                </button>
              </div>
            </aside>

            <!-- Dynamic Content -->
            <div class="section-viewport" v-if="group.vertical[activeVerticalIndices[group.name] || 0]">
              <div class="tab-layout" :class="{ 'has-media': group.vertical[activeVerticalIndices[group.name] || 0].image || getEmbedUrl(group.vertical[activeVerticalIndices[group.name] || 0].video_url) }">
                <!-- Tab Media -->
                <div v-if="group.vertical[activeVerticalIndices[group.name] || 0].image || getEmbedUrl(group.vertical[activeVerticalIndices[group.name] || 0].video_url)" class="tab-media-wrapper">
                  <img v-if="group.vertical[activeVerticalIndices[group.name] || 0].image" :src="group.vertical[activeVerticalIndices[group.name] || 0].image" :alt="group.vertical[activeVerticalIndices[group.name] || 0].page_title" />
                  <iframe v-else-if="getEmbedUrl(group.vertical[activeVerticalIndices[group.name] || 0].video_url)" 
                    :src="getEmbedUrl(group.vertical[activeVerticalIndices[group.name] || 0].video_url)" 
                    title="YouTube video player" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    allowfullscreen>
                  </iframe>
                </div>
                <!-- Tab Content -->
                <div v-html="group.vertical[activeVerticalIndices[group.name] || 0].content" class="section-html-content"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Custom Sections Display -->
      <div v-if="selectedPage.sections && selectedPage.sections.length > 0" class="custom-sections-wrapper">
        <div v-for="(sec, idx) in selectedPage.sections" :key="'sec-'+idx" class="custom-section">
          <!-- Title Box -->
          <h2 class="custom-section-title" v-if="sec.page_title">{{ sec.page_title }}</h2>
          
          <!-- Content Layout -->
          <div class="custom-section-body" :class="{ 'has-media': sec.image || getEmbedUrl(sec.video_url), 'full-width': !sec.image && !getEmbedUrl(sec.video_url) }">
            
            <div v-if="sec.image || getEmbedUrl(sec.video_url)" class="custom-section-media">
              <img v-if="sec.image" :src="sec.image" :alt="sec.page_title" />
              <iframe v-else-if="getEmbedUrl(sec.video_url)" 
                :src="getEmbedUrl(sec.video_url)" 
                title="Video player" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
              </iframe>
            </div>
            
            <div class="custom-section-content" v-html="sec.content"></div>
            
          </div>
        </div>
      </div>

      <!-- Optional Slot for Page-Specific Static Sections -->
      <slot name="after-sections"></slot>

      </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, computed, nextTick } from 'vue'
import PageNotFound from './PageNotFound.vue'
import { showError } from '../utils/toastHandler'

const props = defineProps({
  pageName: {
    type: String,
    required: true
  }
})

const loading = ref(false)
const error = ref(null)
const selectedPage = ref(null)

const getEmbedUrl = (rawUrl) => {
  if (!rawUrl) return null;
  let url = rawUrl;
  
  if (url.includes('<iframe')) {
    const match = url.match(/src=["'](.*?)["']/);
    if (match && match[1]) {
      url = match[1];
    } else {
      return null;
    }
  }
  
  if (url.includes('watch?v=')) {
    url = url.replace('watch?v=', 'embed/').split('&')[0];
  } else if (url.includes('youtu.be/')) {
    url = url.replace('youtu.be/', 'youtube.com/embed/').split('?')[0];
  }
  return url;
}

const embedUrl = computed(() => getEmbedUrl(selectedPage.value?.video_url))

const activeHorizontalIndices = ref({})
const activeVerticalIndices = ref({})

let styleTags = []
let scriptTags = []

const groupedTabs = computed(() => {
  const groups = {}
  const tabs = selectedPage.value?.tabs || []
  
  tabs.forEach(tab => {
    const groupName = tab.group_name || 'Default Group'
    if (!groups[groupName]) {
      groups[groupName] = {
        name: groupName,
        horizontal: [],
        vertical: []
      }
    }
    if (tab.tab_type === 'Vertical') {
      groups[groupName].vertical.push(tab)
    } else {
      groups[groupName].horizontal.push(tab)
    }
  })
  
  return Object.values(groups)
})

watch(groupedTabs, (groups) => {
  groups.forEach(g => {
    if (activeHorizontalIndices.value[g.name] === undefined) {
      activeHorizontalIndices.value[g.name] = 0
    }
    if (activeVerticalIndices.value[g.name] === undefined) {
      activeVerticalIndices.value[g.name] = 0
    }
  })
}, { immediate: true })

const activeSections = computed(() => {
  const sections = []
  groupedTabs.value.forEach(g => {
    const hIdx = activeHorizontalIndices.value[g.name] || 0
    if (g.horizontal[hIdx]) sections.push(g.horizontal[hIdx])
    
    const vIdx = activeVerticalIndices.value[g.name] || 0
    if (g.vertical[vIdx]) sections.push(g.vertical[vIdx])
  })
  
  if (selectedPage.value?.sections) {
    sections.push(...selectedPage.value.sections)
  }
  
  return sections
})

const fetchPageData = async (name) => {
  if (!name) return;
  const cacheKey = `hns_page_${name}`
  const cachedContent = sessionStorage.getItem(cacheKey)
  
  if (cachedContent) {
    selectedPage.value = JSON.parse(cachedContent)
  }

  if (!cachedContent) {
    loading.value = true
  }
  
  error.value = null

  try {
    const res = await fetch(`/api/method/web_pages.api.get_custom_web_pages?name=${encodeURIComponent(name)}`)
    if (!res.ok) throw new Error('Failed to load page details')
    const data = await res.json()
    selectedPage.value = data.message || null
    
    if (data.message && Object.keys(data.message).length > 0) {
      sessionStorage.setItem(cacheKey, JSON.stringify(data.message))
    }

    if (!selectedPage.value || Object.keys(selectedPage.value).length === 0 || ((!selectedPage.value.tabs || selectedPage.value.tabs.length === 0) && !selectedPage.value.content && !selectedPage.value.sections)) {
      error.value = `No content found in the '${name}' Custom Web Page.`
      sessionStorage.removeItem(cacheKey)
    }
  } catch (e) {
    console.error(e)
    error.value = `Failed to fetch '${name}' data from the server.`
    showError(error.value)
  } finally {
    loading.value = false
  }
}

watch(() => props.pageName, (newName) => {
  fetchPageData(newName)
}, { immediate: true })

const cleanupEffects = () => {
  styleTags.forEach(t => t.remove())
  scriptTags.forEach(t => t.remove())
  styleTags = []
  scriptTags = []
}

const applyStylesAndScripts = (sections) => {
  cleanupEffects()

  if (selectedPage.value && selectedPage.value.css) {
    const s = document.createElement('style')
    s.id = 'hns-dynamic-page-main-css'
    s.textContent = selectedPage.value.css
    document.head.appendChild(s)
    styleTags.push(s)
  }
  
  if (selectedPage.value && selectedPage.value.js) {
    const script = document.createElement('script')
    script.id = 'hns-dynamic-page-main-js'
    script.textContent = selectedPage.value.js
    document.body.appendChild(script)
    scriptTags.push(script)
  }

  if (!sections || sections.length === 0) return

  sections.forEach((section, index) => {
    if (section.css) {
      const s = document.createElement('style')
      s.id = 'hns-dynamic-page-css-' + index
      s.textContent = section.css
      document.head.appendChild(s)
      styleTags.push(s)
    }
    
    if (section.js) {
      const script = document.createElement('script')
      script.id = 'hns-dynamic-page-js-' + index
      script.textContent = section.js
      document.body.appendChild(script)
      scriptTags.push(script)
    }
  })
}

watch(activeSections, async (newSecs) => {
  await nextTick()
  applyStylesAndScripts(newSecs)
}, { immediate: true })

onUnmounted(() => {
  cleanupEffects()
})
</script>

<style scoped>
.custom-page-wrapper {
  width: 100%;
}

.custom-sections-wrapper {
  width: 100%;
  margin: 60px 0;
  padding: 0;
}

.custom-section {
  margin-bottom: 50px;
}

.custom-section-title {
  background-color: #1e3a8a;
  color: white;
  text-align: center;
  padding: 15px 20px;
  font-size: 1.5rem;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 30px;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.custom-section-body {
  display: flex;
  flex-direction: row;
  gap: 40px;
  align-items: flex-start;
}

.custom-section-body.full-width {
  flex-direction: column;
}

.custom-section-media {
  flex: 0 0 40%;
  max-width: 40%;
}

.custom-section-media img,
.custom-section-media iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  border: 0;
  display: block;
}

.custom-section-media img {
  object-fit: contain;
  background-color: #f8fafc;
  border-radius: 16px;
}

.custom-section-content {
  flex: 1;
}

@media (max-width: 768px) {
  .custom-section-body {
    flex-direction: column;
  }
  .custom-section-media {
    max-width: 100%;
    flex: 0 0 100%;
  }
}

.hero-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #2b394f;
  background-image: 
    linear-gradient(45deg, rgba(0,0,0,0.1) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.1) 75%, rgba(0,0,0,0.1)), 
    linear-gradient(45deg, rgba(0,0,0,0.1) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.1) 75%, rgba(0,0,0,0.1));
  background-size: 400px 400px;
  background-position: 0 0, 200px 200px;
  padding: 4rem 10%;
  color: #ffffff;
  min-height: 280px;
}

.hero-banner.no-image {
  justify-content: center;
  text-align: center;
}

.hero-content {
  flex: 1;
  max-width: 60%;
}

.hero-banner.no-image .hero-content {
  max-width: 100%;
}

.hero-title {
  font-size: 2.4rem;
  font-weight: 500;
  line-height: 1.3;
  margin: 0;
  color: #ffffff;
}

.hero-image {
  flex: 0 0 35%;
  display: flex;
  justify-content: flex-end;
}

.hero-image img {
  max-width: 100%;
  max-height: 350px;
  object-fit: contain;
}

@media (max-width: 768px) {
  .hero-banner {
    flex-direction: column;
    text-align: center;
    padding: 3rem 5%;
  }
  .hero-content {
    max-width: 100%;
    margin-bottom: 2rem;
  }
  .hero-image {
    flex: 0 0 100%;
    justify-content: center;
  }
  .hero-title {
    font-size: 1.8rem;
  }
}

.hns-page-container {
  max-width: 1280px;
  margin: 0 auto;
  font-family: 'Inter', sans-serif;
  color: #111827;
}

.loading-state {
  text-align: center;
  padding: 4rem;
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

.active-page-view {
  display: flex;
  flex-direction: column;
}

.main-page-content {
  background: transparent;
  border: none;
  color: #334155;
  line-height: 1.8;
  font-size: 1.05rem;
  margin-bottom: 1.5rem;
}

.main-page-content h1,
.main-page-content h2,
.main-page-content h3 {
  color: #0f172a;
  font-weight: 700;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.main-page-content p {
  margin-bottom: 1.25rem;
}

.video-section,
.tab-media-wrapper,
.main-page-content iframe,
.section-html-content iframe {
  width: 100%;
  max-width: 900px;
  aspect-ratio: 16 / 9;
  border-radius: 16px;
  overflow: hidden;
  margin: 1.5rem auto 2.5rem auto;
  display: block;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s ease;
  background-color: #f8fafc;
}

.video-section,
.tab-media-wrapper iframe,
.main-page-content iframe,
.section-html-content iframe {
  background-color: #000;
}

.tab-media-wrapper img,
.tab-media-wrapper iframe {
  width: 100%;
  height: 100%;
  border: 0;
  display: block;
}

.tab-media-wrapper img {
  object-fit: contain;
}

.tab-media-wrapper:hover {
  transform: translateY(-8px) scale(1.01);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.video-section iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

.tab-layout.has-media {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2.5rem;
  align-items: start;
}

@media (min-width: 992px) {
  .tab-layout.has-media {
    grid-template-columns: 1fr 1fr;
  }
}

.tab-layout.has-media .tab-media-wrapper {
  margin: 0;
  max-width: 100%;
}

.horizontal-group {
  margin-bottom: 3rem;
}

.sections-navbar {
  display: flex;
  gap: 0;
  background: transparent;
  padding: 0;
  margin-bottom: 0;
  border-bottom: 1px solid #e2e8f0;
  overflow: visible;
}

.section-nav-link {
  background: transparent;
  border: none;
  border-bottom: 4px solid transparent;
  padding: 1rem 1.5rem;
  cursor: pointer;
  font-weight: 600;
  color: #334155;
  transition: all 0.2s;
  border-radius: 0;
  font-size: 0.95rem;
  position: relative;
  margin-bottom: -1px;
}

.section-nav-link:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.section-nav-link.active {
  background: #ffffff;
  color: #1e3a8a;
  border-bottom-color: #1e3a8a;
  box-shadow: none;
}

.horizontal-viewport {
  background: #ffffff;
  border: none;
  border-radius: 0 20px 20px 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.08);
  transition: all 0.4s ease;
  position: relative;
}

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
  padding: 0 2.5rem 2.5rem;
  background: #ffffff;
}

.section-html-content {
  color: #334155;
  line-height: 1.7;
}

.section-html-content > *:first-child {
  margin-top: 0;
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

.loading-state {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  color: #64748b;
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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
