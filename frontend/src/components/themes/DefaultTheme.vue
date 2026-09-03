<template>
  <div class="premium-theme-wrapper">
    <!-- Top Brand Bar -->
    <div class="top-brand-bar">
      {{ employee.global_company_name ? employee.global_company_name.toUpperCase() : (employee.company ? employee.company.toUpperCase() : 'PROFILE') }}
    </div>

    <div class="card-container">
      <!-- Banner & Profile Picture -->
      <div class="banner-section">
        <img 
          :src="employee.banner_image || employee.header_image || employee.cover_image || 'https://images.unsplash.com/photo-1557683316-973673baf926?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'" 
          class="banner-image" 
          alt="Banner" 
        />
        <div class="profile-avatar-wrapper">
          <img 
            :src="employee.user_image || employee.image || employee.photo || employee.user_photo || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(employee.full_name || 'Employee') + '&background=ffffff&color=1a56db'" 
            :alt="employee.full_name" 
            class="profile-avatar" 
          />
        </div>
      </div>

      <!-- Profile Details (Split Layout) -->
      <div class="profile-main-split">
        
        <!-- Left Side: Details & Buttons -->
        <div class="profile-left">
          
          <div class="profile-info-and-social" style="display: flex; justify-content: space-between; align-items: flex-end; gap: 16px;">
            <div class="profile-info-text">
              <h1 class="name">{{ employee.full_name }}</h1>
              <h2 class="company">{{ employee.company }}</h2>
              <p class="designation">{{ employee.designation }}</p>

              <div class="contact-info-list" style="margin-bottom: 0;">
                <p v-if="employee.phone || employee.mobile_no">
                  Call : {{ employee.phone }} <span v-if="employee.phone && employee.mobile_no">/</span> WA : {{ employee.mobile_no }}
                </p>
                <p v-if="employee.email">Work: {{ employee.email }}</p>
                <p v-if="employee.personal_email">Personal: {{ employee.personal_email }}</p>
              </div>
            </div>

            <!-- Personal Social Media Inline -->
            <div class="social-section-inline" v-if="employee.personal_social_media && employee.personal_social_media.length > 0">
              <div class="social-wrapper" style="justify-content: flex-end; gap: 10px;">
                <a v-for="social in employee.personal_social_media" :key="'personal-'+social.name" :href="social.url" target="_blank" class="social-circle" :title="social.social_media" @click="trackEvent('Click', 'Personal ' + social.social_media)" style="width: 38px; height: 38px; min-width: 38px;">
                  <div v-html="getSocialSvg(social.css_class)" class="social-svg-container" style="width: 18px; height: 18px;"></div>
                </a>
              </div>
            </div>
          </div>

          <!-- About Myself Section -->
          <div class="about-myself-content" v-if="employee.about_myself || employee.about_us" style="margin-top: 24px; margin-bottom: 24px;">
            <div :class="['about-text-container', { 'expanded': isAboutExpanded }]" v-html="employee.about_myself || employee.about_us"></div>
            <button class="show-more-btn" @click="isAboutExpanded = !isAboutExpanded">
              {{ isAboutExpanded ? 'Show Less' : 'Show More' }}
            </button>
          </div>

        </div>

        <!-- Right Side: QR Code -->
        <div class="profile-right qr-inline">
          <!-- Quick Action Icons -->
          <div class="qr-actions" style="display: flex; gap: 12px; margin-bottom: 16px;">
            <a :href="'https://wa.me/' + (employee.mobile_no ? employee.mobile_no.replace(/\D/g,'') : '')" target="_blank" class="social-circle" v-if="employee.mobile_no" @click="trackEvent('Click', 'WhatsApp')" title="WhatsApp">
              <div class="social-svg-container"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#25D366"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg></div>
            </a>
            <a :href="'/api/method/employee_management.api.download_vcard?employee=' + employee.name" class="social-circle" @click="trackEvent('Click', 'Save Contact')" title="Save Contact">
              <div class="social-svg-container"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg></div>
            </a>
          </div>
          <div class="qr-container">
            <img :src="'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(currentUrl)" alt="QR Code" class="qr-image" />
          </div>
          <p class="qr-text">Scan to view</p>

          <!-- Action Buttons (Company & Product) -->
          <div class="action-buttons-grid" style="margin-top: 16px; width: 100%; display: flex; flex-direction: column; gap: 10px;">
            <a :href="'#/' + employee.company_page_route" target="_blank" class="btn-premium btn-company" v-if="employee.company_page_route" @click="trackEvent('Click', 'Company Page')" style="width: 100%;">
              Company Page
            </a>
            <a :href="'#/' + employee.product_page_route" target="_blank" class="btn-premium btn-company" v-if="employee.product_page_route" @click="trackEvent('Click', 'Product Page')" style="width: 100%;">
              Product Page
            </a>
          </div>
        </div>
      </div>





      <!-- Grouped Attachments (Dynamic) -->
      <template v-if="Object.keys(groupedAttachments).length > 0">
        <div class="premium-attachment-section" v-for="(typeGroups, typeName) in groupedAttachments" :key="typeName">
          <div class="section-header premium-accordion-header">
            <h3>{{ typeName || 'Attachments' }}</h3>
          </div>
          <div class="section-content premium-accordion-content">
            <template v-for="(files, groupName) in typeGroups" :key="groupName">
              <div class="premium-group-header">
                <span class="premium-group-badge">{{ groupName }}</span>
              </div>
              
              <!-- Image Gallery -->
              <div class="gallery-grid premium-gallery" v-if="files.some(f => isImage(f.attachment))">
                <template v-for="file in files" :key="file.name">
                  <a v-if="isImage(file.attachment)" :href="file.attachment" target="_blank" class="gallery-item premium-gallery-item" @click="trackEvent('Click', 'Gallery Image')" >
                    <img :src="file.attachment" :alt="file.attachment.split('/').pop()" loading="lazy" />
                    <div class="gallery-overlay">
                      <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
                    </div>
                  </a>
                </template>
              </div>

              <!-- Document List -->
              <div class="document-list premium-doc-list" v-if="files.some(f => !isImage(f.attachment))">
                <template v-for="file in files" :key="file.name + '-doc'">
                  <a class="document-card premium-doc-card" v-if="!isImage(file.attachment)"  :href="file.attachment" target="_blank">
                    <div class="doc-icon" :class="getDocIconClass(file.attachment)">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>
                    </div>
                    <div class="doc-info">
                      <h4 class="truncate-text" :title="file.attachment.split('/').pop()">{{ file.attachment.split('/').pop() }}</h4>
                      <p class="doc-meta">{{ file.attachment.split('.').pop().toUpperCase() }} Document</p>
                    </div>
                    <div class="doc-arrow">
                      <span class="view-text">View</span>
                      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    </div>
                  </a>
                </template>
              </div>
            </template>
          </div>
        </div>
      </template>

      <!-- Social Media Section (Company) -->
      <div class="premium-section social-section" v-if="employee.company_social_media && employee.company_social_media.length > 0" style="padding-top: 32px; border-top: 1px solid #f1f5f9;">
        <p class="social-heading">Company social media handles</p>
        <div class="social-wrapper">
          <a v-for="social in employee.company_social_media" :key="social.name" :href="social.url" target="_blank" class="social-circle" :title="social.social_media" @click="trackEvent('Click', social.social_media)" >
            <div v-html="getSocialSvg(social.css_class)" class="social-svg-container"></div>
          </a>
        </div>
      </div>

    </div>


  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const openSections = ref({})

