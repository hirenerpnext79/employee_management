<template>
  <div class="vcard-wrapper">
    <!-- Background Glows -->
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>

    <div v-if="loading" class="loader-container">
      <div class="pulse-ring"></div>
      <p>Loading profile...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
      </div>
      <h2 class="error-title">Access Denied</h2>
      <p class="error-message">{{ error }}</p>
    </div>

    <div v-else-if="employee" class="profile-card">
      <!-- Profile Picture -->
      <div class="avatar-container">
        <div class="avatar-glow"></div>
        <img v-if="employee.image" class="avatar" :src="employee.image" :alt="employee.display_name" />
        <div v-else class="avatar initials-avatar">
          {{ initials }}
        </div>
      </div>

      <!-- Identity Details -->
      <h1 class="name">{{ employee.display_name }}</h1>
      <div v-if="employee.designation" class="designation">{{ employee.designation }}</div>
      
      <div class="company-department">
        <span v-if="employee.department">{{ employee.department }}</span>
        <span v-if="employee.department && employee.company"> &middot; </span>
        <span v-if="employee.company">{{ employee.company }}</span>
      </div>

      <!-- Contact Details -->
      <div class="info-list">
        <a v-if="employee.cell_number" :href="'tel:' + employee.cell_number" class="info-item">
          <div class="info-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </svg>
          </div>
          <div class="info-content">
            <span class="info-label">Mobile</span>
            <span class="info-value">{{ employee.cell_number }}</span>
          </div>
        </a>

        <a v-if="employee.email" :href="'mailto:' + employee.email" class="info-item">
          <div class="info-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
          </div>
          <div class="info-content">
            <span class="info-label">Email</span>
            <span class="info-value">{{ employee.email }}</span>
          </div>
        </a>

        <div v-if="employee.company" class="info-item">
          <div class="info-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
              <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
            </svg>
          </div>
          <div class="info-content">
            <span class="info-label">Organization</span>
            <span class="info-value">{{ employee.company }}</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  token: {
    type: String,
    required: true
  }
})

const employee = ref(null)
const loading = ref(true)
const error = ref(null)

const initials = computed(() => {
  if (!employee.value) return 'E'
  const first = employee.value.first_name ? employee.value.first_name[0] : ''
  const last = employee.value.last_name ? employee.value.last_name[0] : ''
  return (first + last).toUpperCase() || 'E'
})

const fetchDetails = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/method/employee_management.api.get_vcard_details?token=${props.token}`)
    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData._server_messages ? JSON.parse(errData._server_messages)[0] : 'Failed to fetch details')
    }
    const data = await response.json()
    employee.value = data.message || null
  } catch (e) {
    console.error(e)
    error.value = e.message || 'Invalid token or employee record not found.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDetails()
})
</script>

<style scoped>
.vcard-wrapper {
  background-color: #080b11;
  color: #ffffff;
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}

/* Background glows */
.glow {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  filter: blur(100px);
  pointer-events: none;
  z-index: 0;
}

.glow-1 {
  background: rgba(99, 102, 241, 0.25);
  top: 15%;
  left: 10%;
}

.glow-2 {
  background: rgba(168, 85, 247, 0.25);
  bottom: 15%;
  right: 10%;
}

/* Card */
.profile-card {
  background: rgba(17, 22, 34, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  width: 100%;
  max-width: 420px;
  padding: 32px 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 
              0 0 50px rgba(99, 102, 241, 0.15);
  z-index: 10;
  text-align: center;
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Loading */
.loader-container {
  text-align: center;
  z-index: 10;
}

.pulse-ring {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(99, 102, 241, 0.3);
  border-radius: 50%;
  border-top-color: #6366f1;
  animation: spin 1s linear infinite;
  margin: 0 auto 16px;
}

.loader-container p {
  color: #94a3b8;
  font-size: 0.95rem;
}

/* Avatar */
.avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
}

.avatar-glow {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  border-radius: 50%;
  z-index: 1;
  opacity: 0.8;
  animation: rotateGlow 6s linear infinite;
}

.avatar {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #080b11;
  z-index: 2;
  background-color: #1e293b;
}

.initials-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Outfit', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

/* Identity info */
.name {
  font-family: 'Outfit', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
  background: linear-gradient(to right, #ffffff, #e2e8f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.designation {
  font-size: 1rem;
  font-weight: 500;
  color: #6366f1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 4px;
}

.company-department {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 32px;
}

/* Contact List */
.info-list {
  text-align: left;
  margin-bottom: 32px;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 14px;
  margin-bottom: 12px;
  transition: all 0.25s ease;
  text-decoration: none;
  color: inherit;
}

a.info-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: #6366f1;
  flex-shrink: 0;
  transition: all 0.25s ease;
}

a.info-item:hover .info-icon {
  background: rgba(99, 102, 241, 0.2);
  color: #ffffff;
}

.info-icon svg {
  width: 20px;
  height: 20px;
}

.info-content {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.info-label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 2px;
}

.info-value {
  font-size: 0.95rem;
  font-weight: 500;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Error style */
.error-container {
  background: rgba(17, 22, 34, 0.65);
  border: 1px solid rgba(239, 68, 68, 0.15);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  width: 100%;
  max-width: 420px;
  padding: 40px 24px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  z-index: 10;
}

.error-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.error-title {
  font-family: 'Outfit', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #ffffff;
}

.error-message {
  font-size: 0.95rem;
  color: #94a3b8;
  line-height: 1.5;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes rotateGlow {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
