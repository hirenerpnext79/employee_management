<template>
  <teleport to="body">
    <transition name="feedback-modal-fade">
      <div v-if="isOpen" class="feedback-modal-overlay" @click.self="handleClose">
        <div class="feedback-modal-card" role="dialog" aria-modal="true" :style="modalDynamicStyles">
          <div class="modal-accent-bar"></div>

          <div class="modal-header">
            <div class="header-left">
              <div class="header-icon-badge">
                <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  <path d="M12 7v2"></path>
                  <path d="M12 13h.01"></path>
                </svg>
              </div>
              <div class="header-text">
                <h3 class="modal-title">Feedback & Comments</h3>
                <p class="modal-subtitle" v-if="tabTitle || tabCode">
                  Topic: <strong>{{ tabTitle || tabCode }}</strong>
                </p>
              </div>
            </div>

            <div class="header-right-actions">
              <div v-if="historyTabBadgeCount > 0" class="modal-tabs-nav header-tabs-nav">
                <button
                  type="button"
                  class="tab-nav-btn"
                  :class="{ 'is-active': activeModalTab === 'form' }"
                  @click="activeModalTab = 'form'"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                  <span>Give Feedback</span>
                </button>

                <button
                  type="button"
                  class="tab-nav-btn"
                  :class="{ 'is-active': activeModalTab === 'history' }"
                  @click="switchToHistory"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                  <span>My History</span>
                  <span class="history-count-pill">{{ historyTabBadgeCount }}</span>
                </button>
              </div>

              <button type="button" class="modal-close-btn" @click="handleClose" aria-label="Close">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          </div>

          <div class="modal-scroll-body">

            <div v-if="activeModalTab === 'form' || historyTabBadgeCount === 0" class="form-tab-container">
              <form @submit.prevent="handleSubmit" class="modal-form">
                <div v-if="errorMessage" class="modal-error-banner">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                  </svg>
                  <span>{{ errorMessage }}</span>
                </div>

                <div class="form-group">
                  <label class="form-label">
                    How would you rate this? <span class="reqd-star">*</span>
                  </label>
                  <div class="rating-stars-container">
                    <div class="stars-row">
                      <button
                        v-for="star in 5"
                        :key="star"
                        type="button"
                        class="star-btn"
                        :class="{ 'is-active': (hoverRating || form.rating) >= star }"
                        @click="form.rating = star"
                        @mouseenter="hoverRating = star"
                        @mouseleave="hoverRating = 0"
                      >
                        ★
                      </button>
                    </div>
                    <span class="rating-label">{{ currentRatingText }}</span>
                  </div>
                </div>

                <div class="form-row-2col" :class="{ 'single-col': isLoggedIn }">
                  <div class="form-group" v-if="!isLoggedIn">
                    <label class="form-label" for="feedback-email">
                      Email Address <span class="reqd-star">*</span>
                    </label>
                    <input
                      id="feedback-email"
                      type="email"
                      v-model="form.email"
                      @blur="handleEmailBlur"
                      class="form-input"
                      placeholder="name@company.com"
                      :required="!isLoggedIn"
                    />
                  </div>

                  <div class="form-group">
                    <label class="form-label" for="feedback-mobile">
                      Mobile Number <span class="optional-tag">(Optional)</span>
                    </label>
                    <input
                      id="feedback-mobile"
                      type="tel"
                      v-model="form.mobile_no"
                      class="form-input"
                      placeholder="e.g. 9876543210"
                    />
                  </div>
                </div>



                <div class="form-group">
                  <label class="form-label" for="feedback-message">
                    Message / Comments <span class="reqd-star">*</span>
                  </label>
                  <textarea
                    id="feedback-message"
                    v-model="form.message"
                    class="form-textarea"
                    rows="3"
                    placeholder="Share your thoughts, questions, or suggestions..."
                    required
                  ></textarea>
                </div>

                <div class="modal-footer">
                  <button type="button" class="btn-secondary" @click="handleClose" :disabled="isSubmitting">
                    Cancel
                  </button>
                  <button type="submit" class="btn-primary" :disabled="isSubmitting">
                    <span v-if="isSubmitting" class="submitting-spinner"></span>
                    <span>{{ isSubmitting ? 'Submitting...' : 'Submit Feedback' }}</span>
                  </button>
                </div>
              </form>
            </div>

            <div v-else-if="activeModalTab === 'history' && historyTabBadgeCount > 0" class="history-tab-container">

              <div v-if="isLoadingHistory && currentSectionHistory.length === 0" class="history-loading-state">
                <div class="loading-spinner"></div>
                <span>Loading your feedback...</span>
              </div>

              <div v-else class="history-content-wrap">
                <div class="history-list">
                  <div
                    v-for="item in currentSectionHistory"
                    :key="item.name"
                    class="history-card"
                  >
                    <div class="history-card-header">
                      <div class="history-header-meta">
                        <span v-if="item.reply" class="history-status-pill replied">
                          <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                          </svg>
                          Replied
                        </span>
                        <span v-else class="history-status-pill pending">
                          <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                          </svg>
                          Awaiting Response
                        </span>
                      </div>

                      <div class="history-header-info">
                        <div class="history-stars" :title="(item.stars || 5) + ' stars'">
                          <span
                            v-for="s in 5"
                            :key="s"
                            class="star-symbol"
                            :class="{ 'filled': s <= (item.stars || 5) }"
                          >★</span>
                        </div>
                        <span class="history-timestamp">{{ item.formatted_date || item.creation }}</span>
                      </div>
                    </div>

                    <div class="history-message-body">
                      <p class="history-message-text">{{ item.message }}</p>
                    </div>

                    <div v-if="item.reply" class="history-reply-card">
                      <div class="reply-card-header">
                        <div class="reply-card-author">
                          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="9 17 4 12 9 7"></polyline>
                            <path d="M20 18v-2a4 4 0 0 0-4-4H4"></path>
                          </svg>
                          <span class="reply-card-badge">Support Reply</span>
                        </div>
                        <span class="reply-card-time" v-if="item.formatted_reply_date">
                          {{ item.formatted_reply_date }}
                        </span>
                      </div>
                      <p class="reply-card-text">{{ item.reply }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { showToast } from '../utils/toastHandler'
import { getFeedbackContact, setFeedbackContact, getGlobalSessionToken, getGlobalUser } from '../utils/cookieHandler'
import { collectLogData } from '../utils/activityTracker'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  initialTab: {
    type: String,
    default: 'form'
  },
  tabCode: {
    type: String,
    default: ''
  },
  tabTitle: {
    type: String,
    default: ''
  },
  webPage: {
    type: String,
    default: ''
  },
  section: {
    type: String,
    default: ''
  },
  tab: {
    type: String,
    default: ''
  },
  attachment: {
    type: String,
    default: ''
  },
  webCode: {
    type: String,
    default: ''
  },
  loginUser: {
    type: Object,
    default: null
  },
  primaryColor: {
    type: String,
    default: '#1e3a8a'
  },
  secondaryColor: {
    type: String,
    default: '#118ab2'
  },
  initialHistory: {
    type: Array,
    default: () => []
  }
})

