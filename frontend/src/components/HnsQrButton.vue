<template>
  <button
    type="button"
    class="hns-qr-btn banner"
    :title="title || 'Download QR Code'"
    @click.stop="handleDownload"
    :disabled="isGenerating"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect width="5" height="5" x="3" y="3" rx="1"/>
      <rect width="5" height="5" x="16" y="3" rx="1"/>
      <rect width="5" height="5" x="3" y="16" rx="1"/>
      <path d="M21 16h-3a2 2 0 0 0-2 2v3"/>
      <path d="M21 21v.01"/>
      <path d="M12 7v3a2 2 0 0 1-2 2H7"/>
      <path d="M3 12h.01"/>
      <path d="M12 3h.01"/>
      <path d="M12 16v.01"/>
      <path d="M16 12h1"/>
      <path d="M21 12v.01"/>
      <path d="M12 21v-1"/>
    </svg>
    <span class="hns-qr-text-label">QR</span>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { buildSpecificUrl, generateAndDownloadQrCode } from '../utils/qrCodeHandler'
import { showToast } from '../utils/toastHandler'

const props = defineProps({
  groupName: {
    type: String,
    default: ''
  },
  tabName: {
    type: String,
    default: ''
  },
  targetCode: {
    type: String,
    default: ''
  },
  pageName: {
    type: String,
    default: ''
  },
  webCode: {
    type: String,
    default: ''
  },
  portalTitle: {
    type: String,
    default: ''
  },
  employeeName: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'banner'
  },
  title: {
    type: String,
    default: ''
  }
})

const isGenerating = ref(false)

const handleDownload = async () => {
  if (isGenerating.value) return
  isGenerating.value = true

  try {
    const targetUrl = buildSpecificUrl({
      pageName: props.pageName,
      targetCode: props.targetCode,
      webCode: props.webCode
    })

    const success = await generateAndDownloadQrCode({
      url: targetUrl,
      groupName: props.groupName,
      tabName: props.tabName,
      portalTitle: props.portalTitle,
      employeeName: props.employeeName
    })

    if (success) {
      const label = props.tabName || props.groupName || 'Section'
      showToast(`QR Code downloaded for ${label}`, 'success', 3000)
    } else {
      showToast('Could not generate QR Code', 'error', 3000)
    }
  } catch (error) {
    showToast('Failed to download QR Code', 'error', 3000)
  } finally {
    isGenerating.value = false
  }
}
</script>

<style scoped>
.hns-qr-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  cursor: pointer;
  line-height: 1;
  transition: none;
}

.hns-qr-btn.banner {
  background: #ffffff;
  color: #000000;
  border: 1.5px solid #000000;
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  transition: none;
}

.hns-qr-btn.banner:hover {
  background: #ffffff;
  color: #000000;
  border-color: #000000;
  transform: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.hns-qr-btn.banner:active {
  transform: none;
}

.hns-qr-text-label {
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.hns-qr-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
