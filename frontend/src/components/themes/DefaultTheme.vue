<template>
  <div class="vcard-theme-default">
    <div class="header">
      <h2>{{ employee.display_name || employee.full_name }}</h2>
      <p class="designation">{{ employee.designation }}</p>
    </div>
    
    <div class="details">
      <div class="detail-item">
        <span class="label">Employee Number:</span>
        <span class="value">{{ employee.employee_number }}</span>
      </div>
      <div class="detail-item">
        <span class="label">Department:</span>
        <span class="value">{{ employee.department }}</span>
      </div>
      <div class="detail-item" v-if="employee.gender">
        <span class="label">Gender:</span>
        <span class="value">{{ employee.gender }}</span>
      </div>
      <div class="detail-item" v-if="employee.date_of_birth">
        <span class="label">Date of Birth:</span>
        <span class="value">{{ employee.date_of_birth }}</span>
      </div>
    </div>

    <div class="attachments" v-if="employee.attachments && employee.attachments.length">
      <h3>Attachments</h3>
      <ul>
        <li v-for="attachment in employee.attachments" :key="attachment.name">
          <a :href="attachment.attachment" target="_blank">{{ attachment.group_title || 'File' }}</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  employee: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.vcard-theme-default {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 10px;
}

.header h2 {
  margin: 0;
  color: #1a202c;
}

.designation {
  color: #4a5568;
  margin: 5px 0 0;
  font-weight: 500;
}

.details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px dashed #e2e8f0;
  padding-bottom: 5px;
}

.label {
  color: #718096;
  font-weight: 600;
}

.value {
  color: #2d3748;
}

.attachments {
  margin-top: 20px;
  border-top: 1px solid #e2e8f0;
  padding-top: 10px;
}

.attachments h3 {
  font-size: 1.1em;
  color: #2d3748;
  margin-bottom: 10px;
}
</style>
