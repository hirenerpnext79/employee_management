<template>
  <div class="about-page-wrapper">
    <div v-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="selectedPage" class="active-page-view">
      
      <!-- Hero Banner -->
      <div v-if="selectedPage.main_title" class="hero-banner">
        <div class="hero-content">
          <h1 class="hero-title">{{ selectedPage.main_title }}</h1>
        </div>
        <div class="hero-image" v-if="selectedPage.main_image">
          <img :src="selectedPage.main_image" alt="Main Title Image" />
        </div>
        <div class="hero-image-placeholder" v-else>
          <!-- Optional fallback if no image provided -->
        </div>
      </div>

      <div class="hns-about-container">
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
            <div class="tab-layout" :class="{ 'has-video': getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] || 0].video_url) }">
              <!-- Tab Video -->
              <div v-if="getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] || 0].video_url)" class="tab-video-wrapper">
                <iframe 
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
              <div class="tab-layout" :class="{ 'has-video': getEmbedUrl(group.vertical[activeVerticalIndices[group.name] || 0].video_url) }">
                <!-- Tab Video -->
                <div v-if="getEmbedUrl(group.vertical[activeVerticalIndices[group.name] || 0].video_url)" class="tab-video-wrapper">
                  <iframe 
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

      <!-- Static Premium Sections -->
      <AboutTestimonials />
      <AboutSolutions />
      <AboutFacts />
      <AboutIndustries />

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, computed } from 'vue'

import AboutTestimonials from './about_sections/AboutTestimonials.vue'
import AboutSolutions from './about_sections/AboutSolutions.vue'
import AboutFacts from './about_sections/AboutFacts.vue'
import AboutIndustries from './about_sections/AboutIndustries.vue'

const loading = ref(true)
const error = ref(null)
const selectedPage = ref(null)

const getEmbedUrl = (rawUrl) => {
  if (!rawUrl) return null;
  let url = rawUrl;
  
  // If user pasted a full iframe tag, extract the src attribute
  if (url.includes('<iframe')) {
    const match = url.match(/src=["'](.*?)["']/);
    if (match && match[1]) {
      url = match[1];
    } else {
      return null; // Invalid iframe
    }
  }
  
  // Convert standard watch link to embed link
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
  return sections
})

const fetchAboutData = async () => {
  const cacheKey = 'hns_page_About%20Us'
  const cachedContent = sessionStorage.getItem(cacheKey)
  
  if (cachedContent) {
    selectedPage.value = JSON.parse(cachedContent)
  }

  if (!cachedContent) {
    loading.value = true
  }
  
  error.value = null

  try {
    const res = await fetch('/api/method/web_pages.api.get_custom_web_pages?name=About%20Us')
    if (!res.ok) throw new Error('Failed to load page details')
    const data = await res.json()
    selectedPage.value = data.message || null
    
    if (data.message) {
      sessionStorage.setItem(cacheKey, JSON.stringify(data.message))
    }

    if (!selectedPage.value || ((!selectedPage.value.tabs || selectedPage.value.tabs.length === 0) && !selectedPage.value.content)) {
      if (!cachedContent) error.value = "No content found in the 'About Us' Custom Web Page."
    }
  } catch (e) {
    console.error(e)
    if (!cachedContent) error.value = "Failed to fetch About Us data from the server."
  } finally {
    loading.value = false
  }
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
      s.id = 'hns-dynamic-about-css-' + index
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

fetchAboutData()
</script>

<style scoped>
.about-page-wrapper {
  width: 100%;
}

.hero-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #2b394f; /* Matches premium dark blue from user image */
  background-image: 
    linear-gradient(45deg, rgba(0,0,0,0.1) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.1) 75%, rgba(0,0,0,0.1)), 
    linear-gradient(45deg, rgba(0,0,0,0.1) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.1) 75%, rgba(0,0,0,0.1));
  background-size: 400px 400px;
  background-position: 0 0, 200px 200px;
  padding: 4rem 10%;
  color: #ffffff;
  min-height: 280px;
}

.hero-content {
  flex: 1;
  max-width: 60%;
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

.hns-about-container {
  padding: 2rem;
  max-width: 1280px;
  margin: 0 auto;
  font-family: 'Inter', sans-serif;
  color: #111827;
}

.loading-state, .error-state {
  text-align: center;
  padding: 4rem;
  color: #6b7280;
}

.error-state {
  color: #ef4444;
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
  gap: 1.5rem;
}

.main-page-content {
  background: transparent;
  padding: 1rem 0 2rem 0;
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

/* Ensure iframes (videos) are responsive and visible */
.video-section,
.tab-video-wrapper,
.main-page-content iframe,
.section-html-content iframe {
  width: 100%;
  max-width: 900px;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  margin: 1.5rem auto 2.5rem auto;
  display: block;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-color: #000;
}

.tab-video-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.video-section iframe,
.tab-video-wrapper iframe {
  width: 100%;
  height: 100%;
  border: 0;
}

/* Tab Layout */
.tab-layout.has-video {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  align-items: start;
}

@media (min-width: 992px) {
  .tab-layout.has-video {
    grid-template-columns: 1fr 1fr;
  }
}

.tab-layout.has-video .tab-video-wrapper {
  margin: 0; /* Override the default centered margin so it fills the grid column */
  max-width: 100%;
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
