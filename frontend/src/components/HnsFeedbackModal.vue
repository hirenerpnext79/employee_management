<template>
  <teleport to="body">
    <transition name="feedback-modal-fade">
      <div v-if="isOpen" class="feedback-modal-overlay" @click.self="handleClose">
        <div class="feedback-modal-card" role="dialog" aria-modal="true">
          <!-- Top Accent Bar -->
          <div class="modal-accent-bar"></div>

          <!-- Modal Header -->
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
                <h3 class="modal-title">Share Your Feedback</h3>
                <p class="modal-subtitle" v-if="tabTitle || tabCode">
                  Feedback for: <strong>{{ tabTitle || tabCode }}</strong>
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

          <!-- Success State -->
          <div v-if="isSuccess" class="modal-success-state">
            <div class="success-icon-wrap">
              <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"></path>
              </svg>
            </div>
            <h4 class="success-title">Feedback Submitted!</h4>
            <p class="success-desc">Thank you for taking the time to share your feedback for <strong>{{ tabTitle || tabCode }}</strong>.</p>
            <button type="button" class="btn-primary" @click="handleClose" style="margin-top: 1rem;">Done</button>
          </div>

          <!-- Feedback Form -->
          <form v-else @submit.prevent="handleSubmit" class="modal-form">
            <!-- Error Banner -->
            <div v-if="errorMessage" class="modal-error-banner">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <span>{{ errorMessage }}</span>
            </div>

            <!-- Rating Input -->
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

            <!-- Contact Row (Email & Mobile) -->
            <div class="form-row-2col">
              <!-- Email Input -->
              <div class="form-group">
                <label class="form-label" for="feedback-email">
                  Email Address <span class="reqd-star">*</span>
                </label>
                <input
                  id="feedback-email"
                  type="email"
                  v-model="form.email"
                  class="form-input"
                  placeholder="name@company.com"
                  required
                />
              </div>

              <!-- Mobile No Input -->
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

            <!-- Message Input -->
            <div class="form-group">
              <label class="form-label" for="feedback-message">
                Message / Comments <span class="reqd-star">*</span>
              </label>
              <textarea
                id="feedback-message"
                v-model="form.message"
                class="form-textarea"
                rows="3"
                placeholder="Share your thoughts, suggestions, or issues..."
                required
              ></textarea>
            </div>

            <!-- Modal Footer -->
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
  }
})

const emit = defineEmits(['close', 'submitted'])

const hoverRating = ref(0)
const isSubmitting = ref(false)
const isSuccess = ref(false)
const errorMessage = ref('')

const form = reactive({
  email: '',
  mobile_no: '',
  rating: 5,
  message: ''
})

const loadSavedContact = () => {
  const { email, mobile } = getFeedbackContact()
  if (email) {
    form.email = email
  }
  if (mobile) {
    form.mobile_no = mobile
  }
}

onMounted(() => {
  loadSavedContact()
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

watch(() => props.isOpen, (val) => {
  if (val) {
    isSuccess.value = false
    errorMessage.value = ''
    form.rating = 5
    form.message = ''
    loadSavedContact()
  }
})

const handleClose = () => {
  if (isSubmitting.value) return
  emit('close')
}

const handleSubmit = async () => {
  errorMessage.value = ''

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
      isSuccess.value = true
      setFeedbackContact(form.email.trim(), form.mobile_no ? form.mobile_no.trim() : '')
      showToast('Thank you for your feedback!', 'success')
      emit('submitted', payload)
      setTimeout(() => {
        handleClose()
      }, 1500)
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
  background-color: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(6px);
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
  max-width: 650px;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: modal-pop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.form-row-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .form-row-2col {
    grid-template-columns: 1fr;
  }
}

.modal-accent-bar {
  height: 5px;
  background: linear-gradient(90deg, #3b82f6, #f59e0b, #10b981);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1.25rem 1.5rem 0.75rem 1.5rem;
}

.header-left {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
}

.header-icon-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: #eff6ff;
  color: #2563eb;
  flex-shrink: 0;
}

.modal-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  line-height: 1.3;
}

.modal-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0.25rem 0 0 0;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tab-code-pill {
  display: inline-block;
  padding: 0.1rem 0.4rem;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 0.75rem;
  font-family: monospace;
  color: #475569;
}

.modal-close-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background: #f1f5f9;
  color: #334155;
}

.modal-form {
  padding: 0.75rem 1.5rem 1.5rem 1.5rem;
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
  border-radius: 8px;
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

.modal-success-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2.5rem 1.5rem;
}

.success-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #ecfdf5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.success-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #065f46;
  margin: 0;
}

.success-desc {
  font-size: 0.9rem;
  color: #4b5563;
  margin: 0.5rem 0 0 0;
  max-width: 340px;
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
