<template>
  <div class="custom-page-wrapper">
    <transition name="page-fade" mode="out-in">
      <div v-if="loading" class="loading-state" key="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      
            <div v-else-if="selectedPage" class="active-page-view" :key="selectedPage.name">
      <!-- Password Login Gate -->
      <div v-if="isProtected && !isAuthorized" class="page-password-gate">
        <div class="password-card">
          <!-- Top decorative gradient line -->
          <div class="card-accent-bar"></div>

          <!-- Lock Icon Badge with glowing ambient halo -->
          <div class="lock-icon-badge-wrapper">
            <div class="lock-icon-badge">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
          </div>

          <!-- Restricted Tag -->
          <div class="restricted-tag">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h2v-2h-2v2zm0-4h2V7h-2v6z"/>
            </svg>
            <span>Protected Page</span>
          </div>

          <!-- Title -->
          <h2 class="password-title">{{ selectedPage?.title || selectedPage?.name || 'Protected Content' }}</h2>
          <p class="password-desc">This content is password protected. Please enter your password to view this page.</p>

          <!-- Error Alert -->
          <transition name="alert-fade">
            <div v-if="passwordError" class="password-error-alert">
              <svg class="error-alert-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <span>{{ passwordError }}</span>
            </div>
          </transition>

          <!-- Password Form -->
          <form @submit.prevent="submitPassword" class="password-form">
            <div class="password-input-group">
              <span class="input-left-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 2l-2 2m-1.5 1.5L16 7l-2-2m-1.5 1.5L11 8l-2-2m-2 4a5 5 0 1 0 7.07 7.07l7.93-7.93a1 1 0 0 0 0-1.42l-2.65-2.65a1 1 0 0 0-1.42 0L14 7"></path>
                </svg>
              </span>
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="enteredPassword"
                placeholder="Enter password..."
                class="password-field"
                autofocus
                required
              />
              <button 
                type="button" 
                class="eye-toggle-btn" 
                @click="showPassword = !showPassword" 
                :title="showPassword ? 'Hide password' : 'Show password'"
                tabindex="-1"
              >
                <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                  <line x1="1" y1="1" x2="23" y2="23"></line>
                </svg>
              </button>
            </div>

            <button type="submit" class="password-submit-btn" :disabled="authenticating">
              <span v-if="!authenticating" class="btn-inner">
                <span>Access Page</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </span>
              <span v-else class="btn-spinner-wrap">
                <span class="password-spinner"></span>
                <span>Verifying...</span>
              </span>
            </button>
          </form>

          <!-- Back Link -->
          <div class="card-footer-links">
            <a href="#/" class="back-home-link">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
              </svg>
              <span>Return to Home</span>
            </a>
          </div>
        </div>
      </div>

      <div v-else class="hns-page-container" @click="handleHtmlClick" style="display: flex; flex-direction: column;">
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
        <template v-for="(groupSections, groupName) in groupedSections" :key="groupName">
          <!-- Main Title Box -->
          <h2 class="custom-section-title" v-if="groupName !== 'Default Group'" style="margin-bottom: 10px;">{{ groupName }}</h2>
          
          <template v-for="(sec, idx) in groupSections" :key="'sec-'+idx">
            <div v-if="sec.is_display === 1" class="custom-section">
            <!-- Sub Title Box -->
            <h3 class="custom-section-subtitle" v-if="sec.page_title">
              {{ sec.page_title }}
            </h3>

          <!-- Content Layout -->
          <div class="custom-section-body" :class="{ 'has-media': sec.image || getEmbedUrl(sec.video_url), 'has-both-media': sec.image && getEmbedUrl(sec.video_url), 'full-width': !sec.image && !getEmbedUrl(sec.video_url), 'media-right': sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right' && !(sec.image && getEmbedUrl(sec.video_url)) }">
            
            <div v-if="(sec.image && !isImageFailed(sec.image)) || (getEmbedUrl(sec.video_url) && !(sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'))" class="custom-section-media">
              
              <!-- BOTH EXIST -->
              <template v-if="sec.image && getEmbedUrl(sec.video_url)">
                <template v-if="(!sec.media_type || sec.media_type === 'Image')">
                   <template v-if="sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'">
                     <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                   </template>
                   <template v-else>
<div class="custom-media-card">
  <div class="media-preview-container">
    <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </a>
    <template v-else>
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </template>
  </div>
  <div v-if="sec.image && !isImageFailed(sec.image) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
    <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
      <span>{{ sec.image_text }}</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
    </a>
  </div>
