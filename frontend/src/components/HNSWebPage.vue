<template>
  <div class="custom-page-wrapper">
    <transition name="page-fade" mode="out-in">
      <div v-if="loading" class="loading-state" key="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      
            <div v-else-if="selectedPage" class="active-page-view" :key="selectedPage.name">
      
      <div class="hns-page-container" @click="handleHtmlClick" style="display: flex; flex-direction: column;">
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
      <div v-if="selectedPage.sections && selectedPage.sections.length > 0" class="custom-sections-wrapper" :style="{ order: selectedPage.section_sort_order || 0 }">
        <template v-for="(sec, idx) in selectedPage.sections" :key="'sec-'+idx">
          <div v-if="sec.is_display === 1" class="custom-section">
          <!-- Title Box -->
          <span class="custom-section-title" v-if="sec.page_title">{{ sec.page_title }}</span>

          <!-- Content Layout -->
          <div class="custom-section-body" :class="{ 'has-media': sec.image || getEmbedUrl(sec.video_url), 'has-both-media': sec.image && getEmbedUrl(sec.video_url), 'full-width': !sec.image && !getEmbedUrl(sec.video_url), 'media-right': sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right' && !(sec.image && getEmbedUrl(sec.video_url)) }">
            
            <div v-if="sec.image || (getEmbedUrl(sec.video_url) && !(sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'))" class="custom-section-media">
              
              <!-- BOTH EXIST -->
              <template v-if="sec.image && getEmbedUrl(sec.video_url)">
                <template v-if="(!sec.media_type || sec.media_type === 'Image')">
                   <template v-if="sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'">
                     <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                   </template>
                   <template v-else>
                     <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer"><img :src="sec.image" :alt="sec.page_title" /></a>
                     <img v-else :src="sec.image" :alt="sec.page_title" />
                   </template>
                </template>
                <template v-else-if="sec.media_type === 'Video'">
                   <template v-if="sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'">
                     <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer"><img :src="sec.image" :alt="sec.page_title" /></a>
                     <img v-else :src="sec.image" :alt="sec.page_title" />
                   </template>
                   <template v-else>
                     <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                   </template>
                </template>
              </template>
              
              <!-- ONLY ONE EXISTS -->
              <template v-else>
                <template v-if="sec.image">
                  <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer">
                    <img :src="sec.image" :alt="sec.page_title" />
                  </a>
                  <img v-else :src="sec.image" :alt="sec.page_title" />
                </template>
                <template v-else-if="getEmbedUrl(sec.video_url)">
                  <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </template>
              </template>

            </div>
            
            <div class="custom-section-content" v-html="sec.content"></div>
            
            <div v-if="(sec.image && getEmbedUrl(sec.video_url)) || (!sec.image && getEmbedUrl(sec.video_url) && sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right')" class="custom-section-media video-media">
                <!-- BOTH EXIST -->
                <template v-if="sec.image && getEmbedUrl(sec.video_url)">
                  <template v-if="(!sec.media_type || sec.media_type === 'Image')">
                     <template v-if="sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'">
                       <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer"><img :src="sec.image" :alt="sec.page_title" /></a>
                       <img v-else :src="sec.image" :alt="sec.page_title" />
                     </template>
                     <template v-else>
                       <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                     </template>
                  </template>
                  <template v-else-if="sec.media_type === 'Video'">
                     <template v-if="sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'">
                       <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                     </template>
                     <template v-else>
                       <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer"><img :src="sec.image" :alt="sec.page_title" /></a>
                       <img v-else :src="sec.image" :alt="sec.page_title" />
                     </template>
                  </template>
                </template>
                
                <!-- ONLY ONE EXISTS -->
                <template v-else>
                  <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </template>
            </div>

          </div>
          </div>
        </template>
      </div>

      <!-- Grouped Tabs Display -->
      <div class="tabs-wrapper" :style="{ order: selectedPage.tab_sort_order || 0 }">
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
                <template v-if="group.horizontal[activeHorizontalIndices[group.name] || 0].image">
                  <a v-if="group.horizontal[activeHorizontalIndices[group.name] || 0].image_click_url" :href="group.horizontal[activeHorizontalIndices[group.name] || 0].image_click_url" target="_blank" rel="noopener noreferrer">
                    <img :src="group.horizontal[activeHorizontalIndices[group.name] || 0].image" :alt="group.horizontal[activeHorizontalIndices[group.name] || 0].page_title" />
                  </a>
                  <img v-else :src="group.horizontal[activeHorizontalIndices[group.name] || 0].image" :alt="group.horizontal[activeHorizontalIndices[group.name] || 0].page_title" />
                </template>
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
                  <template v-if="group.vertical[activeVerticalIndices[group.name] || 0].image">
                    <a v-if="group.vertical[activeVerticalIndices[group.name] || 0].image_click_url" :href="group.vertical[activeVerticalIndices[group.name] || 0].image_click_url" target="_blank" rel="noopener noreferrer">
                      <img :src="group.vertical[activeVerticalIndices[group.name] || 0].image" :alt="group.vertical[activeVerticalIndices[group.name] || 0].page_title" />
                    </a>
                    <img v-else :src="group.vertical[activeVerticalIndices[group.name] || 0].image" :alt="group.vertical[activeVerticalIndices[group.name] || 0].page_title" />
                  </template>
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
      </div>
      
      <!-- Grouped Attachments (Dynamic) -->
      <div class="attachments-wrapper" :style="{ order: selectedPage.attachment_sort_order || 0 }">
      <template v-if="Object.keys(groupedAttachments).length > 0">
        <div class="attachment-section-container" v-for="(groupData, groupTitle) in groupedAttachments" :key="groupTitle">
          <!-- Main Title Banner -->
          <h2 class="custom-section-title" v-if="groupTitle !== 'Attachments' && groupTitle !== 'General'">
            {{ groupTitle }}
          </h2>
          
          <!-- General Links (Centered at top) -->
          <div class="attachment-general-links" v-if="groupData.general.length > 0" :style="{ '--attachment-cols': selectedPage?.attachment_across_page || 2 }">
            <template v-for="file in groupData.general" :key="file.name">
                <template v-if="isImage(file)">
                  <a v-if="file.image_click_url" :href="file.image_click_url" target="_blank" class="attachment-image-link">
                    <img :src="file.attachment" :alt="file.drive_label || file.pdf_label" class="attachment-preview-img" />
                  </a>
                  <img v-else :src="file.attachment" :alt="file.drive_label || file.pdf_label" class="attachment-preview-img standalone-img" />
                </template>
                <a v-else :href="file.attachment" target="_blank" class="attachment-link">
                  <span class="attachment-name">{{ file.drive_label || file.pdf_label || file.attachment.split('/').pop() }}</span>
                </a>
              </template>
          </div>

          <!-- Sub Groups (Columns) -->
          <div class="attachment-columns" :style="{ '--attachment-cols': Math.min(selectedPage?.attachment_across_page || 2, Object.keys(groupData.subGroups).length, getVisibleCount(groupTitle)) }" v-if="Object.keys(groupData.subGroups).length > 0">
              <div class="attachment-column" v-for="([subTitle, files]) in Object.entries(groupData.subGroups).slice(0, getVisibleCount(groupTitle))" :key="subTitle">
              <div class="column-header">
                <h3>{{ subTitle }}</h3>
              </div>
              <div class="column-links">
                <template v-for="file in files" :key="file.name">
                    <template v-if="isImage(file)">
                      <a v-if="file.image_click_url" :href="file.image_click_url" target="_blank" class="attachment-image-link">
                        <img :src="file.attachment" :alt="file.drive_label || file.pdf_label" class="attachment-preview-img" />
                      </a>
                      <img v-else :src="file.attachment" :alt="file.drive_label || file.pdf_label" class="attachment-preview-img standalone-img" />
                    </template>
                    <a v-else :href="file.attachment" target="_blank" class="attachment-link">
                      <span class="attachment-name">{{ file.drive_label || file.pdf_label || file.attachment.split('/').pop() }}</span>
                    </a>
                  </template>
              </div>
            </div>
          </div>
          
          <div class="show-more-container" v-if="Object.keys(groupData.subGroups).length > getDisplayLimit()">
            <button @click="showMoreGroups(groupTitle, Object.keys(groupData.subGroups).length)" class="show-more-btn" v-if="getVisibleCount(groupTitle) < Object.keys(groupData.subGroups).length">
              Show More
            </button>
            <button @click="showLessGroups(groupTitle)" class="show-more-btn" v-if="getVisibleCount(groupTitle) > getDisplayLimit()" style="margin-left: 10px;">
              Show Less
            </button>
          </div>
        </div>
      </template>
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

