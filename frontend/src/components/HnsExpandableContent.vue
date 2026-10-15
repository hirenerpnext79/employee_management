<template>
  <div class="hns-expandable-content" :class="customClass">
    <div class="expandable-html-body" v-html="displayHtml"></div>
    <div v-if="showToggle" class="expandable-toggle-wrapper">
      <button 
        type="button" 
        class="expandable-toggle-btn"
        @click="isExpanded = !isExpanded"
        :aria-expanded="isExpanded"
      >
        <span>{{ buttonLabel }}</span>
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          width="14" 
          height="14" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          stroke-width="2.2" 
          stroke-linecap="round" 
          stroke-linejoin="round"
          class="toggle-chevron"
          :class="{ 'is-expanded': isExpanded }"
        >
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  wordLimit: {
    type: [Number, String],
    default: 0
  },
  mobileFactor: {
    type: [Number, String],
    default: 1
  },
  readMoreText: {
    type: String,
    default: ''
  },
  customClass: {
    type: String,
    default: ''
  }
})

const isExpanded = ref(false)
const isMobile = ref(false)

const checkIsMobile = () => {
  if (typeof window !== 'undefined') {
    isMobile.value = window.innerWidth <= 768
  }
}

onMounted(() => {
  checkIsMobile()
  window.addEventListener('resize', checkIsMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkIsMobile)
})

watch(() => props.content, () => {
  isExpanded.value = false
})

const effectiveLimit = computed(() => {
  const base = Number(props.wordLimit)
  if (!base || base <= 0) {
    return 0
  }
  if (isMobile.value) {
    const factor = Number(props.mobileFactor) > 0 ? Number(props.mobileFactor) : 1
    return Math.max(1, Math.floor(base / factor))
  }
  return base
})

const truncateHtmlByWords = (htmlStr, maxWords) => {
  if (!htmlStr || maxWords <= 0) return { html: htmlStr || '', truncated: false, wordCount: 0 }
  if (typeof document === 'undefined') return { html: htmlStr, truncated: false, wordCount: 0 }

  const div = document.createElement('div')
  div.innerHTML = htmlStr
  const text = div.textContent || div.innerText || ''
  const words = text.trim().split(/\s+/).filter(Boolean)
  const wordCount = words.length

  if (wordCount <= maxWords) {
    return { html: htmlStr, truncated: false, wordCount }
  }

  const clone = div.cloneNode(true)
  let currentWords = 0
  let isTruncated = false

  const traverse = (node) => {
    if (isTruncated) {
      node.remove()
      return
    }

    if (node.nodeType === Node.TEXT_NODE) {
      const nodeText = node.textContent || ''
      const nodeWords = nodeText.trim().split(/\s+/).filter(Boolean)
      if (nodeWords.length === 0) return

      if (currentWords + nodeWords.length <= maxWords) {
        currentWords += nodeWords.length
      } else {
        const remaining = maxWords - currentWords
        const matches = [...nodeText.matchAll(/\S+/g)]
        if (matches.length >= remaining && remaining > 0) {
          const lastMatch = matches[remaining - 1]
          const cutIndex = lastMatch.index + lastMatch[0].length
          node.textContent = nodeText.slice(0, cutIndex) + '...'
        } else {
          node.textContent = '...'
        }
        currentWords = maxWords
        isTruncated = true
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      const children = Array.from(node.childNodes)
      for (const child of children) {
        if (isTruncated) {
          child.remove()
        } else {
          traverse(child)
        }
      }
      if (!node.hasChildNodes() && !['IMG', 'BR', 'HR', 'INPUT', 'VIDEO', 'IFRAME'].includes(node.tagName)) {
        node.remove()
      }
    }
  }

  traverse(clone)
  return { html: clone.innerHTML, truncated: true, wordCount }
}

const truncatedData = computed(() => {
  if (effectiveLimit.value <= 0 || !props.content) {
    return { html: props.content || '', truncated: false, wordCount: 0 }
  }
  return truncateHtmlByWords(props.content, effectiveLimit.value)
})

const showToggle = computed(() => {
  if (effectiveLimit.value <= 0) return false
  return truncatedData.value.truncated
})

const displayHtml = computed(() => {
  if (effectiveLimit.value <= 0 || isExpanded.value || !truncatedData.value.truncated) {
    return props.content
  }
  return truncatedData.value.html
})

const buttonLabel = computed(() => {
  const custom = (props.readMoreText || '').trim()
  if (!isExpanded.value) {
    return custom || 'Read More'
  }
  if (!custom) {
    return 'Read Less'
  }
  if (/more/i.test(custom)) {
    return custom.replace(/more/gi, (match) => {
      if (match === 'MORE') return 'LESS'
      if (match === 'More') return 'Less'
      return 'less'
    })
  }
  return 'Read Less'
})
</script>

<style scoped>
.hns-expandable-content {
  position: relative;
  width: 100%;
}

.expandable-html-body {
  width: 100%;
  line-height: 1.65;
  color: inherit;
}

.expandable-toggle-wrapper {
  margin-top: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 100%;
}

.expandable-toggle-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: transparent;
  border: none;
  padding: 0.25rem 0.4rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #2563eb;
  cursor: pointer;
  border-radius: 6px;
  transition: color 0.2s ease;
  user-select: none;
}

.expandable-toggle-btn:hover {
  background-color: transparent;
  color: #1d4ed8;
}

.toggle-chevron {
  transition: transform 0.25s ease;
}

.toggle-chevron.is-expanded {
  transform: rotate(180deg);
}
</style>