const toggleSection = (sectionId) => {
  openSections.value[sectionId] = !openSections.value[sectionId]
}

const showAboutMyself = ref(false)
const toggleAboutMyself = () => {
  showAboutMyself.value = !showAboutMyself.value
  if (showAboutMyself.value) {
    trackEvent('Click', 'About Myself')
  }
}

const svgs = {
  'facebook-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#1877f2"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>',
  'twitter-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#1da1f2"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>',
  'linkedin-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0a66c2"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
  'instagram-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#e1306c"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>',
  'youtube-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ff0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>',
  'location-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ea4335"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'
}

const getSocialSvg = (cssClass) => {
  return svgs[cssClass] || '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>'
}

const trackEvent = (eventType, actionDetails = '') => {
  if (!props.employee || !props.employee.name) return;
  fetch('/api/method/employee_management.api.track_vcard_event', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({
      vcard: props.employee.name,
      event_type: eventType,
      action_details: actionDetails
    })
  }).catch(e => console.error(e));
};

onMounted(() => {
  setTimeout(() => trackEvent('View'), 1000);
});

const currentUrl = computed(() => {
  return typeof window !== 'undefined' ? window.location.href : ''
})

const isAboutExpanded = ref(false)

const props = defineProps({
  employee: {
    type: Object,
    required: true
  }
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const parts = dateStr.split('-')
  if (parts.length === 3) {
    return `${parts[2]}-${parts[1]}-${parts[0]}`
  }
  return dateStr
}

const isImage = (url) => {
  if (!url) return false
  const ext = url.split('.').pop().toLowerCase()
  return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext)
}





const getDocIconClass = (url) => {

  if (!url) return 'doc-icon-default'
  const ext = url.split('.').pop().toLowerCase()
  if (['pdf'].includes(ext)) return 'doc-icon-pdf'
  if (['doc', 'docx'].includes(ext)) return 'doc-icon-word'
  if (['xls', 'xlsx', 'csv'].includes(ext)) return 'doc-icon-excel'
  return 'doc-icon-default'
}