</div>
                   </template>
                </template>
                <template v-else-if="sec.media_type === 'Video'">
                   <template v-if="sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'">
<div class="custom-media-card">
  <div class="media-preview-container">
    <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </a>
    <template v-else>
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </template>
  </div>
  <div v-if="sec.image && !isImageFailed(sec.image) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
    <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
      <span>{{ sec.image_text }}</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
    </a>
  </div>
</div>
                   </template>
                   <template v-else>
                     <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                   </template>
                </template>
              </template>
              
              <!-- ONLY ONE EXISTS -->
              <template v-else>
                <template v-if="sec.image">
<div class="custom-media-card">
  <div class="media-preview-container">
    <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </a>
    <template v-else>
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </template>
  </div>
  <div v-if="sec.image && !isImageFailed(sec.image) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
    <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
      <span>{{ sec.image_text }}</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
    </a>
  </div>
</div>
                </template>
                <template v-else-if="getEmbedUrl(sec.video_url)">
                  <iframe :src="getEmbedUrl(sec.video_url)" title="Video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </template>
              </template>

            </div>
            
            <div class="custom-section-content" v-html="sec.content"></div>
            
            <div v-if="(sec.image && !isImageFailed(sec.image) && getEmbedUrl(sec.video_url)) || (!sec.image && getEmbedUrl(sec.video_url) && sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right')" class="custom-section-media video-media">
                <!-- BOTH EXIST -->
                <template v-if="sec.image && getEmbedUrl(sec.video_url)">
                  <template v-if="(!sec.media_type || sec.media_type === 'Image')">
                     <template v-if="sec.imagevideo_position && sec.imagevideo_position.toLowerCase() === 'right'">
<div class="custom-media-card">
  <div class="media-preview-container">
    <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </a>
    <template v-else>
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </template>
  </div>
  <div v-if="sec.image && !isImageFailed(sec.image) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
    <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
      <span>{{ sec.image_text }}</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
    </a>
  </div>
</div>
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
<div class="custom-media-card">
  <div class="media-preview-container">
    <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </a>
    <template v-else>
      <img 
        v-if="!isImageFailed(sec.image)" 
        :src="sec.image" 
        :alt="sec.page_title || 'Image'" 
        class="custom-media-img"
        @error="handleImageError(sec.image)"
      />
      <div v-else class="media-placeholder-box">
        <div class="placeholder-icon-wrap">
          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
        </div>
        <span class="placeholder-title">{{ sec.page_title || 'Image' }}</span>
      </div>
    </template>
  </div>
  <div v-if="sec.image && !isImageFailed(sec.image) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
    <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
      <span>{{ sec.image_text }}</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
    </a>
  </div>
