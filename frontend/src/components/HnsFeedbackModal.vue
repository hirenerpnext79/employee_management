<template>
  <teleport to="body">
    <transition name="feedback-modal-fade">
      <div v-if="isOpen" class="feedback-modal-overlay" @click.self="handleClose">
        <div class="feedback-modal-card" role="dialog" aria-modal="true">
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
            <button type="button" class="modal-close-btn" @click="handleClose" aria-label="Close">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="modal-tabs-nav">
            <button
              type="button"
              class="tab-nav-btn"
              :class="{ 'is-active': activeModalTab === 'form' }"
              @click="activeModalTab = 'form'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
              </svg>
              <span>My History</span>
              <span v-if="feedbackHistory.length > 0" class="history-count-pill">
                {{ feedbackHistory.length }}
              </span>
            </button>
          </div>

          <div class="modal-scroll-body">
            <div v-if="submissionNotice" class="modal-success-banner">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"></path>
              </svg>
              <span>{{ submissionNotice }}</span>
              <button type="button" class="dismiss-banner-btn" @click="submissionNotice = ''">✕</button>
            </div>

            <div v-if="activeModalTab === 'form'" class="form-tab-container">
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

                <div v-if="!isLoggedIn && feedbackHistory.length > 0" class="history-quick-link">
                  <span>Found {{ feedbackHistory.length }} past feedback(s) with this email.</span>
                  <button type="button" class="link-btn" @click="activeModalTab = 'history'">
                    View comments & replies →
                  </button>
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

            <div v-else-if="activeModalTab === 'history'" class="history-tab-container">
              <div class="history-filter-bar">
                <div class="history-user-info">
                  <div class="history-user-avatar">
                    {{ getUserInitial(effectiveEmail) }}
                  </div>
                  <div class="history-user-text">
                    <span class="history-user-label">Comments by</span>
                    <strong class="history-user-email">{{ effectiveEmail || 'Guest' }}</strong>
                  </div>
                </div>

                <div class="history-actions">
                  <button
                    type="button"
                    class="reload-history-btn"
                    @click="fetchFeedbackHistory(true)"
                    :disabled="isLoadingHistory"
                    title="Refresh history"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="15"
                      height="15"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      :class="{ 'spinning': isLoadingHistory }"
                    >
                      <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"></path>
                    </svg>
                    <span>Refresh</span>
                  </button>
                </div>
              </div>

              <div v-if="!effectiveEmail" class="email-prompt-box">
                <p class="email-prompt-text">Enter your email address to look up your feedback history & replies:</p>
                <div class="email-prompt-input-row">
                  <input
                    type="email"
                    v-model="manualLookupEmail"
                    placeholder="name@company.com"
                    class="form-input"
                    @keyup.enter="handleManualLookup"
                  />
                  <button type="button" class="btn-primary" @click="handleManualLookup">
                    Lookup
                  </button>
                </div>
              </div>

              <div v-if="isLoadingHistory" class="history-loading-state">
                <div class="loading-spinner"></div>
                <span>Loading your feedback threads...</span>
              </div>

              <div v-else-if="feedbackHistory.length === 0" class="history-empty-state">
                <div class="empty-icon-wrap">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
                <h4 class="empty-title">No Feedback History Found</h4>
                <p class="empty-desc">
                  No feedback or discussion comments have been submitted yet under <strong>{{ effectiveEmail || 'this account' }}</strong>.
                </p>
                <button type="button" class="btn-primary" @click="activeModalTab = 'form'" style="margin-top: 1rem;">
                  ✍️ Write Feedback Now
                </button>
              </div>

              <div v-else class="blog-comments-stream">
                <div
                  v-for="(group, dateLabel) in groupedHistory"
                  :key="dateLabel"
                  class="date-stream-group"
                >
                  <div class="stream-date-divider">
                    <span class="date-chip">
                      <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                      </svg>
                      {{ dateLabel }}
                    </span>
                  </div>

                  <div
                    v-for="item in group"
                    :key="item.name"
                    class="blog-comment-thread"
                  >
                    <div class="comment-bubble user-comment">
                      <div class="bubble-left">
                        <div class="avatar-circle user-avatar">
                          {{ getUserInitial(item.email) }}
                        </div>
                      </div>

                      <div class="bubble-main">
                        <div class="bubble-header">
                          <div class="author-meta">
                            <span class="author-name">{{ item.email }}</span>
                            <span class="comment-type-tag sent-tag">Sent</span>
                            <span class="comment-time">{{ item.formatted_date || item.creation }}</span>
                          </div>

                          <div class="bubble-rating-pill">
                            <span class="star-rating-render">
                              <span
                                v-for="s in 5"
                                :key="s"
                                class="star-mini"
                                :class="{ 'filled': s <= (item.stars || 5) }"
                              >★</span>
                            </span>
                          </div>
                        </div>

                        <div class="comment-context-row" v-if="item.tab_title || item.tab_code">
                          <span class="context-tag">
                            <svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                            </svg>
                            {{ item.tab_title || item.tab_code }}
                          </span>
                        </div>

                        <div class="bubble-body">
                          <p class="comment-text">{{ item.message }}</p>
                        </div>

                        <div class="bubble-status-row">
                          <span v-if="item.reply" class="status-badge status-replied">
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                              <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                            Replied
                          </span>
                          <span v-else class="status-badge status-pending">
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                              <circle cx="12" cy="12" r="10"></circle>
                              <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                            Awaiting response
                          </span>
                        </div>
                      </div>
                    </div>

                    <div v-if="item.reply" class="reply-thread-wrap">
                      <div class="thread-connector-branch"></div>
                      <div class="comment-bubble reply-comment">
                        <div class="bubble-left">
                          <div class="avatar-circle team-avatar">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                            </svg>
                          </div>
                        </div>

                        <div class="bubble-main">
                          <div class="bubble-header">
                            <div class="author-meta">
                              <span class="author-name team-name">Support / Admin Team</span>
                              <span class="comment-type-tag reply-tag">Reply</span>
                              <span class="comment-time" v-if="item.formatted_reply_date">
                                {{ item.formatted_reply_date }}
                              </span>
                            </div>
                          </div>

                          <div class="bubble-body reply-body">
                            <p class="comment-text reply-text">{{ item.reply }}</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div v-else class="reply-pending-notice">
                      <div class="thread-connector-branch subtle"></div>
                      <div class="pending-bubble">
                        <span>Our team has received this feedback and will reply here shortly.</span>
                      </div>
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
import { getFeedbackContact, setFeedbackContact } from '../utils/cookieHandler'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
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
  loginUser: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'submitted'])