const modalDynamicStyles = computed(() => {
  const prim = props.primaryColor?.trim() || '#1e3a8a'
  const sec = props.secondaryColor?.trim() || '#118ab2'
  return {
    '--modal-primary': prim,
    '--modal-secondary': sec,
  }
})

const emit = defineEmits(['close', 'submitted', 'history-updated'])

const activeModalTab = ref('form')
const hoverRating = ref(0)
const isSubmitting = ref(false)
const isLoadingHistory = ref(false)
const errorMessage = ref('')
const feedbackHistory = ref(Array.isArray(props.initialHistory) ? [...props.initialHistory] : [])

watch(() => props.initialHistory, (newHistory) => {
  if (Array.isArray(newHistory) && newHistory.length > 0 && (!feedbackHistory.value || feedbackHistory.value.length === 0)) {
    feedbackHistory.value = [...newHistory]
  }
})
const manualLookupEmail = ref('')
// historyScope removed

const normalizeStr = (val) => {
  if (!val) return ''
  return String(val)
    .trim()
    .toLowerCase()
    .replace(/[_\-\s]+/g, ' ')
}

const isMatchingCurrentSection = (item) => {
  if (!item) return false
  const pCode = normalizeStr(props.tabCode)
  const pTitle = normalizeStr(props.tabTitle)

  if (!pCode && !pTitle) return true

  const iCode = normalizeStr(item.tab_code)
  const iTitle = normalizeStr(item.tab_title)

  if (pCode && (pCode === iCode || pCode === iTitle)) return true
  if (pTitle && (pTitle === iCode || pTitle === iTitle)) return true

  return false
}