</div>
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
                  <a v-if="group.horizontal[activeHorizontalIndices[group.name] || 0].image_click_url" :href="group.horizontal[activeHorizontalIndices[group.name] || 0].image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
                    <img 
                      v-if="!isImageFailed(group.horizontal[activeHorizontalIndices[group.name] || 0].image)" 
                      :src="group.horizontal[activeHorizontalIndices[group.name] || 0].image" 
                      :alt="group.horizontal[activeHorizontalIndices[group.name] || 0].page_title || 'Image'" 
                      class="custom-media-img"
                      @error="handleImageError(group.horizontal[activeHorizontalIndices[group.name] || 0].image)"
                    />
                    <div v-else class="media-placeholder-box">
                      <div class="placeholder-icon-wrap">
                        <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                          <circle cx="8.5" cy="8.5" r="1.5"></circle>
                          <polyline points="21 15 16 10 5 21"></polyline>
                        </svg>
                      </div>
                      <span class="placeholder-title">{{ group.horizontal[activeHorizontalIndices[group.name] || 0].page_title || 'Image' }}</span>
                    </div>
                  </a>
                  <template v-else>
                    <img 
                      v-if="!isImageFailed(group.horizontal[activeHorizontalIndices[group.name] || 0].image)" 
                      :src="group.horizontal[activeHorizontalIndices[group.name] || 0].image" 
                      :alt="group.horizontal[activeHorizontalIndices[group.name] || 0].page_title || 'Image'" 
                      class="custom-media-img"
                      @error="handleImageError(group.horizontal[activeHorizontalIndices[group.name] || 0].image)"
                    />
                    <div v-else class="media-placeholder-box">
                      <div class="placeholder-icon-wrap">
                        <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                          <circle cx="8.5" cy="8.5" r="1.5"></circle>
                          <polyline points="21 15 16 10 5 21"></polyline>
                        </svg>
                      </div>
                      <span class="placeholder-title">{{ group.horizontal[activeHorizontalIndices[group.name] || 0].page_title || 'Image' }}</span>
                    </div>
                  </template>
                  <div v-if="group.horizontal[activeHorizontalIndices[group.name] || 0].image && !isImageFailed(group.horizontal[activeHorizontalIndices[group.name] || 0].image) && group.horizontal[activeHorizontalIndices[group.name] || 0].image_click_url && group.horizontal[activeHorizontalIndices[group.name] || 0].image_text" class="image-text-link-wrapper">
                    <a :href="group.horizontal[activeHorizontalIndices[group.name] || 0].image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                      <span>{{ group.horizontal[activeHorizontalIndices[group.name] || 0].image_text }}</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                    </a>
                  </div>
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

            <!-- Price Tag (Bottom Right) -->
            <div class="tab-price-bottom" v-if="priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code] && priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].selling_rate">
              <div class="price-badge">
                <template v-if="priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].special_discount">
                  <span class="price-original">₹{{ priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].selling_rate.toFixed(2) }}</span>
                  <span class="price-special">₹{{ priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].special_discount.toFixed(2) }}</span>
                  <span class="price-discount">({{ (((priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].selling_rate - priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].special_discount) / priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].selling_rate) * 100).toFixed(0) }}% OFF)</span>
                </template>
                <template v-else>
                  <span class="price-selling">₹{{ priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].selling_rate.toFixed(2) }}</span>
                </template>
                <div class="price-info-wrapper" v-if="priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].short_description">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                  <div class="price-info-tooltip" v-html="priceListMap[group.horizontal[activeHorizontalIndices[group.name] || 0].tab_code].short_description"></div>
                </div>
              </div>
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
                    <a v-if="group.vertical[activeVerticalIndices[group.name] || 0].image_click_url" :href="group.vertical[activeVerticalIndices[group.name] || 0].image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
                      <img 
                        v-if="!isImageFailed(group.vertical[activeVerticalIndices[group.name] || 0].image)" 
                        :src="group.vertical[activeVerticalIndices[group.name] || 0].image" 
                        :alt="group.vertical[activeVerticalIndices[group.name] || 0].page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(group.vertical[activeVerticalIndices[group.name] || 0].image)"
                      />
                      <div v-else class="media-placeholder-box">
                        <div class="placeholder-icon-wrap">
                          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                          </svg>
                        </div>
                        <span class="placeholder-title">{{ group.vertical[activeVerticalIndices[group.name] || 0].page_title || 'Image' }}</span>
                      </div>
                    </a>
                    <template v-else>
                      <img 
                        v-if="!isImageFailed(group.vertical[activeVerticalIndices[group.name] || 0].image)" 
                        :src="group.vertical[activeVerticalIndices[group.name] || 0].image" 
                        :alt="group.vertical[activeVerticalIndices[group.name] || 0].page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(group.vertical[activeVerticalIndices[group.name] || 0].image)"
                      />
                      <div v-else class="media-placeholder-box">
                        <div class="placeholder-icon-wrap">
                          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                          </svg>
                        </div>
                        <span class="placeholder-title">{{ group.vertical[activeVerticalIndices[group.name] || 0].page_title || 'Image' }}</span>
                      </div>
                    </template>
                    <div v-if="group.vertical[activeVerticalIndices[group.name] || 0].image && !isImageFailed(group.vertical[activeVerticalIndices[group.name] || 0].image) && group.vertical[activeVerticalIndices[group.name] || 0].image_click_url && group.vertical[activeVerticalIndices[group.name] || 0].image_text" class="image-text-link-wrapper">
                      <a :href="group.vertical[activeVerticalIndices[group.name] || 0].image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                        <span>{{ group.vertical[activeVerticalIndices[group.name] || 0].image_text }}</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                      </a>
                    </div>
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

              <!-- Price Tag (Bottom Right) -->
              <div class="tab-price-bottom" v-if="priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code] && priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].selling_rate">
                <div class="price-badge">
                  <template v-if="priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].special_discount">
                    <span class="price-original">₹{{ priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].selling_rate.toFixed(2) }}</span>
                    <span class="price-special">₹{{ priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].special_discount.toFixed(2) }}</span>
                    <span class="price-discount">({{ (((priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].selling_rate - priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].special_discount) / priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].selling_rate) * 100).toFixed(0) }}% OFF)</span>
                  </template>
                  <template v-else>
                    <span class="price-selling">₹{{ priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].selling_rate.toFixed(2) }}</span>
                  </template>
                  <div class="price-info-wrapper" v-if="priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].short_description">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    <div class="price-info-tooltip" v-html="priceListMap[group.vertical[activeVerticalIndices[group.name] || 0].tab_code].short_description"></div>
                  </div>
                </div>
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
                <div v-if="isImage(file)" class="attachment-image-block">
                  <div class="attachment-image-card">
                    <a v-if="file.image_click_url" :href="file.image_click_url" target="_blank" class="attachment-image-link">
                      <img 
                        v-if="!isImageFailed(file.attachment)" 
                        :src="file.attachment" 
                        :alt="file.drive_label || file.pdf_label || 'Attachment'" 
                        class="attachment-preview-img"
                        @error="handleImageError(file.attachment)"
                      />
                      <div v-else class="media-placeholder-box attachment-placeholder">
                        <div class="placeholder-icon-wrap">
                          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                          </svg>
                        </div>
                        <span class="placeholder-title">{{ file.drive_label || file.pdf_label || 'Attachment' }}</span>
                      </div>
                    </a>
                    <template v-else>
                      <img 
                        v-if="!isImageFailed(file.attachment)" 
                        :src="file.attachment" 
                        :alt="file.drive_label || file.pdf_label || 'Attachment'" 
                        class="attachment-preview-img standalone-img"
                        @error="handleImageError(file.attachment)"
                      />
                      <div v-else class="media-placeholder-box attachment-placeholder">
                        <div class="placeholder-icon-wrap">
                          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                          </svg>
                        </div>
                        <span class="placeholder-title">{{ file.drive_label || file.pdf_label || 'Attachment' }}</span>
                      </div>
                    </template>
                    <div v-if="file.attachment && !isImageFailed(file.attachment) && file.image_click_url && file.image_text" class="image-text-link-wrapper">
                      <a :href="file.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                        <span>{{ file.image_text }}</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                      </a>
                    </div>
                  </div>
                </div>
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
                    <div v-if="isImage(file)" class="attachment-image-block">
                      <div class="attachment-image-card">
                        <a v-if="file.image_click_url" :href="file.image_click_url" target="_blank" class="attachment-image-link">
                          <img 
                            v-if="!isImageFailed(file.attachment)" 
                            :src="file.attachment" 
                            :alt="file.drive_label || file.pdf_label || 'Attachment'" 
                            class="attachment-preview-img"
                            @error="handleImageError(file.attachment)"
                          />
                          <div v-else class="media-placeholder-box attachment-placeholder">
                            <div class="placeholder-icon-wrap">
                              <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                <polyline points="21 15 16 10 5 21"></polyline>
                              </svg>
                            </div>
                            <span class="placeholder-title">{{ file.drive_label || file.pdf_label || 'Attachment' }}</span>
                          </div>
                        </a>
                        <template v-else>
                          <img 
                            v-if="!isImageFailed(file.attachment)" 
                            :src="file.attachment" 
                            :alt="file.drive_label || file.pdf_label || 'Attachment'" 
                            class="attachment-preview-img standalone-img"
                            @error="handleImageError(file.attachment)"
                          />
                          <div v-else class="media-placeholder-box attachment-placeholder">
                            <div class="placeholder-icon-wrap">
                              <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                                <polyline points="21 15 16 10 5 21"></polyline>
                              </svg>
                            </div>
                            <span class="placeholder-title">{{ file.drive_label || file.pdf_label || 'Attachment' }}</span>
                          </div>
                        </template>
                        <div v-if="file.attachment && !isImageFailed(file.attachment) && file.image_click_url && file.image_text" class="image-text-link-wrapper">
                          <a :href="file.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                            <span>{{ file.image_text }}</span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                          </a>
                        </div>
                      </div>
                    </div>
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
const priceListMap = ref({})
const failedImages = ref(new Set())
const isProtected = ref(false)
const isAuthorized = ref(true)
const enteredPassword = ref('')
const passwordError = ref('')
const showPassword = ref(false)
const authenticating = ref(false)

