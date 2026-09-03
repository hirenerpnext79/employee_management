<template>
  <div class="card">
    <div class="topbar">
      <span>{{ employee.global_company_name ? employee.global_company_name.toUpperCase() : (employee.company ? employee.company.toUpperCase() : 'PROFILE') }}</span>
    </div>

    <div style="position: relative; margin-bottom: 50px;">
      <div class="banner" :style="employee.header_image ? { backgroundImage: 'url(' + employee.header_image + ')', backgroundSize: 'cover', backgroundPosition: 'center' } : {}">
      </div>
      <div class="avatar">
        <img v-if="employee.user_image || employee.user_photo" :src="employee.user_image || employee.user_photo" alt="User Photo" style="width:100%;height:100%;object-fit:contain;border-radius:12px;" />
        <svg v-else viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg>
      </div>
    </div>

    <div class="identity">
      <h1 class="name serif">{{ employee.full_name }}</h1>
      <div class="role">{{ employee.designation }}</div>
      <div class="co">{{ employee.global_company_name || employee.company }}</div>

            <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 10px;">
        <div class="contact-row" style="flex-direction: column; gap: 8px; margin-bottom: 0;">
        <span v-if="employee.phone">Call: <a :href="'tel:' + (employee.phone ? employee.phone.replace(/\D/g,'') : '')">{{ employee.phone }}</a></span>
        <span v-if="employee.mobile_no">WA: <a :href="'https://wa.me/' + (employee.mobile_no ? employee.mobile_no.replace(/\D/g,'') : '')">{{ employee.mobile_no }}</a></span>
        <span v-if="employee.email">Work: <a :href="'mailto:' + employee.email">{{ employee.email }}</a></span>
      </div>
        <div class="social-row" v-if="(employee.personal_social_media && employee.personal_social_media.length > 0) || employee.mobile_no">
        <a v-if="employee.mobile_no" :href="'https://wa.me/' + employee.mobile_no.replace(/\D/g,'')" target="_blank" title="WhatsApp" style="padding:8px; display:flex; align-items:center; justify-content:center;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#25D366" width="20" height="20"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.888-.788-1.487-1.761-1.659-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg></a>
          <a v-for="social in employee.personal_social_media" :key="social.name" :href="social.url" target="_blank" :title="social.social_media" @click="trackEvent('Click', social.social_media)" style="padding:8px" v-html="getSocialSvg(social.social_media.toLowerCase().replace(' ', '-') + '-icon')">
        </a>
      </div>
      </div>
    </div>

    <div class="body-grid">
      <div class="bio-panel" v-if="employee.about_myself || employee.about_us">
        <div ref="aboutTextRef" :class="['about-text-container', { 'expanded': isAboutExpanded }]" v-html="employee.about_myself || employee.about_us"></div>
        <button v-if="needsShowMore" class="show-more-btn" @click="isAboutExpanded = !isAboutExpanded">
          {{ isAboutExpanded ? 'Show Less' : 'Show More' }}
        </button>
      </div>
      <div class="side-panel">
        
        <div class="qr-box">
          <img :src="'https://api.qrserver.com/v1/create-qr-code/?size=130x130&data=' + encodeURIComponent(currentUrl)" alt="QR code">
        </div>
        <div class="scan-label">Scan to view</div>
        <a class="pill-btn solid" :href="'#/' + employee.company_page_route" target="_blank" v-if="employee.company_page_route">Company Page</a>
        <a class="pill-btn" :href="'#/' + employee.product_page_route" target="_blank" v-if="employee.product_page_route">Product Page</a>
          <a class="pill-btn solid" :href="'/api/method/employee_management.api.download_vcard?employee=' + employee.name" @click="trackEvent('Click', 'Save Contact')" style="margin-top: 10px; background: #ef4444 !important; color: #fff !important; border-color: #ef4444 !important;">Save Contact</a>
      </div>
    </div>

    <template v-if="Object.keys(groupedAttachments).length > 0">
      <template v-for="(typeGroups, typeName) in groupedAttachments" :key="typeName">
        <template v-for="(files, groupName) in typeGroups" :key="groupName">
          <div class="section" :style="files.some(f => isImage(f.attachment)) ? 'border-bottom:none;' : ''">
            <div class="sec-title">{{ typeName }}</div>
            <h2 class="sec-sub">{{ groupName }}</h2>
            
            <div class="gallery" v-if="files.some(f => isImage(f.attachment))">
              <template v-for="file in files" :key="file.name">
                <figure v-if="isImage(file.attachment)">
                  <a :href="file.attachment" target="_blank" @click="trackEvent('Click', 'Gallery Image')">
                    <img :src="file.attachment" :alt="file.attachment.split('/').pop()">
                  </a>
                </figure>
              </template>
            </div>

                        <div class="document-list premium-doc-list" v-if="files.some(f => !isImage(f.attachment))">
              <template v-for="file in files" :key="file.name + '-doc'">
                <a class="document-card premium-doc-card" v-if="!isImage(file.attachment)" :href="file.attachment" target="_blank">
                  <div class="doc-icon" :class="getDocIconClass(file.attachment)">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>
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
          </div>
        </template>
      </template>
    </template>

    <footer v-if="employee.company_social_media && employee.company_social_media.length > 0">
      <div class="fname">Company social media handles</div>
      <div class="fsoc">
        <a v-for="social in employee.company_social_media" :key="social.name" :href="social.url" target="_blank" :title="social.social_media" @click="trackEvent('Click', social.social_media)" style="padding:8px" v-html="getSocialSvg(social.social_media.toLowerCase().replace(' ', '-') + '-icon')">
        </a>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const svgs = {
  'facebook-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#1877f2"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>',
  'twitter-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#1da1f2"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>',
  'linkedin-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#0a66c2"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>',
  'instagram-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#e1306c"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>',
  'youtube-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#ff0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>',
  'location-icon': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="#ea4335"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>'
}