// Group attachments first by type, then by group_title

const groupedAttachments = computed(() => {
  const groups = {}
  if (props.employee.attachments && Array.isArray(props.employee.attachments)) {
    props.employee.attachments.forEach(attachment => {
      const typeName = attachment.type || 'Other'
      const groupName = attachment.group_title || 'General'
      
      if (!groups[typeName]) {
        groups[typeName] = {}
      }
      if (!groups[typeName][groupName]) {
        groups[typeName][groupName] = []
      }
      groups[typeName][groupName].push(attachment)
    })
  }
  return groups
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.premium-theme-wrapper {
  min-height: 100vh;
  width: 100%;
  background: #fbfbfd;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #1e293b;
  padding-bottom: 40px;
}

/* Top Brand Bar */
.top-brand-bar {
  width: 100%;
  background-color: #1e3a8a;
  color: #ffffff;
  text-align: center;
  padding: 12px 20px;
  font-weight: 700;
  font-size: 18px;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
  z-index: 10;
}

.card-container {
  width: 100%;
  max-width: 100%;
  background: #ffffff;
  min-height: 80vh;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

/* Banner Section */
.banner-section {
  position: relative;
  width: 100%;
  height: 220px;
  background: #f1f5f9;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Profile Avatar positioned inside/over the banner */
.profile-avatar-wrapper {
  position: absolute;
  bottom: -40px;
  right: 40px;
  width: 130px;
  height: 130px;
  border-radius: 8px; /* Slightly rounded square for a professional look */
  background: #ffffff;
  padding: 6px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  z-index: 2;
}

.profile-avatar {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 4px;
}

/* Split Layout */
.profile-main-split {
  padding: 50px 32px 32px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.profile-left {
  flex: 1;
  text-align: left;
}

.profile-right.qr-inline {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #f8fafc;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

.profile-right .qr-image {
  width: 140px;
  height: 140px;
}

.name {
  color: #1e3a8a; /* Deep premium blue */
  font-size: 32px;
  font-weight: 400;
  margin: 0 0 4px;
  letter-spacing: -0.5px;
}

.company {
  color: #042656;
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 6px;
}

.designation {
  color: #475569;
  font-size: 15px;
  font-weight: 500;
  margin: 0 0 24px;
}

/* Contact Info Text */
.contact-info-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 32px;
}

.contact-info-list p {
  margin: 0;
  color: #334155;
  font-size: 14px;
  font-weight: 500;
}

/* Action Buttons Grid */
.action-buttons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 24px;
}

.btn-premium {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 24px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s;
  border: none;
  cursor: pointer;
  width: 100%;
}

.btn-premium:hover {
  transform: translateY(-2px);
}

.btn-whatsapp {
  background-color: #25D366;
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(37, 211, 102, 0.3);
}
.btn-whatsapp:hover {
  background-color: #20b858;
  box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4);
}

.btn-company, .btn-about {
  background-color: #0284c7;
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(2, 132, 199, 0.3);
}
.btn-company:hover, .btn-about:hover {
  background-color: #0369a1;
  box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4);
}

.btn-save {
  background-color: #ef4444;
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.3);
}
.btn-save:hover {
  background-color: #dc2626;
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
}

/* About Myself Content */
.about-myself-content {
  margin-top: 24px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  color: #334155;
  font-size: 14px;
  line-height: 1.6;
  text-align: left;
}
.about-myself-content :deep(p) {
  margin-top: 0;
}
.about-myself-content :deep(p:last-child) {
  margin-bottom: 0;
}

/* Social Media Section */
.social-section {
  padding: 0 32px 40px;
  text-align: center;
}

.social-heading {
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 16px;
}

.social-wrapper {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.social-circle {
  width: 44px;
  height: 44px;
  border-radius: 8px; /* Square with rounded corners to match avatar */
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.social-circle:hover {
  background: #f8fafc;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.08);
  border-color: #cbd5e1;
}

.social-svg-container {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.social-svg-container :deep(svg) {
  width: 100%;
  height: 100%;
}

/* Other Sections (Personal details, attachments, QR) */
.premium-section {
  background: #ffffff;
  border-top: 1px solid #f1f5f9;
  padding: 32px;
}

.section-header {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
}

.section-header.justify-center {
  justify-content: center;
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

.detail-row {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  background: #f8fafc;
  border-radius: 12px;
  transition: background 0.2s;
  border: 1px solid #f1f5f9;
}

.detail-row:hover {
  background: #f1f5f9;
}

.detail-icon-wrap {
  width: 40px;
  height: 40px;
  background: #ffffff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: #0284c7;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.detail-icon-wrap svg {
  width: 20px;
  height: 20px;
}

.detail-text {
  display: flex;
  flex-direction: column;
}

.detail-val {
  color: #1e293b;
  font-weight: 600;
  font-size: 15px;
}

.detail-lbl {
  color: #64748b;
  font-size: 13px;
  margin-top: 2px;
}

/* Gallery and Docs */
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

/* Accordion Specific */
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

@media (max-width: 640px) {
  .banner-section {
    height: 180px;
  }
  .profile-avatar-wrapper {
    right: 50%;
    transform: translateX(50%);
    bottom: -50px;
    z-index: 10;
  }
  .profile-main-split {
    flex-direction: column;
    align-items: center;
    padding-top: 60px;
  }
  .profile-left {
    text-align: center;
    width: 100%;
  }
  .profile-info-and-social {
    flex-direction: column !important;
    align-items: center !important;
  }
  .contact-info-list {
    margin-bottom: 24px !important;
  }
  .action-buttons-grid {
    grid-template-columns: 1fr; 
    max-width: 320px;
    margin: 24px auto 0;
  }
  .name {
    font-size: 26px;
  }
}

/* Premium Attachments Specifics */
.premium-attachment-section {
  padding: 24px 32px;
  background: #ffffff;
  border-radius: 16px;
  margin: 24px 0;
  box-shadow: 0 4px 24px rgba(0,0,0,0.03);
  border: 1px solid #f1f5f9;
}
@media (max-width: 640px) {
  .premium-attachment-section {
    padding: 20px;
    margin: 16px 0;
  }
}

.premium-accordion-header {
  padding: 8px 0;
}
.premium-accordion-header h3 {
  font-size: 18px;
  color: #0f172a;
  letter-spacing: -0.3px;
  font-weight: 700;
}
.premium-accordion-header .chevron {
  background: #f8fafc;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: all 0.3s ease;
}
.premium-accordion-header:hover .chevron {
  background: #e2e8f0;
  color: #334155;
}

.premium-group-header {
  margin: 24px 0 16px;
  position: relative;
}
.premium-group-badge {
  display: inline-block;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #0284c7;
  font-weight: 700;
  padding: 6px 14px;
  background: #f0f9ff;
  border-radius: 20px;
  border: 1px solid #e0f2fe;
}

.premium-doc-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
.premium-doc-card {
  padding: 16px 20px;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  display: flex;
  align-items: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
}
.premium-doc-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.06);
  border-color: #cbd5e1;
}

.premium-doc-card .doc-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  transition: transform 0.3s ease;
  flex-shrink: 0;
}
.premium-doc-card:hover .doc-icon {
  transform: scale(1.05) rotate(-3deg);
}

.doc-icon-pdf { background: #fef2f2; color: #ef4444; }
.doc-icon-word { background: #eff6ff; color: #3b82f6; }
.doc-icon-excel { background: #f0fdf4; color: #22c55e; }
.doc-icon-default { background: #f8fafc; color: #64748b; }

.premium-doc-card .doc-info {
  flex: 1;
  min-width: 0; /* for truncation */
}
.premium-doc-card .doc-info h4 {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px;
  line-height: 1.3;
}
.truncate-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.premium-doc-card .doc-info .doc-meta {
  font-size: 12px;
  color: #64748b;
  margin: 0;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.premium-doc-card .doc-arrow {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #0ea5e9;
  font-weight: 600;
  font-size: 14px;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}
.premium-doc-card:hover .doc-arrow {
  opacity: 1;
  transform: translateX(0);
}
.doc-arrow .view-text {
  display: none;
}
@media (min-width: 768px) {
  .doc-arrow .view-text {
    display: inline-block;
  }
}

.premium-gallery {
  gap: 20px;
}
.premium-gallery-item {
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.04);
  position: relative;
  overflow: hidden;
}
.premium-gallery-item img {
  border-radius: 16px;
  transition: transform 0.5s ease;
}
.gallery-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: all 0.3s ease;
  backdrop-filter: blur(2px);
  border-radius: 16px;
}
.premium-gallery-item:hover .gallery-overlay {
  opacity: 1;
}
.premium-gallery-item:hover img {
  transform: scale(1.1);
}


.about-text-container {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: all 0.3s ease;
}
.about-text-container.expanded {
  -webkit-line-clamp: unset;
}
.show-more-btn {
  background: none;
  border: none;
  color: #0284c7;
  opacity: 1;
  cursor: pointer;
  padding: 0;
  margin-top: 8px;
  font-weight: 600;
  font-size: 13.5px;
  text-decoration: underline;
}
.show-more-btn:hover {
  opacity: 1;
}
</style>