const handleImageError = (imgSrc) => {
  if (imgSrc) {
    failedImages.value.add(imgSrc)
    failedImages.value = new Set(failedImages.value)
  }
}

const isImageFailed = (imgSrc) => {
  return !imgSrc || failedImages.value.has(imgSrc)
}

const groupedSections = computed(() => {
  const groups = {}
  if (selectedPage.value && selectedPage.value.sections) {
    selectedPage.value.sections.forEach(sec => {
      if (sec.is_display === 1) {
        const groupName = sec.section_group || 'Default Group'
        if (!groups[groupName]) {
          groups[groupName] = []
        }
        groups[groupName].push(sec)
      }
    })
  }
  return groups
})

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
    if (tab.is_display === 0) return; // Filter out unchecked tabs
    
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

const fetchPriceList = async (webCode, pwd = '') => {
  if (!webCode) return;
  try {
    let url = `/api/method/employee_management.api.get_web_price_list?web_code=${encodeURIComponent(webCode)}`;
    if (pwd) {
      url += `&password=${encodeURIComponent(pwd)}`;
    }
    const pRes = await fetch(url);
    if (pRes.ok) {
      const pData = await pRes.json();
      priceListMap.value = pData.message || {};
    }
  } catch (e) {
    console.error("Failed to fetch price list", e);
  }
}

