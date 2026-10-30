<template>
  <div class="price-badge feedback-badge-standalone">
    <button 
      type="button" 
      class="price-feedback-btn standalone" 
      :title="title || 'Give Feedback'"
      @click="$emit('click', $event)"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        <path d="M12 7v2"></path>
        <path d="M12 13h.01"></path>
      </svg>
      <span>Feedback</span>
      <span 
        v-if="count > 0" 
        class="feedback-btn-count" 
        title="View feedback history"
      >{{ count }}</span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  count: {
    type: Number,
    default: 0
  },
  title: {
    type: String,
    default: 'Give Feedback'
  }
})

defineEmits(['click'])
</script>

<style scoped>
.price-badge {
  display: inline-flex;
  align-items: center;
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

.feedback-btn-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  box-sizing: border-box;
  min-width: 20px;
  height: 20px;
  padding: 1.5px 5px 0 5px;
  margin-left: 0.25rem;
  font-size: 0.72rem;
  font-weight: 700;
  line-height: 1;
  color: #ffffff;
  background: var(--group-title-color, #1e3a8a);
  border-radius: 9999px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  transition: transform 0.15s ease, background-color 0.15s ease;
  cursor: pointer;
  flex-shrink: 0;
}

.feedback-btn-count:hover {
  background: var(--sub-group-title-color, #118ab2);
  transform: scale(1.1);
}

.price-feedback-btn.standalone {
  gap: 0.4rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--group-title-color, #1e3a8a);
  padding: 0.35rem 0.65rem;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.price-feedback-btn.standalone:hover {
  color: var(--sub-group-title-color, #118ab2);
  background-color: transparent;
  transform: none;
}

.feedback-badge-standalone {
  background: #ffffff;
  border: 1.5px solid var(--group-title-color, #d1d5db);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  border-radius: 9999px;
  padding: 3px 8px;
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
}

.feedback-badge-standalone:hover {
  border-color: var(--sub-group-title-color, #118ab2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: none;
}
</style>