const currentSectionDisplayName = computed(() => props.tabTitle || props.tabCode || '')
const hasCurrentSectionProp = computed(() => Boolean(props.tabCode || props.tabTitle))

const currentSectionHistory = computed(() => {
  if (!hasCurrentSectionProp.value) {
    return feedbackHistory.value
  }
  return feedbackHistory.value.filter(isMatchingCurrentSection)
})

const otherSectionsHistory = computed(() => {
  if (!hasCurrentSectionProp.value) {
    return []
  }
  return feedbackHistory.value.filter(item => !isMatchingCurrentSection(item))
})

const hasOtherSections = computed(() => otherSectionsHistory.value.length > 0)

const historyTabBadgeCount = computed(() => {
  if (hasCurrentSectionProp.value) {
    return currentSectionHistory.value.length
  }
  return feedbackHistory.value.length
})

const sectionWiseHistory = computed(() => {
  const groups = {}

  for (const item of feedbackHistory.value) {
    const rawName = item.tab_title || item.tab_code || (item.web_page ? `${item.web_page} (General)` : 'General Feedback')
    const key = normalizeStr(rawName) || 'general'

    if (!groups[key]) {
      groups[key] = {
        title: rawName,
        isCurrent: isMatchingCurrentSection(item),
        items: []
      }
    }
    groups[key].items.push(item)
  }

  const groupList = Object.values(groups)
  groupList.sort((a, b) => {
    if (a.isCurrent && !b.isCurrent) return -1
    if (!a.isCurrent && b.isCurrent) return 1
    return 0
  })

  return groupList
})



const form = reactive({
  email: '',
  mobile_no: '',
  rating: 5,
  message: ''
})

const currentUserEmail = computed(() => {
  if (props.loginUser?.email && props.loginUser.email.includes('@')) {
    return props.loginUser.email.trim()
  }
  if (props.loginUser?.user_name && props.loginUser.user_name.includes('@')) {
    return props.loginUser.user_name.trim()
  }
  const userData = getGlobalUserData()
  if (userData?.email && userData.email.includes('@')) {
    return userData.email.trim()
  }
  if (userData?.user_name && userData.user_name.includes('@')) {
    return userData.user_name.trim()
  }
  const globalUser = getGlobalUser()
  if (globalUser && globalUser.includes('@')) {
    return globalUser.trim()
  }
  const contact = getFeedbackContact()
  if (contact?.email && contact.email.includes('@')) {
    return contact.email.trim()
  }
  return ''
})

const isLoggedIn = computed(() => {
  const hasUserContext = Boolean(props.loginUser || getGlobalSessionToken() || getGlobalUserData() || getGlobalUser())
  return Boolean(hasUserContext && currentUserEmail.value)
})

const effectiveEmail = computed(() => {
  if (isLoggedIn.value) {
    return currentUserEmail.value
  }
  if (form.email && form.email.trim()) {
    return form.email.trim()
  }
  if (manualLookupEmail.value && manualLookupEmail.value.trim()) {
    return manualLookupEmail.value.trim()
  }
  const { email } = getFeedbackContact()
  return (email || '').trim()
})