const processLoadedPage = (msg, cacheKey) => {
  if (msg.section && !msg.sections) { msg.sections = msg.section; }
  if (msg.content) msg.content = decodeHtml(msg.content);
  if (msg.sections) {
    msg.sections.forEach(s => {
      if (s.content) s.content = decodeHtml(s.content);
    });
  }
  if (msg.tabs) {
    msg.tabs.forEach(t => {
      if (t.content) t.content = decodeHtml(t.content);
    });
  }
  sessionStorage.setItem(cacheKey, JSON.stringify(msg));
}

const fetchPageData = async (name) => {
  if (!name) return;
  const cacheKey = `hns_page_${name}`;
  const savedPassword = sessionStorage.getItem(`hns_pwd_${name}`) || '';
  const cachedContent = sessionStorage.getItem(cacheKey);

  const searchStr = window.location.hash.includes('?') ? window.location.hash.split('?')[1] : window.location.search;
  const urlParams = new URLSearchParams(searchStr);
  const webCode = urlParams.get('web_code');

  if (cachedContent && !sessionStorage.getItem(`hns_req_pwd_${name}`)) {
    selectedPage.value = JSON.parse(cachedContent);
  }

  if (!selectedPage.value) {
    loading.value = true;
  }

  error.value = null;
  passwordError.value = '';

  try {
    let url = `/api/method/employee_management.api.get_custom_web_pages?name=${encodeURIComponent(name)}`;
    if (savedPassword) {
      url += `&password=${encodeURIComponent(savedPassword)}`;
    }
    if (webCode) {
      url += `&web_code=${encodeURIComponent(webCode)}`;
    }

    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to load page details');
    const data = await res.json();
    const pageMsg = data.message || null;

    if (pageMsg && pageMsg.is_protected && !pageMsg.is_authorized) {
      isProtected.value = true;
      isAuthorized.value = false;
      selectedPage.value = pageMsg;
      sessionStorage.setItem(`hns_req_pwd_${name}`, '1');
      sessionStorage.removeItem(cacheKey);
      if (savedPassword) {
        sessionStorage.removeItem(`hns_pwd_${name}`);
      }
      return;
    }

    isProtected.value = !!(pageMsg && pageMsg.is_protected);
    isAuthorized.value = true;
    selectedPage.value = pageMsg;
    sessionStorage.removeItem(`hns_req_pwd_${name}`);

    if (pageMsg && Object.keys(pageMsg).length > 0 && ((pageMsg.tabs && pageMsg.tabs.length > 0) || pageMsg.content || pageMsg.sections)) {
      processLoadedPage(pageMsg, cacheKey);
      if (webCode) {
        fetchPriceList(webCode, savedPassword);
      }
    } else if (pageMsg && Object.keys(pageMsg).length > 0) {
      processLoadedPage(pageMsg, cacheKey);
      if (webCode) {
        fetchPriceList(webCode, savedPassword);
      }
    } else {
      error.value = `No content found in the '${name}' Custom Web Page.`;
      sessionStorage.removeItem(cacheKey);
    }
  } catch (e) {
    console.error(e);
    error.value = `Failed to fetch '${name}' data from the server.`;
    showError(error.value);
  } finally {
    loading.value = false;
  }
}

