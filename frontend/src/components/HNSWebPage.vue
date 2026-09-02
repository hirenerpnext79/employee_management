<template>
  <div class="custom-page-wrapper">
    <transition name="page-fade" mode="out-in">
      <div v-if="loading" class="loading-state" key="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      
            <div v-else-if="selectedPage" class="active-page-view" :key="selectedPage.name">
      
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

      <!-- Custom Sections Display -->
      <div v-if="selectedPage.sections && selectedPage.sections.length > 0" class="custom-sections-wrapper">
        <div v-for="(sec, idx) in selectedPage.sections" :key="'sec-'+idx" class="custom-section">
          <!-- Title Box -->
          <span class="custom-section-title" v-if="sec.page_title">{{ sec.page_title }}</span>

          <!-- Content Layout -->
          <div class="custom-section-body" :class="{ 'has-media': sec.image || getEmbedUrl(sec.video_url), 'full-width': !sec.image && !getEmbedUrl(sec.video_url), 'media-right': sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right' }">
            
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


      
      <!-- Grouped Attachments (Dynamic) -->
      <template v-if="Object.keys(groupedAttachments).length > 0">
        <div class="attachment-section-container" v-for="(groupData, groupTitle) in groupedAttachments" :key="groupTitle">
          <!-- Main Title Banner -->
          <h2 class="custom-section-title" v-if="groupTitle !== 'Attachments' && groupTitle !== 'General'">
            {{ groupTitle }}
          </h2>
          
          <!-- General Links (Centered at top) -->
          <div class="attachment-general-links" v-if="groupData.general.length > 0">
            <a v-for="file in groupData.general" :key="file.name" :href="file.attachment" target="_blank" class="attachment-link">
              {{ file.drive_label || file.attachment.split('/').pop() }}
            </a>
          </div>

          <!-- Sub Groups (Columns) -->
          <div class="attachment-columns" v-if="Object.keys(groupData.subGroups).length > 0">
            <div class="attachment-column" v-for="([subTitle, files]) in Object.entries(groupData.subGroups).slice(0, expandedAttachmentGroups[groupTitle] ? undefined : 2)" :key="subTitle">
              <div class="column-header">
                <h3>{{ subTitle }}</h3>
              </div>
              <div class="column-links">
                <a v-for="file in files" :key="file.name" :href="file.attachment" target="_blank" class="attachment-link">
                  {{ file.drive_label || file.attachment.split('/').pop() }}
                </a>
              </div>
            </div>
          </div>
          
          <div class="show-more-container" v-if="Object.keys(groupData.subGroups).length > 2">
            <button @click="expandedAttachmentGroups[groupTitle] = !expandedAttachmentGroups[groupTitle]" class="show-more-btn">
              {{ expandedAttachmentGroups[groupTitle] ? 'Show Less' : 'Show More' }}
            </button>
          </div>
        </div>
      </template>

      <!-- Grouped Tabs Display -->
      <div v-for="(group, gIdx) in groupedTabs" :key="gIdx" class="tab-group-section">
        <h2 v-if="group.name && group.name !== 'Default Group'" class="custom-section-title">{{ group.name }}</h2>

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

      <!-- Optional Slot for Page-Specific Static Sections -->
      <slot name="after-sections"></slot>

      </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, computed, nextTick } from 'vue'
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






const groupedAttachments = computed(() => {
    const groups = {}
    if (selectedPage.value && selectedPage.value.attachment && Array.isArray(selectedPage.value.attachment)) {
      selectedPage.value.attachment.forEach(att => {
        const groupTitle = att.group_title || 'Attachments'
        if (!groups[groupTitle]) {
          groups[groupTitle] = {
            general: [],
            subGroups: {}
          }
        }
        
        if (att.group_sub_title) {
          if (!groups[groupTitle].subGroups[att.group_sub_title]) {
            groups[groupTitle].subGroups[att.group_sub_title] = []
          }
          groups[groupTitle].subGroups[att.group_sub_title].push(att)
        } else {
          groups[groupTitle].general.push(att)
        }
      })
    }
    return groups
  })



  const decodeHtml = (html) => {
    if (!html) return html;
    const txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
  }

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
const expandedAttachmentGroups = ref({})

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
    const res = await fetch(`/api/method/employee_management.api.get_custom_web_pages?name=${encodeURIComponent(name)}`)
    if (!res.ok) throw new Error('Failed to load page details')
    const data = await res.json()
    selectedPage.value = data.message || null
    
    if (data.message && Object.keys(data.message).length > 0) {
      if(data.message.section && !data.message.sections){data.message.sections=data.message.section;}
        if (data.message.content) data.message.content = decodeHtml(data.message.content);
        if (data.message.sections) {
          data.message.sections.forEach(s => {
            if (s.content) s.content = decodeHtml(s.content);
          });
        }
        if (data.message.tabs) {
          data.message.tabs.forEach(t => {
            if (t.content) t.content = decodeHtml(t.content);
          });
        }
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
  margin: 20px 0;
  padding: 0;
}