const ratingLabels = {
  1: '1 Star - Poor',
  2: '2 Stars - Fair',
  3: '3 Stars - Good',
  4: '4 Stars - Very Good',
  5: '5 Stars - Excellent'
}

const currentRatingText = computed(() => {
  const r = hoverRating.value || form.rating
  return ratingLabels[r] || ''
})

const loadSavedContact = () => {
  if (isLoggedIn.value) {
    form.email = currentUserEmail.value
  } else {
    const { email } = getFeedbackContact()
    if (email) {
      form.email = email
    }
  }
  const { mobile } = getFeedbackContact()
  if (mobile) {
    form.mobile_no = mobile
  }
}

let isFetchingHistory = false

const fetchFeedbackHistory = async (showLoading = false) => {
  if (isFetchingHistory) return
  const emailToFetch = effectiveEmail.value
  if (!emailToFetch || !emailToFetch.includes('@')) {
    feedbackHistory.value = []
    return
  }

  if (showLoading && (!feedbackHistory.value || feedbackHistory.value.length === 0)) {
    isLoadingHistory.value = true
  }

  isFetchingHistory = true
  try {
    const url = `/api/method/employee_management.api.get_user_feedback_history?email=${encodeURIComponent(emailToFetch)}`
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
    const data = await res.json()
    if (res.ok && data.message) {
      feedbackHistory.value = Array.isArray(data.message) ? data.message : []
      emit('history-updated', feedbackHistory.value)
    }
  } catch (err) {
    if (!feedbackHistory.value || feedbackHistory.value.length === 0) {
      feedbackHistory.value = []
    }
  } finally {
    isFetchingHistory = false
    isLoadingHistory.value = false
  }
}

const switchToHistory = () => {
  activeModalTab.value = 'history'
  if (effectiveEmail.value && (!feedbackHistory.value || feedbackHistory.value.length === 0)) {
    fetchFeedbackHistory(true)
  }
}

const handleEmailBlur = () => {
  if (form.email && form.email.includes('@')) {
    setFeedbackContact(form.email.trim(), form.mobile_no ? form.mobile_no.trim() : '')
    fetchFeedbackHistory(false)
  }
}

const handleManualLookup = () => {
  if (manualLookupEmail.value && manualLookupEmail.value.includes('@')) {
    fetchFeedbackHistory(true)
  }
}

onMounted(() => {
  loadSavedContact()
})

watch(historyTabBadgeCount, (count) => {
  if (count === 0 && activeModalTab.value === 'history') {
    activeModalTab.value = 'form'
  }
})

watch(() => props.isOpen, (val) => {
  if (val) {
    errorMessage.value = ''
    form.rating = 5
    form.message = ''
    if (props.initialTab === 'history' && historyTabBadgeCount.value > 0) {
      activeModalTab.value = 'history'
    } else {
      activeModalTab.value = 'form'
    }
    // historyScope removed
    loadSavedContact()
    if (effectiveEmail.value && (!feedbackHistory.value || feedbackHistory.value.length === 0)) {
      fetchFeedbackHistory(false)
    }
  }
})

watch(() => [props.tabCode, props.tabTitle], () => {
  // historyScope removed
})

const handleClose = () => {
  if (isSubmitting.value) return
  emit('close')
}