const submitPassword = async () => {
  const pwd = enteredPassword.value.trim();
  if (!pwd) {
    passwordError.value = 'Please enter password.';
    return;
  }
  authenticating.value = true;
  passwordError.value = '';

  try {
    const searchStr = window.location.hash.includes('?') ? window.location.hash.split('?')[1] : window.location.search;
    const urlParams = new URLSearchParams(searchStr);
    const webCode = urlParams.get('web_code');

    let url = `/api/method/employee_management.api.get_custom_web_pages?name=${encodeURIComponent(props.pageName)}&password=${encodeURIComponent(pwd)}`;
    if (webCode) {
      url += `&web_code=${encodeURIComponent(webCode)}`;
    }

    const res = await fetch(url);
    const data = await res.json();
    const pageMsg = data.message || null;

    if (pageMsg && pageMsg.is_authorized) {
      sessionStorage.setItem(`hns_pwd_${props.pageName}`, pwd);
      sessionStorage.removeItem(`hns_req_pwd_${props.pageName}`);
      isProtected.value = true;
      isAuthorized.value = true;
      passwordError.value = '';
      enteredPassword.value = '';
      selectedPage.value = pageMsg;

      const cacheKey = `hns_page_${props.pageName}`;
      processLoadedPage(pageMsg, cacheKey);

      if (webCode) {
        fetchPriceList(webCode, pwd);
      }
    } else {
      passwordError.value = (pageMsg && pageMsg.error) || 'Incorrect password. Please try again.';
    }
  } catch (e) {
    passwordError.value = 'Verification failed. Please try again.';
  } finally {
    authenticating.value = false;
  }
}

