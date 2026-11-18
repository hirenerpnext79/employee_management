<template>
  <div v-if="trimmedAnswer || trimmedExplanation" class="content-box-answer">
    <div v-if="trimmedAnswer" class="tab-answer-row">
      <div class="tab-answer-header">
        <svg
          class="tab-answer-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <span class="tab-answer-label">Answer</span>
      </div>
      <span class="tab-answer-badge">{{ trimmedAnswer }}</span>
    </div>

    <div
      v-if="trimmedExplanation"
      class="tab-explanation-block"
      :class="{ 'has-divider': Boolean(trimmedAnswer) }"
    >
      <div class="tab-explanation-header">
        <svg
          class="tab-explanation-icon"
          xmlns="http://www.w3.org/2000/svg"
          width="15"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
        <span class="tab-explanation-label">Explanation</span>
      </div>
      <div class="tab-explanation-text">{{ trimmedExplanation }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  answer: {
    type: String,
    default: ''
  },
  explanation: {
    type: String,
    default: ''
  }
})

const trimmedAnswer = computed(() => {
  return props.answer ? String(props.answer).trim() : ''
})

const trimmedExplanation = computed(() => {
  return props.explanation ? String(props.explanation).trim() : ''
})
</script>

<style scoped>
.content-box-answer {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-left: 4px solid #16a34a;
  border-radius: 12px;
  padding: 1.1rem 1.5rem;
  box-shadow: 0 1px 3px rgba(22, 163, 74, 0.06);
  width: 100%;
  box-sizing: border-box;
  color: #1e293b;
  line-height: 1.65;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.tab-answer-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.tab-answer-header,
.tab-explanation-header {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.tab-answer-icon {
  color: #16a34a;
  flex-shrink: 0;
}

.tab-answer-label {
  font-size: 0.84rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #15803d;
}

.tab-answer-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  padding: 0.15rem 0.65rem;
  border-radius: 9999px;
  background-color: #16a34a;
  color: #ffffff;
  font-size: 0.88rem;
  font-weight: 700;
  line-height: 1.4;
}

.tab-explanation-block {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.tab-explanation-block.has-divider {
  padding-top: 0.75rem;
  border-top: 1px solid #bbf7d0;
}

.tab-explanation-icon {
  color: #15803d;
  flex-shrink: 0;
}

.tab-explanation-label {
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #15803d;
}

.tab-explanation-text {
  font-size: 0.95rem;
  font-weight: 400;
  color: #1e293b;
  white-space: pre-line;
  word-break: break-word;
}

@media (max-width: 768px) {
  .content-box-answer {
    padding: 1rem 1.15rem;
  }
}
</style>
