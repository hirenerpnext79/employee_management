<template>
  <div class="custom-page-wrapper">
    <transition name="page-fade" mode="out-in">
      <div v-if="loading" class="loading-state" key="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      
            <div v-else-if="selectedPage" class="active-page-view" :key="selectedPage.name" :style="pageDynamicStyles">
      <!-- Deactivation Administrative Restriction Gate -->
      <div v-if="isDeactivated || selectedPage?.is_deactivated" class="page-deactivated-gate">
        <div class="deactivated-card">
          <!-- Top administrative accent bar -->
          <div class="card-accent-bar deact-accent-bar"></div>

          <!-- Administrative Shield Badge -->
          <div class="deact-icon-badge-wrapper">
            <div class="deact-icon-badge">
              <svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>
              </svg>
            </div>
          </div>

          <!-- Administrative Restricted Tag -->
          <div class="deact-restricted-tag">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h2v-2h-2v2zm0-4h2V7h-2v6z"/>
            </svg>
            <span>Administrative Restriction</span>
          </div>

          <!-- Page Title -->
          <h2 class="deact-title">{{ selectedPage?.title || selectedPage?.name || 'Access Restricted' }}</h2>

          <!-- Administrative Notice Box -->
          <div class="deact-notice-box">
            <svg class="deact-notice-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <p class="deact-message-text">
              {{ selectedPage?.deactivation_message || 'This page is currently inactive. Please contact your administrator.' }}
            </p>
          </div>

          <!-- Back to Home Link -->
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

      <!-- Password Login Gate -->
      <div v-else-if="isProtected && !isAuthorized" class="page-password-gate">
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

          <!-- Login Form -->
          <form @submit.prevent="submitPassword" class="password-form">
            <!-- Username / Email Input -->
            <div class="password-input-group" style="margin-bottom: 0.85rem;">
              <span class="input-left-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </span>
              <input
                type="text"
                v-model="enteredUsername"
                placeholder="Enter email or username..."
                class="password-field"
                autofocus
                required
              />
            </div>

            <!-- Password Input -->
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
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8z"></path>
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
                <span>Login</span>
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
        <!-- Logged-in User Session Bar -->
        <div v-if="selectedPage?.login_user" class="logged-in-user-bar">
          <div class="user-info-pill">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <span>Logged in as: <strong>{{ selectedPage.login_user.user_name || selectedPage.login_user.email }}</strong></span>
          </div>
          <button type="button" @click="handleLogout" class="user-logout-btn" title="Logout">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            <span>Logout</span>
          </button>
        </div>
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
      <div v-if="Object.keys(groupedSections).length > 0" class="custom-sections-wrapper" :style="{ order: selectedPage.section_sort_order || 0 }">
        <template v-for="(groupSections, groupName) in groupedSections" :key="groupName">
          <!-- Main Title Box -->
          <h2 class="custom-section-title" v-if="groupName !== 'Default Group'" :style="{ backgroundColor: selectedPage?.group_title_color || '#1e3a8a' }">
            {{ formatHeaderTitle(groupName, isFirstHeader('section', groupName)) }}
          </h2>
          
          <template v-for="(sec, idx) in groupSections" :key="'sec-'+idx">
            <div v-if="isDisplayed(sec)" class="custom-section">
            <!-- Sub Title Box -->
            <h3 class="custom-section-subtitle" v-if="sec.page_title" :style="{ backgroundColor: selectedPage?.sub_group_title_color || '#118ab2' }">
              {{ formatHeaderTitle(sec.page_title, isFirstHeader('section_sub', sec.page_title || sec.name)) }}
            </h3>

          <!-- Content Layout -->
          <div 
            class="custom-section-body" 
            :class="{ 
              'has-media': hasSectionMedia(sec), 
              'has-both-media': hasBothSectionMedia(sec), 
              'full-width': !hasSectionMedia(sec), 
              'media-only': hasSectionMedia(sec) && !hasAnySectionContent(sec), 
              'media-right': isMediaRight(sec) && !hasBothSectionMedia(sec) 
            }"
          >
            <!-- Media Container 1 (Left by default, or Right if media-right on single media) -->
            <div v-if="hasSectionMedia(sec)" class="custom-section-media">
              
              <!-- PDF -->
              <template v-if="getContainer1Type(sec) === 'pdf'">
                <div class="custom-pdf-container">
                  <a 
                    :href="getSectionPdfUrl(sec)" 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    class="custom-pdf-big-box"
                    title="Click to open PDF"
                  >
                    <div class="pdf-big-icon-wrap">
                      <svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="pdf-file-svg">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                      </svg>
                      <span class="pdf-badge-tag">PDF</span>
                    </div>

                    <h4 class="pdf-big-title">{{ sec.page_title || getPdfFileName(getSectionPdfUrl(sec)) }}</h4>

                    <div class="pdf-big-btn">
                      <span>Click to view PDF</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" y1="14" x2="21" y2="3"></line>
                      </svg>
                    </div>
                  </a>
                </div>
              </template>

              <!-- Video -->
              <template v-else-if="getContainer1Type(sec) === 'video'">
                <video 
                  v-if="isDirectVideoFile(getSectionVideoSrc(sec))"
                  controls 
                  playsinline 
                  class="custom-media-video-player"
                  :src="getSectionVideoSrc(sec)"
                >
                  Your browser does not support the video tag.
                </video>
                <iframe 
                  v-else
                  :src="getEmbedUrl(getSectionVideoSrc(sec))" 
                  title="Video player" 
                  frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                  allowfullscreen
                ></iframe>
              </template>

              <!-- Image -->
              <template v-else-if="getContainer1Type(sec) === 'image'">
                <div class="custom-media-card">
                  <div class="media-preview-container">
                    <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
                      <img 
                        v-if="!isImageFailed(getSectionImageSrc(sec))" 
                        :src="getSectionImageSrc(sec)" 
                        :alt="sec.page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(getSectionImageSrc(sec))"
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
                        v-if="!isImageFailed(getSectionImageSrc(sec))" 
                        :src="getSectionImageSrc(sec)" 
                        :alt="sec.page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(getSectionImageSrc(sec))"
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
                  <div v-if="!isImageFailed(getSectionImageSrc(sec)) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
                    <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                      <span>{{ sec.image_text }}</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                    </a>
                  </div>
                </div>
              </template>

            </div>
            
            <!-- Section Content Column -->
            <div 
              v-if="hasAnySectionContent(sec)" 
              class="custom-section-content"
            >
              <!-- Main Section Content (Light Gray Box) -->
              <div 
                v-if="hasSectionContent(sec.content)"
                class="content-box-current"
              >
                <HnsExpandableContent 
                  :content="sec.content"
                  :wordLimit="pageWordLimit"
                  :mobileFactor="pageMobileFactor"
                  :readMoreText="pageReadMoreText"
                />
              </div>

              <!-- Customer/Employee Custom Description for Section (1-2 Points Darker Gray Box) -->
              <div 
                v-if="hasSectionContent(getCustomerItem(sec.section_code || sec.name || sec.page_title)?.description)"
                class="content-box-customer"
              >
                <div class="customer-tab-description">
                  <HnsExpandableContent 
                    :content="getCustomerItem(sec.section_code || sec.name || sec.page_title).description" 
                    :wordLimit="pageWordLimit" 
                    :mobileFactor="pageMobileFactor" 
                    :readMoreText="pageReadMoreText" 
                    customClass="customer-desc-html"
                  />
                </div>
              </div>
            </div>

            <!-- Media Container 2 (Right by default when BOTH exist) -->
            <div v-if="hasBothSectionMedia(sec)" class="custom-section-media video-media">
              
              <!-- PDF -->
              <template v-if="getContainer2Type(sec) === 'pdf'">
                <div class="custom-pdf-container">
                  <a 
                    :href="getSectionPdfUrl(sec)" 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    class="custom-pdf-big-box"
                    title="Click to open PDF"
                  >
                    <div class="pdf-big-icon-wrap">
                      <svg xmlns="http://www.w3.org/2000/svg" width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="pdf-file-svg">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                      </svg>
                      <span class="pdf-badge-tag">PDF</span>
                    </div>

                    <h4 class="pdf-big-title">{{ sec.page_title || getPdfFileName(getSectionPdfUrl(sec)) }}</h4>

                    <div class="pdf-big-btn">
                      <span>Click to view PDF</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                        <polyline points="15 3 21 3 21 9"></polyline>
                        <line x1="10" y1="14" x2="21" y2="3"></line>
                      </svg>
                    </div>
                  </a>
                </div>
              </template>

              <!-- Video -->
              <template v-else-if="getContainer2Type(sec) === 'video'">
                <video 
                  v-if="isDirectVideoFile(getSectionVideoSrc(sec))"
                  controls 
                  playsinline 
                  class="custom-media-video-player"
                  :src="getSectionVideoSrc(sec)"
                >
                  Your browser does not support the video tag.
                </video>
                <iframe 
                  v-else
                  :src="getEmbedUrl(getSectionVideoSrc(sec))" 
                  title="Video player" 
                  frameborder="0" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                  allowfullscreen
                ></iframe>
              </template>

              <!-- Image -->
              <template v-else-if="getContainer2Type(sec) === 'image'">
                <div class="custom-media-card">
                  <div class="media-preview-container">
                    <a v-if="sec.image_click_url" :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
                      <img 
                        v-if="!isImageFailed(getSectionImageSrc(sec))" 
                        :src="getSectionImageSrc(sec)" 
                        :alt="sec.page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(getSectionImageSrc(sec))"
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
                        v-if="!isImageFailed(getSectionImageSrc(sec))" 
                        :src="getSectionImageSrc(sec)" 
                        :alt="sec.page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(getSectionImageSrc(sec))"
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
                  <div v-if="!isImageFailed(getSectionImageSrc(sec)) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
                    <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                      <span>{{ sec.image_text }}</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                    </a>
                  </div>
                </div>
              </template>

            </div>

          </div>



          <!-- Section Price Tag & Feedback (Bottom Right - Same as Tab) -->
          <div 
            v-if="(getPriceItem(sec.section_code || sec.name || sec.page_title) && (getPriceItem(sec.section_code || sec.name || sec.page_title).selling_rate || getPriceItem(sec.section_code || sec.name || sec.page_title).short_description)) || isFeedbackAllowed"
            class="tab-price-bottom section-price-bottom"
          >
            <div class="price-badge" v-if="getPriceItem(sec.section_code || sec.name || sec.page_title) && (getPriceItem(sec.section_code || sec.name || sec.page_title).selling_rate || getPriceItem(sec.section_code || sec.name || sec.page_title).short_description)">
              <template v-if="getPriceItem(sec.section_code || sec.name || sec.page_title).selling_rate">
                <template v-if="hasSpecialDiscount(getPriceItem(sec.section_code || sec.name || sec.page_title))">
                  <span class="price-original">₹{{ Number(getPriceItem(sec.section_code || sec.name || sec.page_title).selling_rate).toFixed(2) }}</span>
                  <span class="price-special">₹{{ getFinalPrice(getPriceItem(sec.section_code || sec.name || sec.page_title)).toFixed(2) }}</span>
                  <span class="price-discount">({{ getDiscountPercentage(getPriceItem(sec.section_code || sec.name || sec.page_title)) }}% OFF)</span>
                </template>
                <template v-else>
                  <span class="price-selling">₹{{ Number(getPriceItem(sec.section_code || sec.name || sec.page_title).selling_rate).toFixed(2) }}</span>
                </template>
              </template>
              <div class="price-info-wrapper standalone-info" v-if="getPriceItem(sec.section_code || sec.name || sec.page_title).short_description && !getPriceItem(sec.section_code || sec.name || sec.page_title).selling_rate">
                <span class="price-info-label">Note</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                <div class="price-info-tooltip" v-html="getPriceItem(sec.section_code || sec.name || sec.page_title).short_description"></div>
              </div>
              <div class="price-info-wrapper" v-else-if="getPriceItem(sec.section_code || sec.name || sec.page_title).short_description">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                <div class="price-info-tooltip" v-html="getPriceItem(sec.section_code || sec.name || sec.page_title).short_description"></div>
              </div>
            </div>

            <!-- Feedback Pill Button -->
            <div v-if="isFeedbackAllowed" class="price-badge feedback-badge-standalone">
              <button 
                type="button" 
                class="price-feedback-btn standalone" 
                title="Give Feedback"
                @click="openFeedbackModal(sec)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  <path d="M12 7v2"></path>
                  <path d="M12 13h.01"></path>
                </svg>
                <span>Feedback</span>
              </button>
            </div>
          </div>
          </div> <!-- closing custom-section -->
          </template>
        </template>
      </div>

      <!-- Grouped Tabs Display -->
      <div v-if="groupedTabs.length > 0" class="tabs-wrapper" :style="{ order: selectedPage.tab_sort_order || 0 }">
      <div v-for="(group, gIdx) in groupedTabs" :key="gIdx" class="tab-group-section">
        <h2 v-if="group.name && group.name !== 'Default Group'" class="custom-section-title" :style="{ backgroundColor: selectedPage?.group_title_color || '#1e3a8a' }">
          {{ formatHeaderTitle(group.name, isFirstHeader('tab', group.name)) }}
        </h2>

        <!-- Horizontal Tabs Group -->
        <div v-if="group.horizontal.length > 0" class="horizontal-group">
          <!-- Desktop Tabs View -->
          <div class="desktop-tabs">
            <nav class="sections-navbar">
              <button 
                v-for="(sec, idx) in group.horizontal" 
                :key="idx"
                :class="['section-nav-link', { active: (activeHorizontalIndices[group.name] ?? 0) === idx }]"
                @click="activeHorizontalIndices[group.name] = idx"
              >
                {{ sec.page_title }}
              </button>
            </nav>
            <div class="horizontal-viewport" v-if="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0]">
              <div class="tab-layout" :class="{ 'has-media': group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image || getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].video_url) }">
                <!-- Tab Media -->
                <div v-if="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image || getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].video_url)" class="tab-media-wrapper">
                  <template v-if="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image">
                    <a v-if="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image_click_url" :href="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
                      <img 
                        v-if="!isImageFailed(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image)" 
                        :src="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image" 
                        :alt="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image)"
                      />
                      <div v-else class="media-placeholder-box">
                        <div class="placeholder-icon-wrap">
                          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                          </svg>
                        </div>
                        <span class="placeholder-title">{{ group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title || 'Image' }}</span>
                      </div>
                    </a>
                    <template v-else>
                      <img 
                        v-if="!isImageFailed(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image)" 
                        :src="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image" 
                        :alt="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title || 'Image'" 
                        class="custom-media-img"
                        @error="handleImageError(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image)"
                      />
                      <div v-else class="media-placeholder-box">
                        <div class="placeholder-icon-wrap">
                          <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <circle cx="8.5" cy="8.5" r="1.5"></circle>
                            <polyline points="21 15 16 10 5 21"></polyline>
                          </svg>
                        </div>
                        <span class="placeholder-title">{{ group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title || 'Image' }}</span>
                      </div>
                    </template>
                    <div v-if="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image && !isImageFailed(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image) && group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image_click_url && group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image_text" class="image-text-link-wrapper">
                      <a :href="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                        <span>{{ group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].image_text }}</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                      </a>
                    </div>
                  </template>
                  <iframe v-else-if="getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].video_url)" 
                    :src="getEmbedUrl(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].video_url)" 
                    title="YouTube video player" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    allowfullscreen>
                  </iframe>
                </div>
                <!-- Tab Content Container -->
                <div 
                  v-if="hasAnyTabContent(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0])"
                  class="tab-content-container"
                >
                  <!-- Tab Main Content (Light Gray Box) -->
                  <div 
                    v-if="hasSectionContent(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].content)"
                    class="content-box-current"
                  >
                    <HnsExpandableContent 
                      :content="group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].content"
                      :wordLimit="pageWordLimit"
                      :mobileFactor="pageMobileFactor"
                      :readMoreText="pageReadMoreText"
                      customClass="section-html-content"
                    />
                  </div>

                  <!-- Customer Details & Description (1-2 Points Darker Gray Box) -->
                  <div 
                    v-if="hasSectionContent(getCustomerItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title)?.description)"
                    class="content-box-customer"
                  >
                    <div class="customer-tab-description">
                      <HnsExpandableContent 
                        :content="getCustomerItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).description"
                        :wordLimit="pageWordLimit"
                        :mobileFactor="pageMobileFactor"
                        :readMoreText="pageReadMoreText"
                        customClass="customer-desc-html"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <!-- Price Tag & Feedback (Bottom Right) -->
              <div 
                v-if="(getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title) && (getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).selling_rate || getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).short_description)) || isFeedbackAllowed"
                class="tab-price-bottom"
              >
                <div class="price-badge" v-if="getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title) && (getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).selling_rate || getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).short_description)">
                  <template v-if="getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).selling_rate">
                    <template v-if="hasSpecialDiscount(getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title))">
                      <span class="price-original">₹{{ Number(getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).selling_rate).toFixed(2) }}</span>
                      <span class="price-special">₹{{ getFinalPrice(getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title)).toFixed(2) }}</span>
                      <span class="price-discount">({{ getDiscountPercentage(getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title)) }}% OFF)</span>
                    </template>
                    <template v-else>
                      <span class="price-selling">₹{{ Number(getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).selling_rate).toFixed(2) }}</span>
                    </template>
                  </template>
                  <div class="price-info-wrapper standalone-info" v-if="getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).short_description && !getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).selling_rate">
                    <span class="price-info-label">Note</span>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    <div class="price-info-tooltip" v-html="getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).short_description"></div>
                  </div>
                  <div class="price-info-wrapper" v-else-if="getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).short_description">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                    <div class="price-info-tooltip" v-html="getPriceItem(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].tab_code || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].name || group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0].page_title).short_description"></div>
                  </div>
                </div>

                <!-- Feedback Pill Button -->
                <div v-if="isFeedbackAllowed" class="price-badge feedback-badge-standalone">
                  <button 
                    type="button" 
                    class="price-feedback-btn standalone" 
                    title="Give Feedback"
                    @click="openFeedbackModal(group.horizontal[activeHorizontalIndices[group.name] >= 0 ? activeHorizontalIndices[group.name] : 0])"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                      <path d="M12 7v2"></path>
                      <path d="M12 13h.01"></path>
                    </svg>
                    <span>Feedback</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Mobile Accordion View -->
          <div class="mobile-accordion">
            <div class="mobile-accordion-group">
              <div 
                v-for="(sec, idx) in group.horizontal" 
                :key="'m-h-' + idx"
                class="mobile-accordion-item"
                :class="{ 'is-active': isHorizontalTabActive(group.name, idx) }"
              >
                <button 
                  type="button" 
                  class="mobile-accordion-header"
                  :class="{ 'is-active': isHorizontalTabActive(group.name, idx) }"
                  @click="toggleHorizontalTab(group.name, idx)"
                >
                  <div class="mobile-accordion-title-wrap">
                    <span>{{ sec.page_title }}</span>
                  </div>
                  <svg 
                    class="mobile-accordion-chevron" 
                    :class="{ 'is-open': isHorizontalTabActive(group.name, idx) }"
                    xmlns="http://www.w3.org/2000/svg" 
                    width="18" 
                    height="18" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2.5" 
                    stroke-linecap="round" 
                    stroke-linejoin="round"
                  >
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </button>

                <!-- Accordion Content Below Clicked Tab -->
                <div v-show="isHorizontalTabActive(group.name, idx)" class="mobile-accordion-body">
                  <!-- Tab Media -->
                  <div v-if="sec.image || getEmbedUrl(sec.video_url)" class="tab-media-wrapper">
                    <template v-if="sec.image">
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
                      <div v-if="sec.image && !isImageFailed(sec.image) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
                        <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                          <span>{{ sec.image_text }}</span>
                          <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        </a>
                      </div>
                    </template>
                    <iframe v-else-if="getEmbedUrl(sec.video_url)" 
                      :src="getEmbedUrl(sec.video_url)" 
                      title="YouTube video player" 
                      frameborder="0" 
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                      allowfullscreen>
                    </iframe>
                  </div>

                  <!-- Tab Content Container -->
                  <div 
                    v-if="hasAnyTabContent(sec)"
                    class="tab-content-container"
                  >
                    <div 
                      v-if="hasSectionContent(sec.content)"
                      class="content-box-current"
                    >
                      <HnsExpandableContent 
                        :content="sec.content"
                        :wordLimit="pageWordLimit"
                        :mobileFactor="pageMobileFactor"
                        :readMoreText="pageReadMoreText"
                        customClass="section-html-content"
                      />
                    </div>

                    <!-- Customer Details & Description -->
                    <div 
                      v-if="hasSectionContent(getCustomerItem(sec.tab_code || sec.name || sec.page_title)?.description)"
                      class="content-box-customer"
                    >
                      <div class="customer-tab-description">
                        <HnsExpandableContent 
                          :content="getCustomerItem(sec.tab_code || sec.name || sec.page_title).description" 
                          :wordLimit="pageWordLimit" 
                          :mobileFactor="pageMobileFactor" 
                          :readMoreText="pageReadMoreText" 
                          customClass="customer-desc-html"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- Price Tag & Feedback -->
                  <div 
                    v-if="(getPriceItem(sec.tab_code || sec.name || sec.page_title) && (getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate || getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description)) || isFeedbackAllowed"
                    class="tab-price-bottom"
                  >
                    <div class="price-badge" v-if="getPriceItem(sec.tab_code || sec.name || sec.page_title) && (getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate || getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description)">
                      <template v-if="getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate">
                        <template v-if="hasSpecialDiscount(getPriceItem(sec.tab_code || sec.name || sec.page_title))">
                          <span class="price-original">₹{{ Number(getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate).toFixed(2) }}</span>
                          <span class="price-special">₹{{ getFinalPrice(getPriceItem(sec.tab_code || sec.name || sec.page_title)).toFixed(2) }}</span>
                          <span class="price-discount">({{ getDiscountPercentage(getPriceItem(sec.tab_code || sec.name || sec.page_title)) }}% OFF)</span>
                        </template>
                        <template v-else>
                          <span class="price-selling">₹{{ Number(getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate).toFixed(2) }}</span>
                        </template>
                      </template>
                      <div class="price-info-wrapper standalone-info" v-if="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description && !getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate">
                        <span class="price-info-label">Note</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                        <div class="price-info-tooltip" v-html="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description"></div>
                      </div>
                      <div class="price-info-wrapper" v-else-if="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                        <div class="price-info-tooltip" v-html="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description"></div>
                      </div>
                    </div>

                    <div v-if="isFeedbackAllowed" class="price-badge feedback-badge-standalone">
                      <button 
                        type="button" 
                        class="price-feedback-btn standalone" 
                        title="Give Feedback"
                        @click="openFeedbackModal(sec)"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                          <path d="M12 7v2"></path>
                          <path d="M12 13h.01"></path>
                        </svg>
                        <span>Feedback</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Vertical Tabs Group -->
        <div v-if="group.vertical.length > 0" class="vertical-group">
          <!-- Desktop Vertical Tabs View -->
          <div class="desktop-tabs">
            <div class="viewport-wrapper">
              <aside class="vertical-sidebar">
                <div class="sidebar-links">
                  <button 
                    v-for="(sec, idx) in group.vertical" 
                    :key="idx"
                    :class="['sidebar-nav-link', { active: (activeVerticalIndices[group.name] ?? 0) === idx }]"
                    @click="activeVerticalIndices[group.name] = idx"
                  >
                    <svg class="tab-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                    {{ sec.page_title }}
                  </button>
                </div>
              </aside>

              <!-- Dynamic Content -->
              <div class="section-viewport" v-if="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0]">
                <div class="tab-layout" :class="{ 'has-media': group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image || getEmbedUrl(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].video_url) }">
                  <!-- Tab Media -->
                  <div v-if="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image || getEmbedUrl(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].video_url)" class="tab-media-wrapper">
                    <template v-if="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image">
                      <a v-if="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image_click_url" :href="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image_click_url" target="_blank" rel="noopener noreferrer" class="media-link-overlay">
                        <img 
                          v-if="!isImageFailed(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image)" 
                          :src="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image" 
                          :alt="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title || 'Image'" 
                          class="custom-media-img"
                          @error="handleImageError(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image)"
                        />
                        <div v-else class="media-placeholder-box">
                          <div class="placeholder-icon-wrap">
                            <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                              <circle cx="8.5" cy="8.5" r="1.5"></circle>
                              <polyline points="21 15 16 10 5 21"></polyline>
                            </svg>
                          </div>
                          <span class="placeholder-title">{{ group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title || 'Image' }}</span>
                        </div>
                      </a>
                      <template v-else>
                        <img 
                          v-if="!isImageFailed(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image)" 
                          :src="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image" 
                          :alt="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title || 'Image'" 
                          class="custom-media-img"
                          @error="handleImageError(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image)"
                        />
                        <div v-else class="media-placeholder-box">
                          <div class="placeholder-icon-wrap">
                            <svg class="placeholder-svg" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                              <circle cx="8.5" cy="8.5" r="1.5"></circle>
                              <polyline points="21 15 16 10 5 21"></polyline>
                            </svg>
                          </div>
                          <span class="placeholder-title">{{ group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title || 'Image' }}</span>
                        </div>
                      </template>
                      <div v-if="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image && !isImageFailed(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image) && group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image_click_url && group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image_text" class="image-text-link-wrapper">
                        <a :href="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                          <span>{{ group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].image_text }}</span>
                          <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        </a>
                      </div>
                    </template>
                    <iframe v-else-if="getEmbedUrl(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].video_url)" 
                      :src="getEmbedUrl(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].video_url)" 
                      title="YouTube video player" 
                      frameborder="0" 
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                      allowfullscreen>
                    </iframe>
                  </div>
                  <!-- Tab Content Container -->
                  <div 
                    v-if="hasAnyTabContent(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0])"
                    class="tab-content-container"
                  >
                    <!-- Tab Main Content (Light Gray Box) -->
                    <div 
                      v-if="hasSectionContent(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].content)"
                      class="content-box-current"
                    >
                      <HnsExpandableContent 
                        :content="group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].content"
                        :wordLimit="pageWordLimit"
                        :mobileFactor="pageMobileFactor"
                        :readMoreText="pageReadMoreText"
                        customClass="section-html-content"
                      />
                    </div>

                    <!-- Customer Details & Description (1-2 Points Darker Gray Box) -->
                    <div 
                      v-if="hasSectionContent(getCustomerItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title)?.description)"
                      class="content-box-customer"
                    >
                      <div class="customer-tab-description">
                        <HnsExpandableContent 
                          :content="getCustomerItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).description"
                          :wordLimit="pageWordLimit"
                          :mobileFactor="pageMobileFactor"
                          :readMoreText="pageReadMoreText"
                          customClass="customer-desc-html"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Price Tag & Feedback (Bottom Right) -->
                <div 
                  v-if="(getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title) && (getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).selling_rate || getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).short_description)) || isFeedbackAllowed"
                  class="tab-price-bottom"
                >
                  <div class="price-badge" v-if="getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title) && (getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).selling_rate || getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).short_description)">
                    <template v-if="getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).selling_rate">
                      <template v-if="hasSpecialDiscount(getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title))">
                        <span class="price-original">₹{{ Number(getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).selling_rate).toFixed(2) }}</span>
                        <span class="price-special">₹{{ getFinalPrice(getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title)).toFixed(2) }}</span>
                        <span class="price-discount">({{ getDiscountPercentage(getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title)) }}% OFF)</span>
                      </template>
                      <template v-else>
                        <span class="price-selling">₹{{ Number(getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).selling_rate).toFixed(2) }}</span>
                      </template>
                    </template>
                    <div class="price-info-wrapper standalone-info" v-if="getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).short_description && !getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).selling_rate">
                      <span class="price-info-label">Note</span>
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                      <div class="price-info-tooltip" v-html="getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).short_description"></div>
                    </div>
                    <div class="price-info-wrapper" v-else-if="getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).short_description">
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                      <div class="price-info-tooltip" v-html="getPriceItem(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].tab_code || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].name || group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0].page_title).short_description"></div>
                    </div>
                  </div>

                  <!-- Feedback Pill Button -->
                  <div v-if="isFeedbackAllowed" class="price-badge feedback-badge-standalone">
                    <button 
                      type="button" 
                      class="price-feedback-btn standalone" 
                      title="Give Feedback"
                      @click="openFeedbackModal(group.vertical[activeVerticalIndices[group.name] >= 0 ? activeVerticalIndices[group.name] : 0])"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        <path d="M12 7v2"></path>
                        <path d="M12 13h.01"></path>
                      </svg>
                      <span>Feedback</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Mobile Accordion View -->
          <div class="mobile-accordion">
            <div class="mobile-accordion-group">
              <div 
                v-for="(sec, idx) in group.vertical" 
                :key="'m-v-' + idx"
                class="mobile-accordion-item"
                :class="{ 'is-active': isVerticalTabActive(group.name, idx) }"
              >
                <button 
                  type="button" 
                  class="mobile-accordion-header"
                  :class="{ 'is-active': isVerticalTabActive(group.name, idx) }"
                  @click="toggleVerticalTab(group.name, idx)"
                >
                  <div class="mobile-accordion-title-wrap">
                    <svg class="tab-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                    <span>{{ sec.page_title }}</span>
                  </div>
                  <svg 
                    class="mobile-accordion-chevron" 
                    :class="{ 'is-open': isVerticalTabActive(group.name, idx) }"
                    xmlns="http://www.w3.org/2000/svg" 
                    width="18" 
                    height="18" 
                    viewBox="0 0 24 24" 
                    fill="none" 
                    stroke="currentColor" 
                    stroke-width="2.5" 
                    stroke-linecap="round" 
                    stroke-linejoin="round"
                  >
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </button>

                <!-- Accordion Content Below Clicked Tab -->
                <div v-show="isVerticalTabActive(group.name, idx)" class="mobile-accordion-body">
                  <!-- Tab Media -->
                  <div v-if="sec.image || getEmbedUrl(sec.video_url)" class="tab-media-wrapper">
                    <template v-if="sec.image">
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
                      <div v-if="sec.image && !isImageFailed(sec.image) && sec.image_click_url && sec.image_text" class="image-text-link-wrapper">
                        <a :href="sec.image_click_url" target="_blank" rel="noopener noreferrer" class="image-text-link">
                          <span>{{ sec.image_text }}</span>
                          <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="image-text-link-icon"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                        </a>
                      </div>
                    </template>
                    <iframe v-else-if="getEmbedUrl(sec.video_url)" 
                      :src="getEmbedUrl(sec.video_url)" 
                      title="YouTube video player" 
                      frameborder="0" 
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                      allowfullscreen>
                    </iframe>
                  </div>

                  <!-- Tab Content Container -->
                  <div 
                    v-if="hasAnyTabContent(sec)"
                    class="tab-content-container"
                  >
                    <div 
                      v-if="hasSectionContent(sec.content)"
                      class="content-box-current"
                    >
                      <HnsExpandableContent 
                        :content="sec.content"
                        :wordLimit="pageWordLimit"
                        :mobileFactor="pageMobileFactor"
                        :readMoreText="pageReadMoreText"
                        customClass="section-html-content"
                      />
                    </div>

                    <!-- Customer Details & Description -->
                    <div 
                      v-if="hasSectionContent(getCustomerItem(sec.tab_code || sec.name || sec.page_title)?.description)"
                      class="content-box-customer"
                    >
                      <div class="customer-tab-description">
                        <HnsExpandableContent 
                          :content="getCustomerItem(sec.tab_code || sec.name || sec.page_title).description" 
                          :wordLimit="pageWordLimit" 
                          :mobileFactor="pageMobileFactor" 
                          :readMoreText="pageReadMoreText" 
                          customClass="customer-desc-html"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- Price Tag & Feedback -->
                  <div 
                    v-if="(getPriceItem(sec.tab_code || sec.name || sec.page_title) && (getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate || getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description)) || isFeedbackAllowed"
                    class="tab-price-bottom"
                  >
                    <div class="price-badge" v-if="getPriceItem(sec.tab_code || sec.name || sec.page_title) && (getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate || getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description)">
                      <template v-if="getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate">
                        <template v-if="hasSpecialDiscount(getPriceItem(sec.tab_code || sec.name || sec.page_title))">
                          <span class="price-original">₹{{ Number(getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate).toFixed(2) }}</span>
                          <span class="price-special">₹{{ getFinalPrice(getPriceItem(sec.tab_code || sec.name || sec.page_title)).toFixed(2) }}</span>
                          <span class="price-discount">({{ getDiscountPercentage(getPriceItem(sec.tab_code || sec.name || sec.page_title)) }}% OFF)</span>
                        </template>
                        <template v-else>
                          <span class="price-selling">₹{{ Number(getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate).toFixed(2) }}</span>
                        </template>
                      </template>
                      <div class="price-info-wrapper standalone-info" v-if="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description && !getPriceItem(sec.tab_code || sec.name || sec.page_title).selling_rate">
                        <span class="price-info-label">Note</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                        <div class="price-info-tooltip" v-html="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description"></div>
                      </div>
                      <div class="price-info-wrapper" v-else-if="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="price-info-icon"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                        <div class="price-info-tooltip" v-html="getPriceItem(sec.tab_code || sec.name || sec.page_title).short_description"></div>
                      </div>
                    </div>

                    <div v-if="isFeedbackAllowed" class="price-badge feedback-badge-standalone">
                      <button 
                        type="button" 
                        class="price-feedback-btn standalone" 
                        title="Give Feedback"
                        @click="openFeedbackModal(sec)"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                          <path d="M12 7v2"></path>
                          <path d="M12 13h.01"></path>
                        </svg>
                        <span>Feedback</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
      
      <!-- Grouped Attachments (Dynamic) -->
      <div v-if="Object.keys(groupedAttachments).length > 0" class="attachments-wrapper" :style="{ order: selectedPage.attachment_sort_order || 0 }">
      <template v-if="Object.keys(groupedAttachments).length > 0">
        <div class="attachment-section-container" v-for="(groupData, groupTitle) in groupedAttachments" :key="groupTitle">
          <!-- Main Title Banner -->
          <h2 class="custom-section-title" v-if="groupTitle !== 'Attachments' && groupTitle !== 'General'" :style="{ backgroundColor: selectedPage?.group_title_color || '#1e3a8a' }">
            {{ formatHeaderTitle(groupTitle, isFirstHeader('attachment', groupTitle)) }}
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
                    <div v-if="isFeedbackAllowed" class="attachment-card-feedback">
                      <div class="price-badge feedback-badge-standalone">
                        <button 
                          type="button" 
                          class="price-feedback-btn standalone" 
                          title="Give Feedback"
                          @click="openFeedbackModal(file)"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                            <path d="M12 7v2"></path>
                            <path d="M12 13h.01"></path>
                          </svg>
                          <span>Feedback</span>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="attachment-link-container">
                  <a :href="file.attachment" target="_blank" class="attachment-link">
                    <span class="attachment-name">{{ file.drive_label || file.pdf_label || file.attachment.split('/').pop() }}</span>
                  </a>
                  <div v-if="isFeedbackAllowed" class="price-badge feedback-badge-standalone">
                    <button 
                      type="button" 
                      class="price-feedback-btn standalone" 
                      title="Give Feedback"
                      @click="openFeedbackModal(file)"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                        <path d="M12 7v2"></path>
                        <path d="M12 13h.01"></path>
                      </svg>
                      <span>Feedback</span>
                    </button>
                  </div>
                </div>
              </template>
          </div>

          <!-- Sub Groups (Columns) -->
          <div class="attachment-columns" :style="{ '--attachment-cols': Math.min(selectedPage?.attachment_across_page || 2, Object.keys(groupData.subGroups).length, getVisibleCount(groupTitle)) }" v-if="Object.keys(groupData.subGroups).length > 0">
              <div class="attachment-column" v-for="([subTitle, files]) in Object.entries(groupData.subGroups).slice(0, getVisibleCount(groupTitle))" :key="subTitle">
              <div class="column-header" :style="{ backgroundColor: selectedPage?.sub_group_title_color || '#118ab2' }">
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
                    <div v-else class="attachment-link-container">
                      <a :href="file.attachment" target="_blank" class="attachment-link">
                        <span class="attachment-name">{{ file.drive_label || file.pdf_label || file.attachment.split('/').pop() }}</span>
                      </a>

                    </div>
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

          <!-- Attachment Group Feedback Bottom -->
          <div v-if="isFeedbackAllowed" class="attachment-feedback-bottom">
            <div class="price-badge feedback-badge-standalone">
              <button 
                type="button" 
                class="price-feedback-btn standalone" 
                title="Give Feedback"
                @click="openFeedbackModal({ name: groupTitle, page_title: groupTitle, group_title: groupTitle })"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  <path d="M12 7v2"></path>
                  <path d="M12 13h.01"></path>
                </svg>
                <span>Feedback</span>
              </button>
            </div>
          </div>
        </div>
      </template>
      </div>

      <!-- Optional Slot for Page-Specific Static Sections -->
      <slot name="after-sections"></slot>

      </div>
      </div>
    </transition>

    <!-- Feedback Modal Popup -->
    <HnsFeedbackModal
      :isOpen="isFeedbackModalOpen"
      :tabCode="activeFeedbackTab?.tab_code || ''"
      :tabTitle="activeFeedbackTab?.page_title || ''"
      :webPage="selectedPage?.title || selectedPage?.name || props.pageName || ''"
      :loginUser="selectedPage?.login_user"
      @close="closeFeedbackModal"
    />
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted, computed, nextTick } from 'vue'
import { showError } from '../utils/toastHandler'
import HnsExpandableContent from './HnsExpandableContent.vue'
import HnsFeedbackModal from './HnsFeedbackModal.vue'