const activeModalTab = ref('form')
const hoverRating = ref(0)
const isSubmitting = ref(false)
const isLoadingHistory = ref(false)
const errorMessage = ref('')
const submissionNotice = ref('')
const feedbackHistory = ref([])
const manualLookupEmail = ref('')

const form = reactive({
  email: '',
  mobile_no: '',
  rating: 5,
  message: ''
})

const currentUserEmail = computed(() => {
  if (props.loginUser?.email) {
    return props.loginUser.email.trim()
  }
  if (typeof window !== 'undefined' && window.frappe?.session?.user && window.frappe.session.user !== 'Guest' && window.frappe.session.user.includes('@')) {
    return window.frappe.session.user.trim()
  }
  return ''
})

const isLoggedIn = computed(() => Boolean(currentUserEmail.value))

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

const groupedHistory = computed(() => {
  const groups = {}
  feedbackHistory.value.forEach((item) => {
    const rawDate = item.formatted_date || ''
    const dateLabel = rawDate.includes(',') ? rawDate.split(',')[0].trim() : (rawDate || 'Recent')
    if (!groups[dateLabel]) {
      groups[dateLabel] = []
    }
    groups[dateLabel].push(item)
  })
  return groups
})

const getUserInitial = (emailStr) => {
  if (!emailStr) return 'U'
  const clean = emailStr.replace(/[^a-zA-Z0-9]/g, '')
  return clean ? clean.charAt(0).toUpperCase() : 'U'
}

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

const fetchFeedbackHistory = async (showLoading = true) => {
  const emailToFetch = effectiveEmail.value
  if (!emailToFetch || !emailToFetch.includes('@')) {
    feedbackHistory.value = []
    return
  }

  if (showLoading) {
    isLoadingHistory.value = true
  }

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
    }
  } catch (err) {
    feedbackHistory.value = []
  } finally {
    isLoadingHistory.value = false
  }
}

const switchToHistory = () => {
  activeModalTab.value = 'history'
  if (effectiveEmail.value) {
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
  if (effectiveEmail.value) {
    fetchFeedbackHistory(false)
  }
})

watch(() => props.isOpen, (val) => {
  if (val) {
    errorMessage.value = ''
    submissionNotice.value = ''
    form.rating = 5
    form.message = ''
    activeModalTab.value = 'form'
    loadSavedContact()
    if (effectiveEmail.value) {
      fetchFeedbackHistory(false)
    }
  }
})

const handleClose = () => {
  if (isSubmitting.value) return
  emit('close')
}

