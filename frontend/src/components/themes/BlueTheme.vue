<template>
  <div class="premium-theme-wrapper">
    <div class="card-container">

      <!-- Profile Header -->
      <div class="profile-header">
        <div class="avatar-wrap">
          <div class="avatar-ring">
            <img 
              :src="employee.image || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(employee.full_name || 'Employee') + '&background=ffffff&color=1a56db'" 
              :alt="employee.full_name" 
              class="avatar" 
            />
          </div>
        </div>
        <h1 class="name">{{ employee.full_name }}</h1>
        <p class="designation">{{ employee.designation }}</p>
        <p class="company">{{ employee.company }}</p>
      </div>

      <!-- Quick Contact Actions -->
      <div class="quick-contact">
        <a :href="'tel:' + (employee.phone || employee.mobile_no)" class="contact-pill" v-if="employee.phone || employee.mobile_no">
          <div class="pill-icon call-icon">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.03 21c.78 0 1-.6 1-1.15v-3.48c0-.54-.45-.99-.99-.99z"/></svg>
          </div>
          <span class="label">Call</span>
        </a>
        <a :href="'https://wa.me/' + (employee.mobile_no ? employee.mobile_no.replace(/\D/g,'') : '')" target="_blank" class="contact-pill" v-if="employee.mobile_no">
          <div class="pill-icon whatsapp-icon">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm5.46 14.19c-.23.64-1.32 1.22-1.93 1.34-.52.11-1.19.19-3.32-.69-2.73-1.13-4.51-3.93-4.64-4.11-.13-.17-1.11-1.48-1.11-2.82 0-1.34.7-2.02.95-2.28.24-.25.53-.31.71-.31.18 0 .35 0 .5.01.17.01.4 0 .62.54.23.57.77 1.87.84 2.01.07.14.12.31.02.5-.1.19-.15.31-.3.48-.15.17-.32.37-.45.5-.14.14-.3.29-.14.57.16.27.71 1.17 1.54 1.91 1.07.95 1.96 1.25 2.23 1.39.27.14.43.12.59-.06.16-.18.68-.8.86-1.07.18-.28.37-.24.62-.15.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.12.07.72-.16 1.36z"/></svg>
          </div>
          <span class="label">WhatsApp</span>
        </a>
        <a :href="'mailto:' + employee.email" class="contact-pill" v-if="employee.email">
          <div class="pill-icon email-icon">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
          </div>
          <span class="label">Email</span>
        </a>
        <a :href="employee.location || '#'" target="_blank" class="contact-pill" v-if="employee.location">
          <div class="pill-icon location-icon">
            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
          </div>
          <span class="label">Location</span>
        </a>
      </div>

      <!-- Social Media Section (Dynamic) -->
      <div class="social-wrapper" v-if="employee.social_media && employee.social_media.length > 0">
        <a v-for="social in employee.social_media" :key="social.name" :href="social.url" target="_blank" class="social-circle" :title="social.social_media">
          <div v-html="getSocialSvg(social.css_class)" class="social-svg-container"></div>
        </a>
      </div>

      <!-- Section: Personal Details -->
      <div class="premium-section">
        <div class="section-header">
          <h3>Personal Details</h3>
        </div>
        
        <div class="section-content">
          <div class="detail-row" v-if="employee.employee_number">
            <div class="detail-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 8h10M7 12h10M7 16h10"/></svg></div>
            <div class="detail-text">
              <span class="detail-val">{{ employee.employee_number }}</span>
              <span class="detail-lbl">Employee Number</span>
            </div>
          </div>
          <div class="detail-row" v-if="employee.department">
            <div class="detail-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M5 21V5a2 2 0 012-2h10a2 2 0 012 2v16M9 9h6M9 13h6M9 17h6"/></svg></div>
            <div class="detail-text">
              <span class="detail-val">{{ employee.department }}</span>
              <span class="detail-lbl">Department</span>
            </div>
          </div>
          <div class="detail-row" v-if="employee.gender">
            <div class="detail-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg></div>
            <div class="detail-text">
              <span class="detail-val">{{ employee.gender }}</span>
              <span class="detail-lbl">Gender</span>
            </div>
          </div>
          <div class="detail-row" v-if="employee.date_of_birth">
            <div class="detail-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg></div>
            <div class="detail-text">
              <span class="detail-val">{{ formatDate(employee.date_of_birth) }}</span>
              <span class="detail-lbl">Date of Birth</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Grouped Attachments (Dynamic) -->
      <template v-if="Object.keys(groupedAttachments).length > 0">
        <div class="premium-section" v-for="(typeGroups, typeName) in groupedAttachments" :key="typeName">

          
          <div class="section-content">
            <template v-for="(files, groupName) in typeGroups" :key="groupName">
              <h4 style="margin: 8px 0 12px; color: #3b82f6; font-size: 15px;">{{ groupName }}</h4>
              
              <!-- Image Gallery -->
              <div class="gallery-grid" v-if="files.some(f => isImage(f.attachment))">
                <template v-for="file in files" :key="file.name">
                  <a v-if="isImage(file.attachment)" :href="file.attachment" target="_blank" class="gallery-item">
                    <img :src="file.attachment" :alt="file.attachment.split('/').pop()" loading="lazy" />
                  </a>
                </template>
              </div>

              <!-- Document List -->
              <div class="document-list" v-if="files.some(f => !isImage(f.attachment))">
                <template v-for="file in files" :key="file.name + '-doc'">
                  <a class="document-card" v-if="!isImage(file.attachment)" :href="file.attachment" target="_blank">
                    <div class="doc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg></div>
                    <div class="doc-info">
                      <h4>{{ file.attachment.split('/').pop() }}</h4>
                    </div>
                    <div class="doc-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></div>
                  </a>
                </template>
              </div>
            </template>
          </div>
        </div>
      </template>


      <!-- QR Code Section -->
      <div class="premium-section" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
        <div class="section-header" style="justify-content: center;">
          <h3>Share VCard</h3>
        </div>
        <div class="qr-container" style="background: white; padding: 16px; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: inline-block;">
          <img :src="'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(currentUrl)" alt="QR Code" style="display: block; width: 160px; height: 160px;" />
        </div>
        <p style="color: #64748b; font-size: 14px; margin-top: 16px;">Scan to view this card on another device</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const currentUrl = computed(() => {
  return typeof window !== 'undefined' ? window.location.href : ''
})

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