watch(() => props.pageName, (newName) => {
  failedImages.value = new Set();
  enteredPassword.value = '';
  passwordError.value = '';
  isProtected.value = false;
  isAuthorized.value = true;
  fetchPageData(newName);
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

.custom-section-subtitle {
  display: block;
  background-color: var(--section-subtitle-color, #118ab2);
  color: #ffffff !important;
  text-align: center;
  padding: 0.8rem 1rem;
  font-size: 1.15rem;
  font-weight: 600;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  box-sizing: border-box;
  margin-top: 10px;
  margin-bottom: 15px;
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
  display: flex;
  flex-direction: column;
}
.horizontal-viewport .custom-section-subtitle,
.section-viewport .custom-section-subtitle {
  margin-top: 0;
  margin-bottom: 25px;
}

.viewport-wrapper {
  display: flex;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: visible;
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
  display: flex;
  flex-direction: column;
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

.price-badge {
  background: #ffffff;
  padding: 6px 16px;
  border-radius: 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  gap: 10px;
  border: 2px solid #f8fafc;
  font-family: inherit;
  margin-left: auto;
  white-space: nowrap;
  flex-shrink: 0;
}
.custom-section-subtitle {
  display: flex !important;
  justify-content: center;
  align-items: center;
  gap: 10px;
  text-align: center;
}
.custom-section-subtitle:has(.price-badge) {
  justify-content: space-between;
}
.subtitle-text {
  flex: 1;
  text-align: center;
}
.custom-section {
  position: relative;
}
.price-original {
  text-decoration: line-through;
  text-decoration-color: #ef4444;
  text-decoration-thickness: 2px;
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 600;
}
.price-special, .price-selling {
  color: #16a34a;
  font-weight: 800;
  font-size: 1.15rem;
}
.price-discount {
  color: #dc2626;
  font-weight: 700;
  font-size: 0.85rem;
  background: #fee2e2;
  padding: 2px 8px;
  border-radius: 12px;
  letter-spacing: 0.5px;
  white-space: nowrap;
  flex-shrink: 0;
}

.price-info-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #64748b;
  margin-left: 4px;
}
.price-info-wrapper:hover .price-info-icon {
  color: #3b82f6;
}
.price-info-tooltip {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 10px;
  background-color: #ffffff;
  color: #1e293b;
  text-align: left;
  padding: 10px 14px;
  border-radius: 8px;
  z-index: 1000;
  width: max-content;
  max-width: 300px;
  font-size: 0.85rem;
  line-height: 1.4;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
  transition: opacity 0.2s, visibility 0.2s;
  pointer-events: none;
  border: 1px solid #e2e8f0;
}
.price-info-wrapper:hover .price-info-tooltip {
  visibility: visible;
  opacity: 1;
}
.price-info-tooltip::after {
  content: "";
  position: absolute;
  bottom: 100%;
  right: 6px;
  border-width: 6px;
  border-style: solid;
  border-color: transparent transparent #ffffff transparent;
}
.price-info-tooltip::before {
  content: "";
  position: absolute;
  bottom: 100%;
  right: 5px;
  border-width: 7px;
  border-style: solid;
  border-color: transparent transparent #e2e8f0 transparent;
  z-index: -1;
}


.tab-price-bottom {
  display: flex;
  justify-content: flex-end;
  align-self: flex-end;
  margin-top: auto;
  margin-right: -1.6rem;
  margin-bottom: -1.6rem;
  padding-top: 1.5rem;
}
.tab-price-bottom .price-badge {
  margin-left: auto;
  white-space: nowrap;
}
.tab-price-bottom .price-info-tooltip {
  top: auto;
  bottom: calc(100% + 10px);
  margin-top: 0;
  margin-bottom: 0;
  right: 0;
  left: auto;
  max-width: 280px;
  width: max-content;
  white-space: normal;
  word-break: break-word;
  overflow-wrap: break-word;
  box-sizing: border-box;
}
.tab-price-bottom .price-info-tooltip::after {
  top: 100%;
  bottom: auto;
  right: 12px;
  border-color: #ffffff transparent transparent transparent;
}
.tab-price-bottom .price-info-tooltip::before {
  top: 100%;
  bottom: auto;
  right: 11px;
  border-color: #e2e8f0 transparent transparent transparent;
}

@media (max-width: 768px) {
  .horizontal-viewport,
  .section-viewport {
    padding: 1.5rem 1.25rem 1.25rem 1.25rem !important;
  }
  .custom-section-subtitle {
    flex-direction: column !important;
    align-items: center !important;
    gap: 12px !important;
  }
  .subtitle-text {
    text-align: center;
    width: 100%;
  }
  .custom-section-subtitle .price-badge {
    margin-left: 0 !important;
    justify-content: center;
    width: 100%;
    box-sizing: border-box;
  }
  .tab-price-bottom {
    align-self: flex-end !important;
    justify-content: flex-end !important;
    margin-top: 1.25rem !important;
    margin-right: 0 !important;
    margin-bottom: 0 !important;
    padding-top: 0 !important;
  }
  .tab-price-bottom .price-badge {
    margin-left: auto !important;
    padding: 5px 12px !important;
    gap: 7px !important;
    width: auto !important;
    white-space: nowrap !important;
  }
  .tab-price-bottom .price-special,
  .tab-price-bottom .price-selling {
    font-size: 1.05rem !important;
  }
  .tab-price-bottom .price-original {
    font-size: 0.85rem !important;
  }
  .tab-price-bottom .price-discount {
    font-size: 0.75rem !important;
    padding: 2px 6px !important;
    white-space: nowrap !important;
  }
  .tab-price-bottom .price-info-tooltip {
    right: 0 !important;
    left: auto !important;
    max-width: min(250px, calc(100vw - 48px)) !important;
    width: max-content !important;
    white-space: normal !important;
    word-break: break-word !important;
    overflow-wrap: break-word !important;
    box-sizing: border-box !important;
  }
  .tab-price-bottom .price-info-tooltip::after {
    right: 12px !important;
  }
  .tab-price-bottom .price-info-tooltip::before {
    right: 11px !important;
  }
}




.custom-media-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.custom-media-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.media-preview-container {
  width: 100%;
  background-color: #f8fafc;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.media-link-overlay {
  display: flex;
  width: 100%;
  height: auto;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.custom-media-img {
  width: 100%;
  height: auto;
  display: block;
}

.media-placeholder-box {
  width: 100%;
  height: 100%;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
  background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
  text-align: center;
}

.tab-media-wrapper .media-placeholder-box {
  min-height: 260px;
  aspect-ratio: 16 / 9;
}

.attachment-placeholder {
  min-height: 160px;
  border-radius: 8px;
}

.placeholder-icon-wrap {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06);
  color: #64748b;
  flex-shrink: 0;
}

.placeholder-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #334155;
  max-width: 90%;
  line-height: 1.4;
  word-break: break-word;
}

.custom-media-card .image-text-link-wrapper {
  margin-top: 0;
  padding: 12px 16px 14px;
  background: #ffffff;
  border-top: 1px solid #f1f5f9;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
}



.attachment-image-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.attachment-image-card .image-text-link-wrapper {
  margin-top: 0;
  padding: 10px 12px;
  border-top: 1px solid #f1f5f9;
  background: #ffffff;
}

.attachment-image-card .attachment-image-link {
  border: none;
  box-shadow: none;
  border-radius: 0;
}

.attachment-image-card .standalone-img {
  border: none;
  box-shadow: none;
  border-radius: 0;
  margin-bottom: 0;
}

.attachment-image-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.attachment-image-block .attachment-image-link,
.attachment-image-block .standalone-img {
  width: 100%;
}

.attachment-image-block .standalone-img {
  margin-bottom: 0;
}

.image-text-link-wrapper {
  margin-top: 10px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.image-text-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #1e3a8a;
  font-size: 0.95rem;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: all 0.2s ease;
  cursor: pointer;
  line-height: 1.4;
  word-break: break-word;
}

.image-text-link:hover {
  color: #0284c7;
  text-decoration: underline;
}

.image-text-link-icon {
  flex-shrink: 0;
  stroke-width: 2.2;
}

.tab-media-wrapper .image-text-link-wrapper {
  padding: 10px 14px 14px;
  margin-top: 0;
  background: #ffffff;
}

/* Password Gate Styles - Premium Look & Feel */
.page-password-gate {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  padding: 3rem 1.5rem;
  width: 100%;
  box-sizing: border-box;
  background: 
    radial-gradient(circle at 50% 20%, rgba(37, 99, 235, 0.05) 0%, transparent 60%),
    radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.04) 0%, transparent 50%),
    #f8fafc;
}

