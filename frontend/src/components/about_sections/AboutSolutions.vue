<template>
  <div class="about-solutions">
    <div class="solutions-grid">
      
      <!-- ERPNext Card -->
      <div class="solution-card erpnext-card">
        <div class="card-content">
          <h3 class="card-title">ERPNEXT : OPEN SOURCE ERP</h3>
          <ul class="feature-list">
            <li>Garment Manufacturing</li>
            <li>Hospital Management</li>
            <li>Color Chemical Manufacturing</li>
            <li>Construction Industry</li>
          </ul>
        </div>
        <div class="card-icon-area">
          <div class="icon-circle">
            <span class="erp-letter">E</span>
          </div>
          <span class="icon-label">ERPNext</span>
        </div>
      </div>

      <!-- SAP Card -->
      <div class="solution-card sap-card">
        <div class="card-content">
          <h3 class="card-title">SAP BUSINESS ONE & ADD-ONS</h3>
          <ul class="feature-list">
            <li>Dynamic Report</li>
            <li>On Demand Reporting System</li>
            <li>Analytical Graphical Reporting Add-on</li>
            <li>Report Robot</li>
          </ul>
        </div>
        <div class="card-icon-area">
          <svg class="solution-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="4" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/>
            <path d="M8 10H16M8 14H12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="icon-label">SAP</span>
        </div>
      </div>

      <!-- Zoho Card -->
      <div class="solution-card zoho-card">
        <div class="card-content">
          <h3 class="card-title">ZOHO SOLUTIONS</h3>
          <ul class="feature-list">
            <li>Zoho CRM</li>
            <li>Zoho Books</li>
            <li>Zoho One</li>
          </ul>
        </div>
        <div class="card-icon-area">
          <div class="zoho-shapes">
            <div class="shape red"></div>
            <div class="shape green"></div>
            <div class="shape yellow"></div>
            <div class="shape blue"></div>
          </div>
          <span class="icon-label">ZOHO</span>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.about-solutions {
  margin: 4rem 0;
  width: 100%;
}

.solutions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .solutions-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.solution-card {
  border-radius: 16px;
  padding: 2.5rem 2rem;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 400px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.solution-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

/* Background Gradients */
.erpnext-card {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
}

.sap-card {
  background: linear-gradient(135deg, #84cc16 0%, #65a30d 100%);
}

.zoho-card {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 1px;
  margin-top: 0;
  margin-bottom: 2rem;
  line-height: 1.4;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  position: relative;
  padding-left: 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  font-weight: 500;
  opacity: 0.95;
  line-height: 1.4;
}

.feature-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: white;
  font-size: 1.2rem;
  line-height: 1;
}

/* Decorative Icon Areas */
.card-icon-area {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.15);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.icon-circle {
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.erp-letter {
  color: #ea580c;
  font-size: 2rem;
  font-weight: 800;
}

.solution-svg {
  width: 60px;
  height: 60px;
  color: white;
  margin-bottom: 1rem;
}

.zoho-shapes {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 1rem;
}

.shape {
  width: 25px;
  height: 25px;
  border-radius: 4px;
}

.shape.red { background: #ef4444; border-radius: 50%; }
.shape.green { background: #22c55e; }
.shape.yellow { background: #eab308; clip-path: polygon(50% 0%, 0% 100%, 100% 100%); border-radius: 0; }
.shape.blue { background: #3b82f6; border-radius: 8px 0 8px 0; }

.icon-label {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: 2px;
  opacity: 0.9;
}
</style>