const handleSubmit = async () => {
  errorMessage.value = ''

  if (isLoggedIn.value) {
    form.email = currentUserEmail.value
  }

  if (!form.email || !form.email.includes('@')) {
    errorMessage.value = 'Please enter a valid email address.'
    return
  }

  if (!form.rating) {
    errorMessage.value = 'Please select a rating.'
    return
  }

  if (!form.message.trim()) {
    errorMessage.value = 'Please enter your message.'
    return
  }

  isSubmitting.value = true

  try {
    const cleanMobile = form.mobile_no ? form.mobile_no.trim() : null
    let logData = null
    try {
      logData = await collectLogData()
    } catch (e) {
      // Ignored
    }

    const sessionToken = getGlobalSessionToken();
    const storedUser = props.loginUser?.name || props.loginUser?.user_name || getGlobalUser() || '';

    const payload = {
      email: form.email.trim(),
      rating: form.rating,
      message: form.message.trim(),
      tab_code: props.tabCode || '',
      tab_title: props.tabTitle || '',
      web_page: props.webPage || '',
      section: props.section || '',
      tab: props.tab || '',
      attachment: props.attachment || '',
      mobile_no: cleanMobile,
      session_token: sessionToken,
      user: storedUser,
      web_code: props.webCode || (typeof window !== 'undefined' ? (sessionStorage.getItem('hns_web_code') || localStorage.getItem('hns_web_code') || '') : ''),
      log: logData
    }

    const res = await fetch('/api/method/employee_management.api.submit_web_page_feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    const data = await res.json()

    if (res.ok && data.message && data.message.status === 'success') {
      setFeedbackContact(form.email.trim(), form.mobile_no ? form.mobile_no.trim() : '')
      showToast('Thank you! Feedback submitted.', 'success')
      emit('submitted', payload)

      form.message = ''
      // historyScope removed

      await fetchFeedbackHistory(true)
      activeModalTab.value = 'history'
    } else {
      errorMessage.value = data?.message?.message || data?._server_messages || 'Failed to submit feedback. Please try again.'
    }
  } catch (err) {
    errorMessage.value = 'An unexpected network error occurred. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.feedback-modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(15, 23, 42, 0.68);
  backdrop-filter: blur(8px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.feedback-modal-card {
  position: relative;
  background: #ffffff;
  width: 100%;
  max-width: 680px;
  max-height: 90vh;
  max-height: 90dvh;
  border-radius: 18px;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: modal-pop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-accent-bar {
  height: 5px;
  background: linear-gradient(90deg, var(--modal-primary, #3b82f6), var(--modal-secondary, #6366f1));
  flex-shrink: 0;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1.15rem 1.5rem 0.75rem 1.5rem;
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.header-icon-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #eff6ff;
  background: color-mix(in srgb, var(--modal-primary, #2563eb) 12%, #ffffff);
  color: var(--modal-primary, #2563eb);
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.modal-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  line-height: 1.3;
}

.modal-subtitle {
  font-size: 0.825rem;
  color: #64748b;
  margin: 0.2rem 0 0 0;
}

.modal-close-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 6px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.header-right-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.modal-tabs-nav {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0;
  border-bottom: none;
  flex-shrink: 0;
}

.tab-nav-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  height: 36px;
  padding: 0 0.85rem;
  box-sizing: border-box;
  border-radius: 9px;
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1;
  color: #64748b;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tab-nav-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.tab-nav-btn.is-active {
  background: var(--modal-primary, #2563eb);
  color: #ffffff;
  border-color: var(--modal-primary, #2563eb);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.tab-nav-btn:hover:not(.is-active) {
  background: #f1f5f9;
  color: var(--modal-primary, #1e293b);
  border-color: var(--modal-primary, #e2e8f0);
}

.history-count-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-sizing: border-box;
  min-width: 20px;
  height: 20px;
  padding: 0 5px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 20px;
  background: #0f172a;
  color: #ffffff !important;
  flex-shrink: 0;
  transition: all 0.2s ease;
}

.tab-nav-btn:not(.is-active) .history-count-pill {
  background: #0f172a;
  color: #ffffff !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
}

.tab-nav-btn.is-active .history-count-pill {
  background: #ffffff;
  color: #0f172a !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

.modal-scroll-body {
  flex: 1 1 auto;
  min-height: 0 !important;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 1.25rem 1.5rem 1.75rem 1.5rem;
}

.history-tab-container {
  min-height: 380px;
}

.modal-success-banner {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #065f46;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 1rem;
  animation: modal-pop 0.2s ease;
}

.dismiss-banner-btn {
  margin-left: auto;
  background: transparent;
  border: none;
  color: #059669;
  font-weight: bold;
  cursor: pointer;
  padding: 0 4px;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.modal-error-banner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  font-size: 0.825rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-label {
  font-size: 0.825rem;
  font-weight: 600;
  color: #334155;
}

.reqd-star {
  color: #ef4444;
}

.optional-tag {
  font-size: 0.75rem;
  font-weight: 400;
  color: #94a3b8;
}

.rating-stars-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.5rem 0.85rem;
}

.stars-row {
  display: flex;
  gap: 0.2rem;
}

.star-btn {
  background: transparent;
  border: none;
  font-size: 1.6rem;
  line-height: 1;
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.15s ease;
  padding: 0;
  user-select: none;
}

.star-btn.is-active {
  color: #f59e0b;
  transform: scale(1.1);
  text-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
}

.rating-label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
}

.form-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-row-2col.single-col {
  grid-template-columns: 1fr;
}

.form-input,
.form-textarea {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.6rem 0.85rem;
  font-size: 0.875rem;
  color: #1e293b;
  background: #ffffff;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--modal-primary, #3b82f6);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--modal-primary, #3b82f6) 20%, transparent);
}

.history-quick-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-size: 0.8rem;
  color: #166534;
}

.link-btn {
  background: transparent;
  border: none;
  color: #2563eb;
  font-weight: 600;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 0;
}

.link-btn:hover {
  text-decoration: underline;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.btn-secondary {
  padding: 0.6rem 1.15rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover:not(:disabled) {
  background: #e2e8f0;
  color: #1e293b;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.6rem 1.35rem;
  background: var(--modal-primary, #2563eb);
  border: 1px solid transparent;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.btn-primary:hover:not(:disabled) {
  background: var(--modal-secondary, #1d4ed8);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.22);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submitting-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* History Tab Styles (Clean & Simple Design) */
.history-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.25rem 0.25rem 0.75rem 0.25rem;
  margin-bottom: 0.85rem;
  border-bottom: 1px solid #f1f5f9;
}

.history-account-badge {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  color: #64748b;
}

.history-account-label {
  font-size: 0.78rem;
  color: #94a3b8;
}

.history-account-email {
  color: #0f172a;
  font-weight: 600;
  font-size: 0.82rem;
}

.history-refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 0.32rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
}

.history-refresh-btn:hover {
  background: #f8fafc;
  color: #0f172a;
  border-color: #cbd5e1;
}

.spinning {
  animation: spin 0.75s linear infinite;
}

.email-prompt-box {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 10px;
  padding: 0.85rem 1rem;
  margin-bottom: 1rem;
}

.email-prompt-text {
  font-size: 0.82rem;
  color: #0369a1;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.email-prompt-input-row {
  display: flex;
  gap: 0.5rem;
}

.history-loading-state,
.history-empty-state {
  min-height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2.5rem 1.5rem;
  gap: 0.65rem;
}

.loading-spinner {
  width: 26px;
  height: 26px;
  border: 2.5px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.empty-icon-wrap {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-title {
  font-size: 0.98rem;
  font-weight: 700;
  color: #334155;
  margin: 0;
}

.empty-desc {
  font-size: 0.82rem;
  color: #64748b;
  max-width: 360px;
  margin: 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.history-scope-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.9rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f1f5f9;
}

.scope-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 0.35rem 0.75rem;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.scope-pill-btn:hover {
  background: #f1f5f9;
  color: #334155;
}

.scope-pill-btn.is-active {
  background: #eff6ff;
  color: #2563eb;
  border-color: #bfdbfe;
}

.scope-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: #e2e8f0;
  color: #475569;
  font-size: 0.7rem;
  font-weight: 700;
}

.scope-pill-btn.is-active .scope-count {
  background: #2563eb;
  color: #ffffff;
}

.history-sections-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-section-group {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.section-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.45rem 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 3px solid #2563eb;
}

.section-group-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  min-width: 0;
}

.section-folder-svg {
  color: #2563eb;
  flex-shrink: 0;
}

.section-group-title {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.current-section-badge {
  font-size: 0.65rem;
  font-weight: 600;
  padding: 0.1rem 0.45rem;
  border-radius: 10px;
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
  flex-shrink: 0;
}

.section-group-count {
  font-size: 0.72rem;
  font-weight: 700;
  color: #64748b;
  background: #ffffff;
  padding: 0.12rem 0.45rem;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.empty-actions-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 0.75rem;
  flex-wrap: wrap;
}

.history-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.85rem 1rem;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.history-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.history-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.55rem;
}

.history-header-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.history-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.68rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  letter-spacing: 0.2px;
}

.history-status-pill.replied {
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}

.history-status-pill.pending {
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
}

.history-topic-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.28rem;
  background: #f1f5f9;
  color: #475569;
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.15rem 0.45rem;
  border-radius: 5px;
  border: 1px solid #e2e8f0;
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-header-info {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.history-stars {
  display: inline-flex;
  gap: 1px;
}

.star-symbol {
  font-size: 0.85rem;
  color: #e2e8f0;
  line-height: 1;
}

.star-symbol.filled {
  color: #f59e0b;
}

.history-timestamp {
  font-size: 0.74rem;
  color: #94a3b8;
}

.history-message-body {
  margin-top: 0.1rem;
}

.history-message-text {
  font-size: 0.88rem;
  line-height: 1.5;
  color: #1e293b;
  margin: 0;
  word-break: break-word;
}

.history-reply-card {
  margin-top: 0.65rem;
  background: #f8fafc;
  border-left: 3px solid #2563eb;
  border-radius: 0 8px 8px 0;
  padding: 0.6rem 0.8rem;
}

.reply-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.reply-card-author {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  color: #2563eb;
}

.reply-card-badge {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.reply-card-time {
  font-size: 0.7rem;
  color: #94a3b8;
}

.reply-card-text {
  font-size: 0.84rem;
  line-height: 1.45;
  color: #334155;
  margin: 0;
  word-break: break-word;
}

@keyframes modal-pop {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.feedback-modal-fade-enter-active,
.feedback-modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.feedback-modal-fade-enter-from,
.feedback-modal-fade-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .feedback-modal-overlay {
    padding: 0.5rem;
    align-items: center;
  }

  .feedback-modal-card {
    max-height: 94vh;
    max-height: 94dvh;
    border-radius: 14px;
    min-height: 0;
  }

  .modal-header {
    padding: 0.75rem 1rem;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .header-left {
    flex: 1;
    min-width: 0;
  }

  .header-right-actions {
    width: 100%;
    justify-content: flex-start;
    order: 3;
    padding-top: 0.35rem;
    border-top: 1px solid #f1f5f9;
  }

  .header-icon-badge {
    width: 36px;
    height: 36px;
  }

  .modal-title {
    font-size: 1.05rem;
  }

  .modal-tabs-nav {
    padding: 0;
  }

  .tab-nav-btn {
    padding: 0.35rem 0.7rem;
    font-size: 0.8rem;
  }

  .modal-scroll-body {
    min-height: 0 !important;
    padding: 0.75rem 0.85rem 1.75rem 0.85rem;
  }

  .modal-form {
    gap: 0.65rem;
  }

  .form-row-2col {
    grid-template-columns: 1fr;
  }

  .modal-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 0.6rem;
    padding: 0.75rem 0 0.5rem 0;
    margin-top: 0.5rem;
    border-top: 1px solid #e2e8f0;
    flex-shrink: 0;
  }

  .history-tab-container {
    min-height: 0 !important;
  }
}
</style>