const handleSubmit = async () => {
  errorMessage.value = ''

  if (isLoggedIn.value && !form.email) {
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
    const payload = {
      email: form.email.trim(),
      rating: form.rating,
      message: form.message.trim(),
      tab_code: props.tabCode || '',
      tab_title: props.tabTitle || '',
      web_page: props.webPage || '',
      mobile_no: cleanMobile
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

      submissionNotice.value = 'Your feedback was successfully posted! View sent thread below.'
      form.message = ''

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
  border-radius: 18px;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: modal-pop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-accent-bar {
  height: 5px;
  background: linear-gradient(90deg, #3b82f6, #6366f1, #8b5cf6, #ec4899);
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
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  color: #2563eb;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.12);
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

.modal-tabs-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0 1.5rem 0.75rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.tab-nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-nav-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.tab-nav-btn.is-active {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
}

.history-count-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 5px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.25);
  color: inherit;
}

.tab-nav-btn:not(.is-active) .history-count-pill {
  background: #e2e8f0;
  color: #475569;
}

.modal-scroll-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem 1.5rem 1.5rem 1.5rem;
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

@media (max-width: 640px) {
  .form-row-2col {
    grid-template-columns: 1fr;
  }
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
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
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
  margin-top: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
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
  background: #2563eb;
  border: 1px solid transparent;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
}

.btn-primary:hover:not(:disabled) {
  background: #1d4ed8;
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

/* History Tab & Blog Comment Stream Styles */
.history-filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 0.65rem 1rem;
  margin-bottom: 1.25rem;
}

.history-user-info {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.history-user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.history-user-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.history-user-label {
  font-size: 0.72rem;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.history-user-email {
  font-size: 0.85rem;
  color: #1e293b;
}

.reload-history-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reload-history-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.spinning {
  animation: spin 0.75s linear infinite;
}

.email-prompt-box {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.25rem;
}

.email-prompt-text {
  font-size: 0.85rem;
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2.5rem 1.5rem;
  gap: 0.75rem;
}

.loading-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.empty-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #334155;
  margin: 0;
}

.empty-desc {
  font-size: 0.85rem;
  color: #64748b;
  max-width: 380px;
  margin: 0;
}

/* Date Stream & Blog Comment Threading */
.blog-comments-stream {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.date-stream-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.stream-date-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin: 0.5rem 0;
}

.stream-date-divider::before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: #e2e8f0;
  z-index: 1;
}

.date-chip {
  position: relative;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 0.2rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.blog-comment-thread {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
  transition: all 0.2s ease;
}

.blog-comment-thread:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.comment-bubble {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
}

.bubble-left {
  flex-shrink: 0;
}

.avatar-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 700;
}

.avatar-circle.user-avatar {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.2);
}

.avatar-circle.team-avatar {
  background: linear-gradient(135deg, #8b5cf6, #6366f1);
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.2);
}

.bubble-main {
  flex: 1;
  min-width: 0;
}

.bubble-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-bottom: 0.25rem;
}

.author-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.author-name {
  font-size: 0.85rem;
  font-weight: 700;
  color: #0f172a;
}

.author-name.team-name {
  color: #6366f1;
}

.comment-type-tag {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 0.1rem 0.45rem;
  border-radius: 4px;
}

.comment-type-tag.sent-tag {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #dbeafe;
}

.comment-type-tag.reply-tag {
  background: #f5f3ff;
  color: #6d28d9;
  border: 1px solid #ddd6fe;
}

.comment-time {
  font-size: 0.75rem;
  color: #94a3b8;
}

.bubble-rating-pill {
  display: flex;
  align-items: center;
}

.star-rating-render {
  display: inline-flex;
  gap: 1px;
}

.star-mini {
  font-size: 0.95rem;
  color: #e2e8f0;
  line-height: 1;
}

.star-mini.filled {
  color: #f59e0b;
}

.comment-context-row {
  margin: 0.2rem 0 0.5rem 0;
}

.context-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  background: #f1f5f9;
  color: #475569;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.bubble-body {
  margin-top: 0.35rem;
}

.comment-text {
  font-size: 0.875rem;
  line-height: 1.5;
  color: #334155;
  margin: 0;
  word-break: break-word;
}

.bubble-status-row {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
}

.status-badge.status-replied {
  background: #ecfdf5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.status-badge.status-pending {
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
}

/* Reply Threading */
.reply-thread-wrap {
  position: relative;
  margin-left: 1.25rem;
  padding-left: 1.25rem;
  border-left: 2px solid #8b5cf6;
}

.thread-connector-branch {
  position: absolute;
  top: 18px;
  left: 0;
  width: 14px;
  height: 2px;
  background: #8b5cf6;
}

.reply-comment {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 0.85rem;
}

.reply-body {
  margin-top: 0.35rem;
}

.reply-text {
  color: #1e293b;
  font-weight: 500;
}

.reply-pending-notice {
  position: relative;
  margin-left: 1.25rem;
  padding-left: 1.25rem;
  border-left: 2px dashed #cbd5e1;
}

.thread-connector-branch.subtle {
  background: #cbd5e1;
}

.pending-bubble {
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  color: #64748b;
  font-style: italic;
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
</style>