const isFeedbackModalOpen = ref(false)
const activeFeedbackTab = ref(null)

const openFeedbackModal = (item) => {
  if (!item) return
  activeFeedbackTab.value = {
    tab_code: item.tab_code || item.section_code || item.name || '',
    page_title: item.page_title || item.drive_label || item.pdf_label || item.group_title || (typeof item.attachment === 'string' ? item.attachment.split('/').pop() : '') || 'Feedback'
  }
  isFeedbackModalOpen.value = true
}

const closeFeedbackModal = () => {
  isFeedbackModalOpen.value = false
  activeFeedbackTab.value = null
}

const props = defineProps({
  pageName: {
    type: String,
    required: true
  },
  initialPageData: {
    type: Object,
    default: null
  },
  token: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['logout'])

const loading = ref(false)
const error = ref(null)
const selectedPage = ref(null)
const priceListMap = ref({})

const pageDynamicStyles = computed(() => {
  const groupColor = selectedPage.value?.group_title_color?.trim() || '#1e3a8a'
  const subGroupColor = selectedPage.value?.sub_group_title_color?.trim() || '#118ab2'
  return {
    '--group-title-color': groupColor,
    '--section-title-color': groupColor,
    '--sub-group-title-color': subGroupColor,
    '--section-subtitle-color': subGroupColor,
  }
})

const getResolvedGroupName = (rawName) => {
  if (!rawName) return ''
  if (selectedPage.value?.group_name_map && selectedPage.value.group_name_map[rawName]) {
    return selectedPage.value.group_name_map[rawName]
  }
  return rawName
}
const failedImages = ref(new Set())
const isDeactivated = ref(false)
const isProtected = ref(false)
const isAuthorized = ref(true)
const enteredUsername = ref('')
const enteredPassword = ref('')
const passwordError = ref('')
const showPassword = ref(false)
const authenticating = ref(false)

const pageWordLimit = computed(() => {
  const limit = selectedPage.value?.content_word_limit
  return limit !== undefined && limit !== null ? Number(limit) : 0
})

const pageMobileFactor = computed(() => {
  const factor = selectedPage.value?.content_word_mobile_factor
  return factor !== undefined && factor !== null ? Number(factor) : 1
})

const pageReadMoreText = computed(() => {
  return selectedPage.value?.read_more_text || ''
})


const getEffectiveWebCode = () => {
  const searchStr = window.location.hash.includes('?') ? window.location.hash.split('?')[1] : window.location.search
  const urlParams = new URLSearchParams(searchStr)
  return urlParams.get('web_code') || urlParams.get('employee_code') || urlParams.get('employee') || urlParams.get('token') || props.token || ''
}

const employeeDisplayName = computed(() => {
  return selectedPage.value?.employee_name || priceListMap.value?._employee_name || ''
})

const firstHeaderInfo = computed(() => {
  const blocks = []

  const secKeys = Object.keys(groupedSections.value || {})
  if (secKeys.length > 0) {
    const validGroup = secKeys.find(k => k && k !== 'Default Group')
    const sortOrder = Number(selectedPage.value?.section_sort_order ?? 1)
    if (validGroup) {
      blocks.push({
        type: 'section',
        key: validGroup,
        order: isNaN(sortOrder) ? 1 : sortOrder,
        domIndex: 1
      })
    } else {
      for (const k of secKeys) {
        const secs = groupedSections.value[k] || []
        const firstSec = secs.find(s => s && s.page_title && isDisplayed(s))
        if (firstSec) {
          blocks.push({
            type: 'section_sub',
            key: firstSec.page_title || firstSec.name,
            order: isNaN(sortOrder) ? 1 : sortOrder,
            domIndex: 1
          })
          break
        }
      }
    }
  }

  const tabs = groupedTabs.value || []
  if (tabs.length > 0) {
    const validTabGroup = tabs.find(g => g && g.name && g.name !== 'Default Group')
    const sortOrder = Number(selectedPage.value?.tab_sort_order ?? 2)
    if (validTabGroup) {
      blocks.push({
        type: 'tab',
        key: validTabGroup.name,
        order: isNaN(sortOrder) ? 2 : sortOrder,
        domIndex: 2
      })
    }
  }

  const attKeys = Object.keys(groupedAttachments.value || {})
  if (attKeys.length > 0) {
    const validAttGroup = attKeys.find(k => k && k !== 'Attachments' && k !== 'General')
    const sortOrder = Number(selectedPage.value?.attachment_sort_order ?? 3)
    if (validAttGroup) {
      blocks.push({
        type: 'attachment',
        key: validAttGroup,
        order: isNaN(sortOrder) ? 3 : sortOrder,
        domIndex: 3
      })
    }
  }

  if (blocks.length === 0) return null

  blocks.sort((a, b) => {
    if (a.order !== b.order) return a.order - b.order
    return a.domIndex - b.domIndex
  })

  return blocks[0]
})

const isFirstHeader = (type, key) => {
  if (!firstHeaderInfo.value) return false
  return firstHeaderInfo.value.type === type && firstHeaderInfo.value.key === key
}

const formatHeaderTitle = (title, isFirst) => {
  if (!title) return ''
  const empName = employeeDisplayName.value
  if (isFirst && empName) {
    if (title.toLowerCase().endsWith(empName.toLowerCase())) {
      return title
    }
    return `${title} - ${empName}`
  }
  return title
}

watch(
  [() => selectedPage.value?.title, employeeDisplayName],
  ([title, empName]) => {
    if (title) {
      document.title = empName ? `${title} - ${empName}` : title
    }
  },
  { immediate: true }
)

const isFeedbackAllowed = computed(() => {
  return Boolean(Number(selectedPage.value?.feedback_allow) === 1 || selectedPage.value?.feedback_allow === true)
})

const hasSpecialDiscount = (priceItem) => {
  if (!priceItem || !priceItem.selling_rate) return false
  return Boolean(Number(priceItem.special_discount) > 0)
}

const getFinalPrice = (priceItem) => {
  if (!priceItem || !priceItem.selling_rate) return 0
  const rate = Number(priceItem.selling_rate) || 0
  const discount = Number(priceItem.special_discount) || 0
  return Math.max(0, rate - discount)
}

const getDiscountPercentage = (priceItem) => {
  if (!priceItem || !priceItem.selling_rate || !priceItem.special_discount) return 0
  const rate = Number(priceItem.selling_rate) || 0
  const discount = Number(priceItem.special_discount) || 0
  if (rate <= 0) return 0
  return Math.round((discount / rate) * 100)
}

const isHorizontalTabActive = (groupName, idx) => {
  if (activeHorizontalIndices.value[groupName] === undefined) {
    return idx === 0
  }
  return activeHorizontalIndices.value[groupName] === idx
}

const toggleHorizontalTab = (groupName, idx) => {
  const current = activeHorizontalIndices.value[groupName] ?? 0
  if (current === idx) {
    activeHorizontalIndices.value[groupName] = -1
  } else {
    activeHorizontalIndices.value[groupName] = idx
  }
}

const isVerticalTabActive = (groupName, idx) => {
  if (activeVerticalIndices.value[groupName] === undefined) {
    return idx === 0
  }
  return activeVerticalIndices.value[groupName] === idx
}

const toggleVerticalTab = (groupName, idx) => {
  const current = activeVerticalIndices.value[groupName] ?? 0
  if (current === idx) {
    activeVerticalIndices.value[groupName] = -1
  } else {
    activeVerticalIndices.value[groupName] = idx
  }
}

const getPriceItem = (code) => {
  if (!code || !priceListMap.value) return null
  const map = priceListMap.value
  if (map[code]) return map[code]
  const str = String(code).trim()
  if (map[str]) return map[str]
  const lower = str.toLowerCase()
  if (map[lower]) return map[lower]
  const snake = lower.replace(/[-\s]+/g, '_')
  if (map[snake]) return map[snake]
  const slug = lower.replace(/[\s_]+/g, '-')
  if (map[slug]) return map[slug]
  const space = lower.replace(/[_-]+/g, ' ')
  if (map[space]) return map[space]
  for (const k of Object.keys(map)) {
    const kLower = k.toLowerCase()
    if (kLower === lower || kLower.replace(/[-\s]+/g, '_') === snake) {
      return map[k]
    }
  }
  return null
}

const getCustomerItem = (tabCode) => {
  return getPriceItem(tabCode)
}

const isDisplayed = (item) => {
  if (!item) return false
  if (item.is_display === 0 || item.is_display === '0' || item.is_display === false) return false
  return true
}

const hasSectionContent = (content) => {
  if (!content) return false
  if (typeof content !== 'string') return Boolean(content)
  const trimmed = content.trim()
  if (!trimmed) return false
  if (/<(img|iframe|video|svg|object|embed|audio|table|canvas|hr|picture|button|input)[\s>/]/i.test(trimmed)) {
    return true
  }
  const stripped = trimmed
    .replace(/<[^>]*>/g, '')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&#160;/gi, ' ')
    .replace(/[\s\u200B\uFEFF\u00A0]+/g, ' ')
    .trim()
  return stripped.length > 0
}

const hasAnySectionContent = (sec) => {
  if (!sec) return false
  if (hasSectionContent(sec.content)) return true
  const custItem = getCustomerItem(sec.section_code || sec.name || sec.page_title)
  return Boolean(custItem && hasSectionContent(custItem.description))
}

const hasAnyTabContent = (tab) => {
  if (!tab) return false
  if (hasSectionContent(tab.content)) return true
  const custItem = getCustomerItem(tab.tab_code || tab.name || tab.page_title)
  return Boolean(custItem && hasSectionContent(custItem.description))
}

const isPdfFile = (src) => {
  if (!src) return false
  const clean = String(src).split('?')[0].toLowerCase()
  return clean.endsWith('.pdf')
}

const isDirectVideoFile = (src) => {
  if (!src) return false
  const lower = String(src).split('?')[0].toLowerCase()
  return lower.endsWith('.mp4') || lower.endsWith('.webm') || lower.endsWith('.ogg') || lower.endsWith('.mov') || lower.endsWith('.mkv')
}

const getSectionPdfUrl = (sec) => {
  if (!sec) return ''
  const mt = sec.media_type ? String(sec.media_type).trim().toLowerCase() : ''
  if (mt === 'pdf' && sec.image) return sec.image
  const candidates = [sec.image, sec.attachment_pdf, sec.attachment]
  for (const c of candidates) {
    if (c && isPdfFile(c)) return c
  }
  return ''
}

const isSectionPdf = (sec) => {
  return Boolean(getSectionPdfUrl(sec))
}

const getSectionVideoSrc = (sec) => {
  if (!sec) return ''
  if (sec.video_url) return sec.video_url
  const candidates = [sec.image, sec.attachment]
  for (const c of candidates) {
    if (c && isDirectVideoFile(c)) return c
  }
  return ''
}

const isSectionVideo = (sec) => {
  if (!sec) return false
  if (sec.video_url && getEmbedUrl(sec.video_url)) return true
  return Boolean(getSectionVideoSrc(sec))
}

const getSectionImageSrc = (sec) => {
  if (!sec) return ''
  if (sec.media_type && String(sec.media_type).trim().toLowerCase() === 'pdf') return ''
  const candidates = [sec.image, sec.attachment]
  for (const c of candidates) {
    if (c && !isPdfFile(c) && !isDirectVideoFile(c)) return c
  }
  return ''
}

const isSectionImage = (sec) => {
  return Boolean(getSectionImageSrc(sec))
}

const isMediaRight = (sec) => {
  if (!sec || !sec.imagevideo_position) return false
  return String(sec.imagevideo_position).trim().toLowerCase() === 'right'
}

const getEffectiveMediaType = (sec) => {
  if (!sec) return 'none'
  const mt = sec.media_type ? String(sec.media_type).trim().toLowerCase() : ''
  if (mt === 'video' && isSectionVideo(sec)) return 'video'
  if (mt === 'pdf' && isSectionPdf(sec)) return 'pdf'
  if (mt === 'image' && isSectionImage(sec)) return 'image'
  
  if (isSectionPdf(sec)) return 'pdf'
  if (isSectionVideo(sec)) return 'video'
  if (isSectionImage(sec)) return 'image'
  
  if (mt === 'video') return 'video'
  if (mt === 'pdf') return 'pdf'
  if (mt === 'image') return 'image'
  return 'none'
}

const hasBothSectionMedia = (sec) => {
  if (!sec) return false
  const hasFirst = Boolean(getSectionPdfUrl(sec) || getSectionImageSrc(sec))
  const hasSecond = Boolean(isSectionVideo(sec))
  return hasFirst && hasSecond
}

const hasSectionMedia = (sec) => {
  if (!sec) return false
  return Boolean(getSectionPdfUrl(sec) || getSectionImageSrc(sec) || isSectionVideo(sec))
}

const getOtherMediaType = (sec) => {
  return isSectionPdf(sec) ? 'pdf' : 'image'
}

const getContainer1Type = (sec) => {
  if (!sec) return 'none'
  if (hasBothSectionMedia(sec)) {
    const mt = sec.media_type ? String(sec.media_type).trim().toLowerCase() : ''
    const right = isMediaRight(sec)
    if (mt === 'video') {
      return right ? getOtherMediaType(sec) : 'video'
    } else if (mt === 'pdf' || mt === 'image') {
      return right ? 'video' : mt
    } else {
      return right ? 'video' : getOtherMediaType(sec)
    }
  }
  return getEffectiveMediaType(sec)
}

const getContainer2Type = (sec) => {
  if (!sec || !hasBothSectionMedia(sec)) return 'none'
  const mt = sec.media_type ? String(sec.media_type).trim().toLowerCase() : ''
  const right = isMediaRight(sec)
  if (mt === 'video') {
    return right ? 'video' : getOtherMediaType(sec)
  } else if (mt === 'pdf' || mt === 'image') {
    return right ? mt : 'video'
  } else {
    return right ? getOtherMediaType(sec) : 'video'
  }
}

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
  const rawSections = selectedPage.value?.sections || selectedPage.value?.section
  if (rawSections && Array.isArray(rawSections)) {
    rawSections.forEach(sec => {
      if (isDisplayed(sec)) {
        const rawGroup = sec.section_group || 'Default Group'
        const groupName = getResolvedGroupName(rawGroup) || 'Default Group'
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
        if (!isDisplayed(att)) return;
        const rawGroup = att.group_title || 'Attachments'
        const groupTitle = getResolvedGroupName(rawGroup) || 'Attachments'
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
    const finalGroups = {}
    Object.keys(groups).forEach(key => {
      const g = groups[key]
      if (g.general.length > 0 || Object.keys(g.subGroups).length > 0) {
        finalGroups[key] = g
      }
    })
    return finalGroups
  })

  const decodeHtml = (html) => {
    if (!html) return html;
    const txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
  }

  const getEmbedUrl = (rawUrl) => {
  if (!rawUrl) return null;
  let url = rawUrl.trim();
  
  if (url.includes('<iframe')) {
    const match = url.match(/src=["'](.*?)["']/);
    if (match && match[1]) {
      url = match[1];
    } else {
      return null;
    }
  }

  // Google Drive video / file preview embed
  if (url.includes('drive.google.com') || url.includes('docs.google.com')) {
    const fileMatch = url.match(/\/file\/d\/([a-zA-Z0-9_-]+)/);
    if (fileMatch && fileMatch[1]) {
      return `https://drive.google.com/file/d/${fileMatch[1]}/preview`;
    }
    const idMatch = url.match(/[?&]id=([a-zA-Z0-9_-]+)/);
    if (idMatch && idMatch[1]) {
      return `https://drive.google.com/file/d/${idMatch[1]}/preview`;
    }
  }

  if (url.includes('youtube.com/shorts/')) {
    const match = url.match(/shorts\/([a-zA-Z0-9_-]+)/);
    if (match && match[1]) {
      return `https://www.youtube.com/embed/${match[1]}`;
    }
  }
  
  if (url.includes('watch?v=')) {
    url = url.replace('watch?v=', 'embed/').split('&')[0];
  } else if (url.includes('youtu.be/')) {
    url = url.replace('youtu.be/', 'youtube.com/embed/').split('?')[0];
  } else if (url.includes('vimeo.com/') && !url.includes('player.vimeo.com')) {
    const match = url.match(/vimeo\.com\/(\d+)/);
    if (match && match[1]) {
      return `https://player.vimeo.com/video/${match[1]}`;
    }
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
    if (!isDisplayed(tab)) return; // Filter out unchecked tabs
    
    const rawGroup = tab.group_name || 'Default Group'
    const groupName = getResolvedGroupName(rawGroup) || 'Default Group'
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
  
  return Object.values(groups).filter(g => g.horizontal.length > 0 || g.vertical.length > 0)
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
    if (g.horizontal[hIdx] && isDisplayed(g.horizontal[hIdx])) sections.push(g.horizontal[hIdx])
    
    const vIdx = activeVerticalIndices.value[g.name] || 0
    if (g.vertical[vIdx] && isDisplayed(g.vertical[vIdx])) sections.push(g.vertical[vIdx])
  })
  
  const rawSections = selectedPage.value?.sections || selectedPage.value?.section
  if (rawSections && Array.isArray(rawSections)) {
    rawSections.forEach(sec => {
      if (isDisplayed(sec)) sections.push(sec)
    })
  }
  
  return sections
})

const fetchPriceList = async (webCode, pwd = '') => {
  if (!webCode) return;
  try {
    const payload = {
      web_code: webCode,
    };
    if (pwd) {
      payload.password = pwd;
    }
    const pRes = await fetch('/api/method/employee_management.api.get_web_price_list', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    if (pRes.ok) {
      const pData = await pRes.json();
      priceListMap.value = pData.message || {};
    }
  } catch (e) {
    console.error("Failed to fetch price list", e);
  }
}

const getStoredCredential = (key) => {
  try {
    return localStorage.getItem(key) || sessionStorage.getItem(key) || '';
  } catch (e) {
    return '';
  }
}

const setStoredCredential = (key, val) => {
  try { localStorage.setItem(key, val); } catch (e) {}
  try { sessionStorage.setItem(key, val); } catch (e) {}
}

const removeStoredCredential = (key) => {
  try { localStorage.removeItem(key); } catch (e) {}
  try { sessionStorage.removeItem(key); } catch (e) {}
}

const processLoadedPage = (msg, cacheKey) => {
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
  setStoredCredential(cacheKey, JSON.stringify(msg));
}

const handlePageResponse = (pageMsg, name, webCode) => {
  const cacheKey = `hns_page_${name}`;
  if (pageMsg) {
    if (pageMsg.section && !pageMsg.sections) {
      pageMsg.sections = pageMsg.section;
    }
  }

  if (pageMsg && pageMsg.is_deactivated) {
    isDeactivated.value = true;
    isProtected.value = false;
    isAuthorized.value = false;
    selectedPage.value = pageMsg;
    removeStoredCredential(cacheKey);
    removeStoredCredential(`hns_session_${name}`);
    removeStoredCredential(`hns_req_pwd_${name}`);
    return;
  }
  isDeactivated.value = false;

  if (pageMsg && pageMsg.is_protected && !pageMsg.is_authorized) {
    isProtected.value = true;
    isAuthorized.value = false;
    selectedPage.value = pageMsg;
    setStoredCredential(`hns_req_pwd_${name}`, '1');
    removeStoredCredential(cacheKey);
    if (pageMsg.error || pageMsg.session_expired) {
      removeStoredCredential(`hns_session_${name}`);
    }
    return;
  }

  isProtected.value = !!(pageMsg && pageMsg.is_protected);
  isAuthorized.value = true;
  selectedPage.value = pageMsg;
  removeStoredCredential(`hns_req_pwd_${name}`);

  if (pageMsg && pageMsg.session_token) {
    setStoredCredential(`hns_session_${name}`, pageMsg.session_token);
  }

  if (pageMsg && Object.keys(pageMsg).length > 0 && ((pageMsg.tabs && pageMsg.tabs.length > 0) || pageMsg.content || pageMsg.sections)) {
    processLoadedPage(pageMsg, cacheKey);
    if (webCode) {
      fetchPriceList(webCode);
    }
  } else if (pageMsg && Object.keys(pageMsg).length > 0) {
    processLoadedPage(pageMsg, cacheKey);
    if (webCode) {
      fetchPriceList(webCode);
    }
  } else {
    error.value = `No content found in the '${name}' Custom Web Page.`;
    removeStoredCredential(cacheKey);
  }
}

const fetchPageData = async (name) => {
  if (!name) return;
  const cacheKey = `hns_page_${name}`;
  const sessionToken = getStoredCredential(`hns_session_${name}`);
  const cachedContent = getStoredCredential(cacheKey);

  const webCode = getEffectiveWebCode();

  error.value = null;
  passwordError.value = '';
  isDeactivated.value = false;

  if (props.initialPageData && (props.initialPageData.name === name || props.initialPageData.route === name)) {
    if (props.initialPageData.is_protected && !props.initialPageData.is_authorized && sessionToken) {
      // Session token exists to verify against server
    } else {
      handlePageResponse(props.initialPageData, name, webCode);
      loading.value = false;
      return;
    }
  }

  if (cachedContent && !getStoredCredential(`hns_req_pwd_${name}`)) {
    try {
      selectedPage.value = JSON.parse(cachedContent);
    } catch (e) {}
  }

  if (!selectedPage.value) {
    loading.value = true;
  }

  try {
    const payload = {
      name,
    };
    if (sessionToken) {
      payload.session_token = sessionToken;
    }
    if (webCode) payload.web_code = webCode;

    const res = await fetch('/api/method/employee_management.api.get_custom_web_pages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to load page details');
    const data = await res.json();
    const pageMsg = data.message || null;
    if (pageMsg && pageMsg.session_expired) {
      removeStoredCredential(`hns_session_${name}`);
      removeStoredCredential(cacheKey);
    }
    handlePageResponse(pageMsg, name, webCode);
  } catch (e) {
    console.error(e);
    error.value = `Failed to fetch '${name}' data from the server.`;
    showError(error.value);
  } finally {
    loading.value = false;
  }
}

const submitPassword = async () => {
  const username = enteredUsername.value.trim();
  const pwd = enteredPassword.value.trim();
  if (!username) {
    passwordError.value = 'Please enter email or username.';
    return;
  }
  if (!pwd) {
    passwordError.value = 'Please enter password.';
    return;
  }
  authenticating.value = true;
  passwordError.value = '';

  try {
    const webCode = getEffectiveWebCode();

    const payload = {
      name: props.pageName,
      username,
      password: pwd,
    };
    if (webCode) payload.web_code = webCode;

    const res = await fetch('/api/method/employee_management.api.get_custom_web_pages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    const pageMsg = data.message || null;

    if (pageMsg && pageMsg.is_deactivated) {
      isDeactivated.value = true;
      isProtected.value = false;
      isAuthorized.value = false;
      selectedPage.value = pageMsg;
      removeStoredCredential(`hns_page_${props.pageName}`);
      removeStoredCredential(`hns_session_${props.pageName}`);
      removeStoredCredential(`hns_req_pwd_${props.pageName}`);
      return;
    }

    if (pageMsg && pageMsg.is_authorized) {
      if (pageMsg.session_token) {
        setStoredCredential(`hns_session_${props.pageName}`, pageMsg.session_token);
      }
      removeStoredCredential(`hns_req_pwd_${props.pageName}`);
      removeStoredCredential(`hns_pwd_${props.pageName}`);
      removeStoredCredential(`hns_user_${props.pageName}`);
      isProtected.value = true;
      isAuthorized.value = true;
      passwordError.value = '';
      enteredPassword.value = '';
      enteredUsername.value = '';
      selectedPage.value = pageMsg;

      const cacheKey = `hns_page_${props.pageName}`;
      processLoadedPage(pageMsg, cacheKey);

      if (webCode) {
        fetchPriceList(webCode);
      }
    } else {
      passwordError.value = (pageMsg && pageMsg.error) || 'Authentication failed. Please check your credentials.';
    }
  } catch (e) {
    passwordError.value = 'Verification failed. Please try again.';
  } finally {
    authenticating.value = false;
  }
}

const handleLogout = async () => {
  const sessionToken = getStoredCredential(`hns_session_${props.pageName}`);
  removeStoredCredential(`hns_session_${props.pageName}`);
  removeStoredCredential(`hns_page_${props.pageName}`);
  removeStoredCredential(`hns_req_pwd_${props.pageName}`);
  removeStoredCredential(`hns_pwd_${props.pageName}`);
  removeStoredCredential(`hns_user_${props.pageName}`);

  enteredUsername.value = '';
  enteredPassword.value = '';
  passwordError.value = '';
  isAuthorized.value = false;
  isProtected.value = true;
  selectedPage.value = null;
  emit('logout');

  if (sessionToken) {
    try {
      await fetch('/api/method/employee_management.api.logout_web_page_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_token: sessionToken }),
      });
    } catch (e) {}
  }

  fetchPageData(props.pageName);
}

watch(() => props.pageName, (newName) => {
  failedImages.value = new Set();
  enteredUsername.value = '';
  enteredPassword.value = '';
  passwordError.value = '';
  isProtected.value = false;
  isAuthorized.value = true;
  isDeactivated.value = false;
  fetchPageData(newName);
}, { immediate: true })

watch(() => props.initialPageData, (newData) => {
  if (newData && (newData.name === props.pageName || newData.route === props.pageName)) {
    const webCode = getEffectiveWebCode();
    const sessionToken = getStoredCredential(`hns_session_${props.pageName}`);

    if (newData.is_protected && !newData.is_authorized && sessionToken) {
      fetchPageData(props.pageName);
      return;
    }
    handlePageResponse(newData, props.pageName, webCode);
  }
})

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
    background-color: var(--group-title-color, var(--section-title-color, #1e3a8a));
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
    margin-top: 2.5rem;
    margin-bottom: 1.5rem;
  }

.custom-section-title:first-child,
.attachment-section-container > .custom-section-title:first-of-type {
    margin-top: 0;
  }

.custom-section-subtitle {
  display: block;
  background-color: var(--sub-group-title-color, var(--section-subtitle-color, #118ab2));
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

.custom-section-body.media-only {
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.custom-section-body.media-only .custom-section-media {
  flex: 0 0 100%;
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
}

.custom-section-body.media-only .custom-section-media iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  min-height: 520px;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
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
  flex: 0 0 48%;
  max-width: 48%;
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
  min-height: 360px;
  border: 0;
  display: block;
  border-radius: 16px;
}

.custom-section-body.has-both-media {
  align-items: flex-start;
}

.custom-section-body.has-both-media .custom-section-media iframe,
.custom-section-body.has-both-media .custom-section-media .custom-media-video-player,
.custom-section-body.has-both-media .custom-section-media .custom-media-card,
.custom-section-body.has-both-media .custom-section-media .custom-pdf-container,
.custom-section-body.has-both-media .custom-section-media .custom-pdf-big-box {
  width: 100%;
  height: 280px;
  min-height: 280px;
  max-height: 280px;
  border-radius: 16px;
  box-sizing: border-box;
}

.custom-section-body.has-both-media .custom-section-media .custom-media-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.custom-section-body.has-both-media .custom-section-media .media-preview-container {
  flex: 1;
  width: 100%;
  height: 100%;
  min-height: 0;
  display: flex;
  overflow: hidden;
}

.custom-section-body.has-both-media .custom-section-media .media-preview-container .media-link-overlay {
  width: 100%;
  height: 100%;
  display: flex;
}

.custom-section-body.has-both-media .custom-section-media img.custom-media-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 16px;
  display: block;
}

.custom-section-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .custom-section-body,
  .custom-section-body.media-right,
  .custom-section-body.full-width,
  .custom-section-body.has-both-media {
    flex-direction: column !important;
    gap: 1.5rem !important;
    width: 100% !important;
  }
  .custom-section-media,
  .custom-section-body.has-both-media .custom-section-media {
    max-width: 100% !important;
    flex: 0 0 100% !important;
    width: 100% !important;
    display: flex;
    justify-content: center;
  }
  .custom-section-body.has-both-media .custom-section-content,
  .custom-section-content {
    max-width: 100% !important;
    flex: 0 0 100% !important;
    width: 100% !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    padding: 0 !important;
  }
  .custom-section-body.media-only .custom-section-media iframe {
    min-height: 260px;
  }
  .custom-section-media iframe {
    min-height: 240px;
  }
  .custom-section-body.has-both-media .custom-section-media .custom-media-card,
  .custom-section-body.has-both-media .custom-section-media iframe,
  .custom-section-body.has-both-media .custom-section-media .custom-media-video-player,
  .custom-section-body.has-both-media .custom-section-media .custom-pdf-big-box {
    min-height: 240px;
    height: auto;
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
  padding: 0 1.25rem;
  box-sizing: border-box;
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

.tabs-wrapper {
  width: 100%;
  margin: 0 0 1.5rem 0;
  padding: 0;
}

.tab-group-section {
  margin-bottom: 2rem;
}

.tab-group-section:last-child {
  margin-bottom: 0;
}

.vertical-group {
  margin-bottom: 2rem;
}

.horizontal-group {
  margin-bottom: 2rem;
}

.tab-group-section:last-child .vertical-group,
.tab-group-section:last-child .horizontal-group {
  margin-bottom: 0;
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
  border: 1px solid #e2e8f0;
  border-radius: 0 12px 12px 12px;
  padding: 2.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: all 0.4s ease;
  position: relative;
  display: flex;
  flex-direction: column;
  margin-top: -1px;
}
.custom-section .custom-section-subtitle,
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
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
}

.tab-group-section:last-child .viewport-wrapper {
  margin-bottom: 0;
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

.sidebar-nav-link:last-child {
  border-bottom: none;
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
  margin: 1.5rem 0 2.5rem 0;
  font-family: inherit;
}

.attachment-section-container:first-child,
.attachments-wrapper .attachment-section-container:first-child {
  margin-top: 0;
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
  background-color: var(--sub-group-title-color, var(--section-subtitle-color, #118ab2));
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
  width: 100%;
  box-sizing: border-box;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 2.5rem;
  padding: 2.5rem;
}

.custom-section-body {
  display: flex;
  flex-direction: row;
  gap: 2.5rem;
  align-items: flex-start;
  padding: 0;
}

.section-price-bottom {
  padding: 0 !important;
  margin-top: 1.5rem;
}

.desktop-tabs {
  display: block;
}

.mobile-accordion {
  display: none;
}

.mobile-accordion-group {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 0;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
}

.mobile-accordion-item {
  width: 100%;
  border-bottom: 1px solid #e2e8f0;
}

.mobile-accordion-item:last-child {
  border-bottom: none;
}

.mobile-accordion-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.1rem 1.25rem;
  background: #f8fafc;
  border: none;
  cursor: pointer;
  text-align: left;
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--tabs-font-color, #334155);
  transition: all 0.2s ease;
  border-left: 4px solid transparent;
}

.mobile-accordion-header:hover {
  background: #f1f5f9;
}

.mobile-accordion-header.is-active {
  background: #ffffff;
  color: var(--tabs-color, #1e3a8a);
  border-left-color: var(--tabs-color, #1e3a8a);
}

.mobile-accordion-header.is-active .tab-icon {
  color: var(--tabs-color, #1e3a8a);
}

.mobile-accordion-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.mobile-accordion-chevron {
  width: 18px;
  height: 18px;
  color: #94a3b8;
  transition: transform 0.25s ease, color 0.2s ease;
  flex-shrink: 0;
}

.mobile-accordion-header.is-active .mobile-accordion-chevron {
  transform: rotate(180deg);
  color: var(--tabs-color, #1e3a8a);
}

.mobile-accordion-body {
  padding: 1.5rem 1.25rem 1.25rem 1.25rem;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  animation: accordionFadeIn 0.25s ease-out;
}

@keyframes accordionFadeIn {
  from {
    opacity: 0;
    transform: translateY(-6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .desktop-tabs {
    display: none !important;
  }
  .mobile-accordion {
    display: block !important;
  }
  .custom-section-body {
    flex-direction: column;
    padding: 0;
    gap: 1.5rem;
  }
  .custom-section {
    padding: 1.5rem 1.25rem !important;
    margin-bottom: 1.5rem;
  }
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
  align-items: center;
  align-self: flex-end;
  margin-top: auto;
  margin-right: -1.6rem;
  margin-bottom: -1.6rem;
  padding-top: 1.5rem;
  gap: 12px;
}
.tab-price-bottom .price-badge {
  margin-left: 0 !important;
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
    margin-left: 0 !important;
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

/* Deactivation Administrative Gate Styles */
.page-deactivated-gate {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px);
  padding: 3rem 1.5rem;
  width: 100%;
  box-sizing: border-box;
  background: 
    radial-gradient(circle at 50% 20%, rgba(220, 38, 38, 0.04) 0%, transparent 60%),
    radial-gradient(circle at 80% 80%, rgba(239, 68, 68, 0.03) 0%, transparent 50%),
    #f8fafc;
}

.deactivated-card {
  position: relative;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 
    0 1px 3px rgba(15, 23, 42, 0.04),
    0 20px 40px -12px rgba(15, 23, 42, 0.12),
    0 0 0 1px rgba(226, 232, 240, 0.85);
  max-width: 460px;
  width: 100%;
  padding: 2.75rem 2.25rem 2.25rem;
  text-align: center;
  box-sizing: border-box;
  overflow: hidden;
  animation: gateCardEntrance 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.deact-accent-bar {
  background: linear-gradient(90deg, #991b1b 0%, #dc2626 50%, #f87171 100%);
}

.deact-icon-badge-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1.15rem;
}

.deact-icon-badge {
  width: 68px;
  height: 68px;
  border-radius: 20px;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 0 0 6px rgba(254, 242, 242, 0.85),
    0 8px 20px rgba(220, 38, 38, 0.16);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.deact-icon-badge:hover {
  transform: scale(1.05);
}

.deact-restricted-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #fef2f2;
  color: #991b1b;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.85rem;
  border: 1px solid #fecaca;
}

.deact-restricted-tag svg {
  color: #dc2626;
}

.deact-title {
  font-size: 1.55rem !important;
  font-weight: 700 !important;
  color: #0f172a !important;
  margin: 0 0 1rem 0 !important;
  line-height: 1.3 !important;
  letter-spacing: -0.02em;
  word-break: break-word;
}

.deact-notice-box {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: #fff1f2;
  border: 1px solid #ffe4e6;
  border-radius: 12px;
  padding: 12px 14px;
  text-align: left;
  margin-bottom: 1.25rem;
}

.deact-notice-icon {
  flex-shrink: 0;
  stroke: #e11d48;
  margin-top: 2px;
}

.deact-message-text {
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  color: #9f1239 !important;
  line-height: 1.5 !important;
  margin: 0 !important;
}

.deact-subtext {
  font-size: 0.85rem !important;
  color: #64748b !important;
  line-height: 1.55 !important;
  margin: 0 0 0.5rem 0 !important;
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

/* Tab Content Container & Customer Details Section */
.tab-content-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
  gap: 1.25rem;
}

.tab-customer-fullwidth-section {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-top: 1.75rem;
  padding-top: 1.5rem;
  border-top: 1px dashed #cbd5e1;
}

.section-customer-description,
.tab-customer-description-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.section-customer-description.has-top-divider,
.tab-customer-description-wrapper.has-top-divider {
  margin-top: 1.25rem;
  padding-top: 1.25rem;
  border-top: 1px dashed #cbd5e1;
}

.customer-tab-description {
  width: 100%;
  line-height: 1.65;
  color: #334155;
}

.customer-desc-html {
  width: 100%;
  font-size: 0.95rem;
}


/* Feedback Button in Price Badge */
.price-feedback-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  margin-left: 6px;
}

.price-feedback-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #64748b;
  padding: 3px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.price-feedback-btn:hover {
  color: #f59e0b;
  background-color: rgba(245, 158, 11, 0.12);
  transform: scale(1.1);
}

.price-feedback-btn.standalone {
  gap: 0.4rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1d4ed8;
  padding: 0.35rem 0.65rem;
  background: transparent;
  border: none;
  cursor: pointer;
}

.price-feedback-btn.standalone:hover {
  color: #1d4ed8;
  background-color: transparent;
  transform: none;
}

.feedback-badge-standalone {
  background: #ffffff;
  border: 1px solid #d1d5db;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border-radius: 9999px;
  padding: 3px 8px;
  display: inline-flex;
  align-items: center;
}

.feedback-badge-standalone:hover {
  border-color: #d1d5db;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transform: none;
}

.section-feedback-bottom {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.25rem;
  width: 100%;
}

.attachment-feedback-bottom {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
  width: 100%;
}

.attachment-card-feedback {
  display: flex;
  justify-content: flex-end;
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
}

.attachment-link-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.5rem 0.85rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  transition: all 0.2s ease;
}

.attachment-link-container:hover {
  border-color: #cbd5e1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.feedback-btn-tooltip {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 8px;
  background-color: #1e293b;
  color: #ffffff;
  text-align: center;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  pointer-events: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: opacity 0.2s, visibility 0.2s;
  z-index: 1000;
}

.feedback-btn-tooltip::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 4px;
  border-style: solid;
  border-color: #1e293b transparent transparent transparent;
}

.price-feedback-wrapper:hover .feedback-btn-tooltip {
  visibility: visible;
  opacity: 1;
}


.price-info-wrapper.standalone-info {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  color: #2563eb;
  font-weight: 500;
  font-size: 0.88rem;
}
.price-info-label {
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.section-customer-description {
  margin-top: 1.5rem;
  width: 100%;
}


.section-price-bottom {
  margin-right: 0 !important;
  margin-bottom: 1.5rem !important;
  margin-top: 1.25rem !important;
  padding-top: 0 !important;
  gap: 12px;
}
@media (max-width: 768px) {
  .section-price-bottom {
    margin-right: 0 !important;
    gap: 8px !important;
  }
}


.custom-media-video-player {
  width: 100%;
  aspect-ratio: 16 / 9;
  min-height: 360px;
  border-radius: 12px;
  display: block;
  background-color: #000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.custom-section-body.media-only .custom-media-video-player {
  min-height: 520px;
}

.custom-pdf-container {
  width: 100%;
}

.custom-pdf-big-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  min-height: 340px;
  padding: 3rem 2rem;
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  text-decoration: none;
  color: #1e293b;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  box-sizing: border-box;
  cursor: pointer;
  transition: none;
}

.custom-pdf-big-box:hover {
  transform: none;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  border-color: #cbd5e1;
}

.pdf-big-icon-wrap {
  position: relative;
  width: 84px;
  height: 84px;
  background: #fef2f2;
  border: 1.5px solid #fee2e2;
  border-radius: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.25rem;
}

.pdf-big-icon-wrap .pdf-file-svg {
  width: 44px;
  height: 44px;
  color: #dc2626;
}

.pdf-big-icon-wrap .pdf-badge-tag {
  position: absolute;
  bottom: -6px;
  right: -6px;
  background: #dc2626;
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  padding: 2px 7px;
  border-radius: 6px;
  box-shadow: 0 2px 5px rgba(220, 38, 38, 0.35);
}

.pdf-big-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 1rem 0;
  line-height: 1.4;
  max-width: 90%;
  word-break: break-word;
  text-align: center;
}

.pdf-big-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 20px;
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 8px;
  font-size: 0.92rem;
  font-weight: 600;
}

.custom-section-body.media-only .custom-pdf-container {
  max-width: 620px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .custom-media-video-player {
    min-height: 240px;
  }
  .custom-section-body.media-only .custom-media-video-player {
    min-height: 260px;
  }
  .custom-pdf-big-box {
    min-height: 250px;
    padding: 2rem 1.25rem;
  }
  .pdf-big-icon-wrap {
    width: 68px;
    height: 68px;
    border-radius: 18px;
  }
  .pdf-big-icon-wrap .pdf-file-svg {
    width: 36px;
    height: 36px;
  }
  .pdf-big-title {
    font-size: 1.05rem;
  }
}





.content-box-current {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.25rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  width: 100%;
  box-sizing: border-box;
  color: #1e293b;
  line-height: 1.65;
}

.content-box-current:last-child {
  margin-bottom: 0;
}

.content-box-customer {
  background-color: #edf2f7;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  width: 100%;
  box-sizing: border-box;
  color: #1e293b;
  line-height: 1.65;
}

.custom-section-body.full-width {
  flex-direction: column;
  width: 100%;
  align-items: stretch;
}

.custom-section-body.full-width .custom-section-content {
  width: 100%;
  max-width: 100%;
  flex: 1 1 100%;
  box-sizing: border-box;
}

.custom-section-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .custom-section-content {
    display: flex !important;
    flex-direction: column !important;
    width: 100% !important;
  }
  .content-box-current,
  .content-box-customer {
    width: 100% !important;
    max-width: 100% !important;
    display: block !important;
    box-sizing: border-box !important;
    margin-bottom: 1rem;
  }
  .content-box-customer:last-child,
  .content-box-current:last-child {
    margin-bottom: 0 !important;
  }
}


.logged-in-user-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.65rem 1.25rem;
  margin-bottom: 1.75rem;
  font-size: 0.9rem;
  color: #334155;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.user-info-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-role-badge {
  background: #e2e8f0;
  color: #475569;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.user-logout-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0.35rem 0.85rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #dc2626;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-logout-btn:hover {
  background: #fee2e2;
  border-color: #fca5a5;
  color: #b91c1c;
}
</style>