const svgs = {
  'linkedin-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#0a66c2"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>',
  'facebook-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#1877f2"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg>',
  'twitter-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#1da1f2"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg>',
  'google-plus-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#db4437"><path d="M12.545,10.239v3.821h5.445c-0.712,2.315-2.647,3.972-5.445,3.972c-3.332,0-6.033-2.701-6.033-6.032 s2.701-6.032,6.033-6.032c1.498,0,2.866,0.549,3.921,1.453l2.814-2.814C17.503,2.988,15.139,2,12.545,2 C7.021,2,2.545,6.477,2.545,12s4.477,10,10,10c5.366,0,9.29-3.746,9.29-9.435c0-0.79-0.081-1.582-0.231-2.326H12.545z"/></svg>',
  'instagram-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#e1306c"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>',
  'youtube-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ff0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'
}

const getSocialSvg = (cssClass) => {
  return svgs[cssClass] || '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>'
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.premium-theme-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #f6f8fd 0%, #f1f5f9 100%);
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  box-sizing: border-box;
  color: #1e293b;
}

.card-container {
  background: #ffffff;
  width: 100%;
  max-width: 600px;
  border-radius: 32px;
  box-shadow: 0 24px 48px -12px rgba(15, 23, 42, 0.08), 0 12px 24px -8px rgba(15, 23, 42, 0.04);
  padding: 40px 30px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.8);
}

/* Profile Header */
.profile-header {
  text-align: center;
  margin-bottom: 32px;
}
.avatar-wrap {
  display: inline-flex;
  justify-content: center;
  margin-bottom: 20px;
}
.avatar-ring {
  padding: 4px;
  background: linear-gradient(45deg, #3b82f6, #8b5cf6);
  border-radius: 50%;
  box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2);
}
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
  border: 4px solid #fff;
}
.name {
  color: #0f172a;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0 0 6px;
}
.designation {
  color: #3b82f6;
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 6px;
}
.company {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Quick Contact */
.quick-contact {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 32px;
}
.contact-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  background: #f8fafc;
  padding: 12px 16px;
  border-radius: 20px;
  min-width: 80px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #f1f5f9;
}
.contact-pill:hover {
  transform: translateY(-4px);
  background: #ffffff;
  box-shadow: 0 12px 20px -8px rgba(59, 130, 246, 0.15);
  border-color: #e2e8f0;
}
.pill-icon {
  width: 24px;
  height: 24px;
  margin-bottom: 8px;
}
.call-icon { color: #10b981; }
.whatsapp-icon { color: #25D366; }
.email-icon { color: #f59e0b; }
.location-icon { color: #ef4444; }

.contact-pill .label {
  font-size: 12px;
  font-weight: 600;
  color: #475569;
}

/* Social Media Section */
.social-wrapper {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 40px;
  padding: 0 20px;
  flex-wrap: wrap;
}
.social-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #f1f5f9;
  transition: all 0.2s ease;
}
.social-circle:hover {
  background: #ffffff;
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 16px -4px rgba(15, 23, 42, 0.1);
  border-color: #e2e8f0;
}
.social-svg-container {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.social-svg-container :deep(svg) {
  width: 100%;
  height: 100%;
}

/* Sections */
.premium-section {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
}
.section-header {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}
.section-header h3 {
  color: #0f172a;
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.01em;
}

/* Content Details */
.section-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.detail-row {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 16px;
  transition: background 0.2s;
}
.detail-row:hover {
  background: #f1f5f9;
}
.detail-icon-wrap {
  width: 40px;
  height: 40px;
  background: #ffffff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: #3b82f6;
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

/* Gallery Grid */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 16px;
}
.gallery-item {
  display: block;
  border-radius: 16px;
  overflow: hidden;
  aspect-ratio: 1;
  position: relative;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}
.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}
.gallery-item:hover img {
  transform: scale(1.08);
}

/* Document List */
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
  border-radius: 16px;
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
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 14px;
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
.doc-info p {
  margin: 0;
  color: #64748b;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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

@media (max-width: 640px) {
  .premium-theme-wrapper {
    padding: 20px 10px;
  }
  .card-container {
    padding: 30px 20px;
    border-radius: 24px;
  }
  .quick-contact {
    gap: 12px;
  }
  .contact-pill {
    padding: 10px 12px;
    min-width: 70px;
  }
}
</style>
