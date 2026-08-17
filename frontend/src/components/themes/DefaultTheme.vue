<template>
  <div class="premium-glass-theme">
    <div class="glass-card">
      <div class="avatar-container">
        <img 
          :src="employee.image || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(employee.employee_name || 'Employee') + '&background=random&color=fff'" 
          :alt="employee.employee_name" 
          class="avatar-img" 
        />
      </div>
      
      <div class="card-content">
        <h2 class="employee-name">{{ employee.display_name || employee.full_name || employee.employee_name }}</h2>
        <div class="badges">
          <span class="badge designation">{{ employee.designation }}</span>
          <span class="badge department">{{ employee.department }}</span>
        </div>

        <div class="details-grid">
          <div class="detail-row" v-if="employee.employee_number">
            <span class="icon">👤</span>
            <div class="detail-text">
              <span class="label">Employee ID</span>
              <span class="value">{{ employee.employee_number }}</span>
            </div>
          </div>
          <div class="detail-row" v-if="employee.gender">
            <span class="icon">⚥</span>
            <div class="detail-text">
              <span class="label">Gender</span>
              <span class="value">{{ employee.gender }}</span>
            </div>
          </div>
          <div class="detail-row" v-if="employee.date_of_birth">
            <span class="icon">🎂</span>
            <div class="detail-text">
              <span class="label">Date of Birth</span>
              <span class="value">{{ employee.date_of_birth }}</span>
            </div>
          </div>
        </div>

        <div class="attachments-section" v-if="employee.attachments && employee.attachments.length">
          <h3 class="section-title">Documents & Links</h3>
          <div class="attachments-grid">
            <a v-for="attachment in employee.attachments" :key="attachment.name" :href="attachment.attachment" target="_blank" class="attachment-pill">
              <span class="pill-icon">📄</span>
              <span class="pill-text">{{ attachment.group_title || 'Attachment' }}</span>
            </a>
          </div>
        </div>
      </div>
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
.premium-glass-theme {
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 20px;
  box-sizing: border-box;
}

.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  overflow: hidden;
  position: relative;
  margin-top: 50px; /* Space for avatar */
}

.avatar-container {
  display: flex;
  justify-content: center;
  margin-top: -60px;
}

.avatar-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  background-color: #fff;
}

.card-content {
  padding: 30px 24px 40px;
  text-align: center;
  color: #fff;
}

.employee-name {
  margin: 0 0 12px;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.badges {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge.designation {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.badge.department {
  background: rgba(0, 210, 255, 0.2);
  color: #bbf0ff;
  border: 1px solid rgba(0, 210, 255, 0.3);
}

.details-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
  text-align: left;
}

.detail-row {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.15);
  padding: 12px 16px;
  border-radius: 12px;
  transition: transform 0.2s ease, background 0.2s ease;
}

.detail-row:hover {
  transform: translateY(-2px);
  background: rgba(0, 0, 0, 0.25);
}

.icon {
  font-size: 24px;
  margin-right: 16px;
  opacity: 0.8;
}

.detail-text {
  display: flex;
  flex-direction: column;
}

.detail-text .label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.6;
  margin-bottom: 2px;
}

.detail-text .value {
  font-size: 15px;
  font-weight: 500;
}

.section-title {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.7;
  margin-bottom: 16px;
}

.attachments-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.attachment-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
  color: #fff;
  text-decoration: none;
  padding: 14px 20px;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 114, 255, 0.3);
}

.attachment-pill:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 114, 255, 0.5);
  filter: brightness(1.1);
}

.pill-icon {
  margin-right: 8px;
  font-size: 18px;
}
</style>