.custom-section-title {
    display: block;
    background-color: var(--section-title-color, #1e3a8a);
    color: var(--section-title-font-color, #ffffff);
    text-align: center;
    padding: 1.2rem 1rem;
    font-size: 1.5rem;
    font-weight: 700;
    text-transform: uppercase;
    margin: 0 0 30px 0 !important;
    border-radius: 6px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    width: 100%;
    box-sizing: border-box;
  }

.custom-section-body {
  display: flex;
  flex-direction: row;
  gap: 40px;
  align-items: flex-start;
}

.custom-section-body.media-right {
  flex-direction: row-reverse;
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
  background-color: var(--main-title-bg, #2b394f);
  background-image: 
    linear-gradient(45deg, rgba(0,0,0,0.1) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.1) 75%, rgba(0,0,0,0.1)), 
    linear-gradient(45deg, rgba(0,0,0,0.1) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.1) 75%, rgba(0,0,0,0.1));
  background-size: 400px 400px;
  background-position: 0 0, 200px 200px;
    padding: 4rem 10%;
    color: var(--main-title-font-color, #111827);
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
    color: var(--main-title-font-color, #111827);
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
  color: var(--tabs-font-color, #334155);
  transition: all 0.2s;
  border-radius: 0;
  font-size: 0.95rem;
  position: relative;
  margin-bottom: -1px;
}

.section-nav-link:hover {
  background: #f1f5f9;
}

.section-nav-link.active {
    background: #ffffff;
    color: var(--tabs-color, #1e3a8a);
    border-bottom-color: var(--tabs-color, #1e3a8a);
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
  color: var(--tabs-font-color, #334155);
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
  color: var(--tabs-color, #1e3a8a);
    border-left-color: var(--tabs-color, #1e3a8a);
}

.sidebar-nav-link.active .tab-icon {
    color: var(--tabs-color, #1e3a8a);
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

.custom-page-wrapper :deep(h1) { color: var(--h1-color, inherit); }
.custom-page-wrapper :deep(h2) { color: var(--h2-color, #ffffff); }
.custom-page-wrapper :deep(h3) { color: var(--h3-color, inherit); }
.custom-page-wrapper :deep(h4) { color: var(--h4-color, inherit); }
.custom-page-wrapper :deep(h5) { color: var(--h5-color, inherit); }
.custom-page-wrapper :deep(p) { color: var(--p-color, inherit); }

.premium-section {
  background: #ffffff;
  padding: 32px;
  border-radius: 12px;
  margin-top: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.section-header {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
}

.section-header.clickable {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: opacity 0.2s;
}
.section-header.clickable:hover {
  opacity: 0.8;
}

.section-header h3 {
  color: #0f172a;
  font-size: 18px;
  font-weight: 700;
  margin: 0;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chevron {
  transition: transform 0.3s ease;
  color: #64748b;
  display: flex;
  align-items: center;
}
.chevron.open {
  transform: rotate(180deg);
}
.collapsible-section .section-content {
  margin-top: 16px;
  animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.gallery-item {
  display: block;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 1;
  position: relative;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.gallery-item:hover img {
  transform: scale(1.08);
}

.document-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.document-card {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s;
}

.document-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
  transform: translateY(-2px);
}

.doc-icon {
  width: 48px;
  height: 48px;
  background: #f0f9ff;
  color: #0284c7;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.doc-icon svg {
  width: 24px;
  height: 24px;
}

.doc-info {
  flex: 1;
  overflow: hidden;
}

.doc-info h4 {
  margin: 0 0 4px;
  color: #0f172a;
  font-size: 15px;
  font-weight: 600;
}

.doc-arrow {
  color: #94a3b8;
  display: flex;
  align-items: center;
  margin-left: 12px;
}

.doc-arrow svg {
  width: 20px;
  height: 20px;
}

.attachment-section-container {
  margin: 3rem 0;
  font-family: inherit;
}
.attachment-main-banner {
  background-color: #032b5f;
  color: #ffffff;
  text-align: center;
  padding: 1.2rem;
  margin-bottom: 2rem;
}
.attachment-main-banner h2 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 1px;
}
.attachment-general-links {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
  margin-bottom: 3rem;
}
.attachment-link {
  color: #1e3a8a;
  text-decoration: underline;
  font-size: 0.95rem;
  transition: color 0.2s;
}
.attachment-link:hover {
  color: #1d4ed8;
}
.attachment-columns {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  align-items: start;
}

@media (max-width: 768px) {
  .attachment-columns {
    grid-template-columns: 1fr;
  }
}

.show-more-container {
  text-align: center;
  margin-top: 1.5rem;
}

.show-more-btn {
  background-color: #1e3a8a;
  color: white;
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
  font-size: 0.95rem;
}
.attachment-column {
  display: flex;
  flex-direction: column;
}
.column-header {
  background-color: #097ab0;
  color: #ffffff;
  text-align: center;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
.column-header h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
}
.column-links {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  padding: 0 0.5rem;
}

.custom-page-wrapper :deep(.domains-grid) {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  align-items: start;
}

.custom-page-wrapper :deep(.domain-item) {
  text-align: center;
  background: #ffffff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.custom-page-wrapper :deep(.domain-item h4) {
  margin-bottom: 12px;
  font-size: 1.1rem;
  color: #1e3a8a;
}

.custom-page-wrapper :deep(.domain-item img) {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
}

@media (max-width: 768px) {
  .custom-page-wrapper :deep(.domains-grid) {
    grid-template-columns: 1fr;
  }
}
</style>