const isImage = (file) => {
  if (file && file.type === 'Image') return true;
  if (!file || !file.attachment) return false;
  const ext = file.attachment.split('.').pop().toLowerCase();
  return ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'].includes(ext);
}

const getFileIconSvg = (attachment, driveLabel) => {
  if (driveLabel || (attachment && attachment.includes('drive.google.com'))) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="file-icon drive-icon"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>`;
  }
  const ext = attachment ? attachment.split('.').pop().toLowerCase() : '';
  if (['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'].includes(ext)) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="file-icon image-icon"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>`;
  }
  if (['pdf'].includes(ext)) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="file-icon pdf-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><path d="M16 13H8"></path><path d="M16 17H8"></path><path d="M10 9H8"></path></svg>`;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="file-icon generic-icon"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>`;
}

const getDisplayLimit = () => {
  if (selectedPage.value?.display_attachment > 0) return selectedPage.value.display_attachment;
  return selectedPage.value?.attachment_across_page || 2;
}

const getVisibleCount = (groupTitle) => {
  if (expandedAttachmentGroups.value[groupTitle] !== undefined) {
    return expandedAttachmentGroups.value[groupTitle];
  }
  return getDisplayLimit();
}

const showMoreGroups = (groupTitle, total) => {
  const current = getVisibleCount(groupTitle);
  const step = getDisplayLimit();
  expandedAttachmentGroups.value[groupTitle] = Math.min(current + step, total);
}

