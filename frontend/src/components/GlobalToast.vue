<template>
  <div v-if="toastState.message" class="global-toast" :class="toastState.type">
    <div class="toast-content">
      <!-- Error Icon -->
      <svg v-if="toastState.type === 'error'" xmlns="http://www.w3.org/2000/svg" class="toast-icon" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      <!-- Success Icon -->
      <svg v-else xmlns="http://www.w3.org/2000/svg" class="toast-icon" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
      </svg>
      <span>{{ toastState.message }}</span>
    </div>
    <button @click="clearToast" class="close-btn">&times;</button>
  </div>
</template>

<script setup>
import { toastState, clearToast } from '../utils/toastHandler'
</script>

<style scoped>
.global-toast {
  position: fixed;
  top: 24px;
  right: 24px;
  color: white;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  z-index: 9999;
  font-family: 'Inter', sans-serif;
  animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  max-width: 400px;
}

.global-toast.error {
  background-color: #ef4444; /* red-500 */
}

.global-toast.success {
  background-color: #10b981; /* emerald-500 */
}

.toast-content {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  font-size: 0.95rem;
}

.toast-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover {
  color: white;
}

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
</style>