.password-card {
  position: relative;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 
    0 1px 3px rgba(15, 23, 42, 0.04),
    0 20px 40px -12px rgba(15, 23, 42, 0.12),
    0 0 0 1px rgba(226, 232, 240, 0.85);
  max-width: 440px;
  width: 100%;
  padding: 2.75rem 2.25rem 2.25rem;
  text-align: center;
  box-sizing: border-box;
  overflow: hidden;
  animation: gateCardEntrance 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes gateCardEntrance {
  from {
    opacity: 0;
    transform: translateY(18px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.card-accent-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
}

.lock-icon-badge-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1.15rem;
}

.lock-icon-badge {
  width: 68px;
  height: 68px;
  border-radius: 20px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  color: #1d4ed8;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 0 0 6px rgba(239, 246, 255, 0.8),
    0 8px 20px rgba(37, 99, 235, 0.18);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.lock-icon-badge:hover {
  transform: scale(1.06) rotate(4deg);
}

.restricted-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #eff6ff;
  color: #1e40af;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.85rem;
  border: 1px solid #bfdbfe;
}

.restricted-tag svg {
  color: #2563eb;
}

.password-title {
  font-size: 1.6rem !important;
  font-weight: 700 !important;
  color: #0f172a !important;
  margin: 0 0 0.5rem 0 !important;
  line-height: 1.3 !important;
  letter-spacing: -0.02em;
  word-break: break-word;
}

.password-desc {
  font-size: 0.92rem !important;
  color: #64748b !important;
  margin: 0 0 1.5rem 0 !important;
  line-height: 1.55 !important;
}

.password-error-alert {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 0.88rem;
  font-weight: 500;
  margin-bottom: 1.25rem;
  animation: shakeAlert 0.35s ease;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.08);
}

.error-alert-icon {
  flex-shrink: 0;
  stroke: #dc2626;
}

@keyframes shakeAlert {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  75% { transform: translateX(6px); }
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
  width: 100%;
}

.password-input-group {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
}

.input-left-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: #94a3b8;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.password-input-group:focus-within .input-left-icon {
  color: #2563eb;
}

.password-field {
  width: 100%;
  height: 48px;
  padding: 0 44px 0 42px;
  font-size: 0.98rem;
  font-weight: 500;
  color: #0f172a;
  background: #f8fafc;
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s ease, background-color 0.2s ease, box-shadow 0.2s ease;
}

.password-field::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.password-field:focus {
  background: #ffffff;
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.eye-toggle-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border-radius: 8px;
  transition: color 0.2s ease, background-color 0.2s ease;
}

.eye-toggle-btn:hover {
  color: #1e293b;
  background: #f1f5f9;
}

.password-submit-btn {
  width: 100%;
  height: 48px;
  padding: 0 1.5rem;
  font-size: 0.96rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.28);
  transition: all 0.2s ease;
}

.password-submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(37, 99, 235, 0.36);
}

.password-submit-btn:active:not(:disabled) {
  transform: translateY(1px);
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
}

.password-submit-btn:disabled {
  opacity: 0.75;
  cursor: not-allowed;
  transform: none;
}

.btn-inner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-spinner-wrap {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.password-spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255, 255, 255, 0.35);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spinGate 0.65s linear infinite;
}

@keyframes spinGate {
  to { transform: rotate(360deg); }
}

.card-footer-links {
  margin-top: 1.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: center;
}

.back-home-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.88rem;
  font-weight: 500;
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s ease, transform 0.2s ease;
}

.back-home-link:hover {
  color: #1e40af;
  transform: translateX(-2px);
}

.alert-fade-enter-active,
.alert-fade-leave-active {
  transition: all 0.2s ease;
}

.alert-fade-enter-from,
.alert-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