const showLessGroups = (groupTitle) => {
  const step = getDisplayLimit();
  const current = getVisibleCount(groupTitle);
  expandedAttachmentGroups.value[groupTitle] = Math.max(current - step, step);
}

// Common handler for Show More/Less buttons in dynamic v-html content
const handleHtmlClick = (event) => {
  const btn = event.target.closest('.common-toggle-btn');
  if (btn) {
    const targetId = btn.getAttribute('data-target');
    if (targetId) {
      const content = document.getElementById(targetId);
      if (content) {
        if (content.style.display === "none" || content.style.display === "") {
          content.style.display = "block";
          btn.innerHTML = "Show Less";
        } else {
          content.style.display = "none";
          btn.innerHTML = "Show More";
        }
      }
    }
  }
}

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

let jsTimeout = null;

const applyStylesAndScripts = (sections) => {
  cleanupEffects()
  if (jsTimeout) clearTimeout(jsTimeout)

  if (selectedPage.value && selectedPage.value.css) {
    const s = document.createElement('style')
    s.id = 'hns-dynamic-page-main-css'
    s.textContent = selectedPage.value.css
    document.head.appendChild(s)
    styleTags.push(s)
  }

  if (sections && sections.length > 0) {
    sections.forEach((section, index) => {
      if (section.css) {
        const s = document.createElement('style')
        s.id = 'hns-dynamic-page-css-' + index
        s.textContent = section.css
        document.head.appendChild(s)
        styleTags.push(s)
      }
    })
  }

  jsTimeout = setTimeout(() => {
    if (selectedPage.value && selectedPage.value.js) {
      const script = document.createElement('script')
      script.id = 'hns-dynamic-page-main-js'
      script.textContent = `(async function() {\n  try {\n    ${selectedPage.value.js}\n  } catch(e) {\n    console.error("Error in main page dynamic JS:", e);\n  }\n})();`
      document.body.appendChild(script)
      scriptTags.push(script)
    }

    if (sections && sections.length > 0) {
      sections.forEach((section, index) => {
        if (section.js) {
          const script = document.createElement('script')
          script.id = 'hns-dynamic-page-js-' + index
          script.textContent = `(async function() {\n  try {\n    ${section.js}\n  } catch(e) {\n    console.error("Error in section dynamic JS:", e);\n  }\n})();`
          document.body.appendChild(script)
          scriptTags.push(script)
        }
      })
    }
  }, 400)
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

.custom-section-body.has-both-media {
  align-items: flex-start;
  gap: 0;
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

.custom-section-body.has-both-media .custom-section-media {
  flex: 1;
  max-width: 30%;
  display: flex;
  flex-direction: column;
}

.custom-section-body.has-both-media .custom-section-content {
  flex: 1.5;
  max-width: 100%;
  padding: 0 20px;
}

.custom-section-media img {
  width: 100%;
  height: auto;
  border: 0;
  display: block;
  border-radius: 16px;
}

.custom-section-media iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  border: 0;
  display: block;
  border-radius: 16px;
}

.custom-section-body.has-both-media .custom-section-media img,
.custom-section-body.has-both-media .custom-section-media iframe {
  flex: none;
  height: auto;
  aspect-ratio: 4 / 3;
  object-fit: contain;
}

.custom-section-content {
  flex: 1;
}

@media (max-width: 768px) {
  .custom-section-body,
  .custom-section-body.media-right,
  .custom-section-body.full-width {
    flex-direction: column;
  }
  .custom-section-media,
  .custom-section-body.has-both-media .custom-section-media,
  .custom-section-body.has-both-media .custom-section-content {
    max-width: 100%;
    flex: 0 0 100%;
    width: 100%;
    display: flex;
    justify-content: center;
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
.main-page-content iframe,
.section-html-content iframe {
  width: 100%;
  max-width: 900px;
  
  border-radius: 16px;
  overflow: hidden;
  margin: 1.5rem auto 2.5rem auto;
  display: block;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s ease;
  background-color: #f8fafc;
}

.tab-media-wrapper {
  width: 100%;
  max-width: 900px;
  border-radius: 16px;
  overflow: hidden;
  margin: 1.5rem auto 2.5rem auto;
  display: block;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s ease;
  background-color: #ffffff;
}

.video-section,
.tab-media-wrapper iframe,
.main-page-content iframe,
.section-html-content iframe {
  background-color: #000;
}

.tab-media-wrapper img {
  width: 100%;
  height: auto;
  border: 0;
  display: block;
}

.tab-media-wrapper iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  border: 0;
  display: block;
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
  padding: 2.5rem;
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
  object-fit: contain;
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
  display: grid;
  grid-template-columns: repeat(var(--attachment-cols, 2), minmax(0, 1fr));
  gap: 2rem;
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
  grid-template-columns: repeat(var(--attachment-cols, 2), minmax(0, 1fr));
  gap: 2rem;
  align-items: start;
}

@media (max-width: 768px) {
  .attachment-columns {
    grid-template-columns: 1fr !important;
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
  min-width: 0;
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

.attachment-image-link {
  display: block;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  text-decoration: none;
}

.attachment-preview-img {
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  border-radius: 8px;
  background-color: #f8f9fa;
  display: block !important;
  border-bottom: 1px solid #e2e8f0;
}
.attachment-image-label {
  padding: 10px 12px;
  font-weight: 500;
  font-size: 0.9rem;
  color: #334155;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.standalone-img {
  display: block;
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  object-fit: contain !important;
  border-radius: 8px;
  background-color: #f8f9fa;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  margin-bottom: 1rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
}

.attachment-general-links > * {
  min-width: 0;
}
</style>
