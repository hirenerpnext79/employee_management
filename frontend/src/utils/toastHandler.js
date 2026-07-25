import { reactive } from 'vue'

export const toastState = reactive({
  message: null,
  type: 'error' // 'error' or 'success'
})

// Call this function from anywhere to show a global message
export const showToast = (message, type = 'error', timeout = 5000) => {
  toastState.message = message
  toastState.type = type
  
  if (timeout > 0) {
    setTimeout(() => {
      clearToast()
    }, timeout)
  }
}

// Keep showError for backward compatibility with components we already updated
export const showError = (message, timeout = 5000) => {
  showToast(message, 'error', timeout)
}

export const clearToast = () => {
  toastState.message = null
}

// Expose to window so standard JavaScript in CMS pages can use it instead of alert()
if (typeof window !== 'undefined') {
  window.showToast = showToast
}