const getSocialSvg = (cssClass) => {
  return svgs[cssClass] || '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 014 10 15.3 15.3 0 01-4 10 15.3 15.3 0 01-4-10 15.3 15.3 0 014-10z"/></svg>'
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
  setTimeout(() => {
    if (aboutTextRef.value) {
      needsShowMore.value = aboutTextRef.value.scrollHeight > aboutTextRef.value.clientHeight;
    }
  }, 150);
  setTimeout(() => trackEvent('View'), 1000);
});

const currentUrl = computed(() => {
  return typeof window !== 'undefined' ? window.location.href : ''
})

const isAboutExpanded = ref(false)
const needsShowMore = ref(false)
const aboutTextRef = ref(null)

const props = defineProps({
  employee: {
    type: Object,
    required: true
  }
})


const getDocIconClass = (url) => {
  if (!url) return 'doc-icon-default'
  const ext = url.split('.').pop().toLowerCase()
  if (['pdf'].includes(ext)) return 'doc-icon-pdf'
  if (['doc', 'docx'].includes(ext)) return 'doc-icon-word'
  if (['xls', 'xlsx', 'csv'].includes(ext)) return 'doc-icon-excel'
  return 'doc-icon-default'
}

const isImage = (url) => {
  if (!url) return false
  const ext = url.split('.').pop().toLowerCase()
  return ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(ext)
}

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
  :root{
    --bg:#0B0E14;
    --panel:#12161F;
    --panel2:#161B26;
    --gold:#D2A857;
    --gold-soft:#8E7845;
    --text:#EDEEF2;
    --muted:#9199A8;
    --line:#242A38;
  }
  *{box-sizing:border-box;}
  .card{max-width:900px;margin:0 auto;background:#12161F;min-height:100vh;font-family:'Inter',sans-serif;color:#EDEEF2;}
  a{color:inherit;text-decoration:none;}
  .serif{font-family:'Playfair Display',serif;}

  .topbar{background:linear-gradient(90deg,#0B0E14,#171C28);padding:16px 36px;text-align:center;
    border-bottom:1px solid #242A38;}
  .topbar span{font-family:'Playfair Display',serif;font-size:15px;letter-spacing:.14em;color:#D2A857;text-transform:uppercase;}

  .banner{height:180px;position:relative;overflow:hidden;
    background:
      radial-gradient(circle at 20% 30%, rgba(210,168,87,.10), transparent 45%),
      radial-gradient(circle at 80% 70%, rgba(210,168,87,.08), transparent 50%),
      linear-gradient(135deg,#10131C,#1B2130 60%,#10131C);
  }
  .banner::after{content:'';position:absolute;inset:0;
    background-image:repeating-linear-gradient(45deg, rgba(210,168,87,.035) 0 2px, transparent 2px 40px);}
  .avatar{position:absolute;right:40px;bottom:-50px;width:130px;height:130px;border-radius:16px;
    background:#fff;display:flex;align-items:center;justify-content:center;
    box-shadow:0 10px 26px rgba(0,0,0,.15);padding:4px;box-sizing:border-box;}
  .avatar svg{width:56px;height:56px;color:#8E7845;}

  .identity{padding:56px 40px 26px;border-bottom:1px solid #242A38;}
  .identity .name{font-size:38px;margin:0 0 4px;color:#EDEEF2;}
  .identity .role{font-size:14px;color:#D2A857;letter-spacing:.03em;margin-bottom:2px;text-transform:uppercase;}
  .identity .co{font-size:13.5px;color:#9199A8;margin-bottom:18px;}

  .contact-row{display:flex;flex-wrap:wrap;gap:20px 32px;font-size:13.5px;color:#9199A8;margin-bottom:18px;}
  .contact-row a{color:#EDEEF2;}
  .contact-row a:hover{color:#D2A857;}

  .social-row{display:flex;gap:10px;flex-wrap:wrap;}
  .social-row a{width:38px;height:38px;border-radius:50%;border:1px solid #242A38;background:#161B26;
    display:flex;align-items:center;justify-content:center;font-size:11px;color:#9199A8;transition:.2s;font-weight:600;}
  .social-row a:hover{border-color:#D2A857;color:#D2A857;}

  .body-grid{display:grid;grid-template-columns:1.5fr 1fr;gap:0;border-bottom:1px solid #242A38;}
  .bio-panel{padding:34px 40px;border-right:1px solid #242A38;font-size:15px;line-height:1.85;color:#C9CDD6;}
  .bio-panel :deep(p){margin:0 0 16px;}
  .bio-panel :deep(b){color:#D2A857;font-weight:600;}

  .side-panel{padding:34px 32px;text-align:center;display:flex;flex-direction:column;align-items:center;}
  .qr-box{background:#fff;padding:14px;border-radius:14px;box-shadow:0 12px 30px rgba(0,0,0,.4);}
  .qr-box img{width:130px;height:130px;display:block;}
  .scan-label{font-size:12px;color:#9199A8;margin:14px 0 20px;letter-spacing:.03em;}
  .icon-row{display:flex;gap:10px;margin-bottom:20px;}
  .icon-btn{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;
    font-size:11px;border:1px solid #242A38;color:#9199A8;font-weight:700;}
  .icon-btn.wa{background:#25D366;color:#0B0E14;border-color:#25D366;}
  .pill-btn{width:100%;padding:13px;border-radius:8px;font-size:13px;font-weight:500;text-align:center;
    margin-bottom:10px;border:1px solid #8E7845;color:#D2A857;letter-spacing:.02em;display:block;}
  .pill-btn.solid{background:linear-gradient(90deg,#D2A857,#B7924A);color:#171307;border:none;font-weight:600;}

  .section{padding:34px 40px;border-bottom:1px solid #242A38;}
  .sec-title{font-size:12px;letter-spacing:.14em;color:#D2A857;margin-bottom:4px;text-transform:uppercase;}
  .sec-sub{font-family:'Playfair Display',serif;font-size:20px;margin:0 0 18px;color:#EDEEF2;}

  .file-row{display:flex;align-items:center;gap:16px;background:#161B26;border:1px solid #242A38;
    border-radius:10px;padding:16px 20px;transition:.2s;}
  .file-row:hover{border-color:#8E7845;}
  .file-icon{width:38px;height:38px;border-radius:8px;background:rgba(210,168,87,.12);color:#D2A857;
    display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;flex-shrink:0;}
  .file-name{font-size:14px;color:#EDEEF2;flex:1;}
  .chev{color:#9199A8;}

  .gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}
  .gallery figure{margin:0;border-radius:10px;overflow:hidden;border:1px solid #242A38;position:relative;}
  .gallery img{width:100%;height:140px;object-fit:cover;display:block;filter:saturate(1.05) contrast(1.03);}
  .gallery figure::after{content:'';position:absolute;inset:0;
    background:linear-gradient(to top, rgba(11,14,20,.5), transparent 55%);pointer-events:none;}

  footer{padding:30px 40px;text-align:center;}
  footer .fname{font-family:'Playfair Display',serif;font-size:15px;letter-spacing:.1em;color:#D2A857;margin-bottom:16px;text-transform:uppercase;}
  footer .fsoc{display:flex;justify-content:center;gap:10px;}
  footer .fsoc a{width:36px;height:36px;border-radius:50%;border:1px solid #242A38;
    display:flex;align-items:center;justify-content:center;font-size:11px;color:#9199A8;font-weight:600;}

  @media(max-width:700px){
    .body-grid{grid-template-columns:1fr;}
    .bio-panel{border-right:none;border-bottom:1px solid #242A38;}
    .gallery{grid-template-columns:1fr 1fr;}
    .identity .name{font-size:30px;}
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
  color: #D2A857 !important;
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
  min-width: 0;
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

</style>















