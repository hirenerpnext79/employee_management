<template>
  <div class="about-facts">
    <div class="section-header">
      <h2>OUR FACTS</h2>
    </div>

    <!-- Top Facts Grid -->
    <div class="facts-grid">
      <div class="fact-item">
        <div class="fact-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 6v6l4 2"></path>
          </svg>
        </div>
        <p class="fact-text">Since 1987</p>
      </div>

      <div class="fact-item">
        <div class="fact-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
            <circle cx="12" cy="10" r="3"></circle>
          </svg>
        </div>
        <p class="fact-text">Exhaustive Presence in Western India</p>
      </div>

      <div class="fact-item">
        <div class="fact-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
          </svg>
        </div>
        <p class="fact-text">Served All Across India</p>
      </div>

      <div class="fact-item">
        <div class="fact-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M8 21h8M12 17v4"></path>
            <circle cx="12" cy="10" r="2"></circle>
            <path d="M16 10a4 4 0 0 0-8 0"></path>
          </svg>
        </div>
        <p class="fact-text">Designed & Implemented Business Application Software Solutions</p>
      </div>
    </div>

    <!-- Value Proposition Section -->
    <div class="value-prop-container">
      <div class="value-prop-card">
        <div class="target-icon-wrapper">
          <svg class="target-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" stroke="#ef4444"></circle>
            <circle cx="12" cy="12" r="6" stroke="#f59e0b"></circle>
            <circle cx="12" cy="12" r="2" stroke="#ef4444" fill="#ef4444"></circle>
            <path d="M22 2l-7 7" stroke="#10b981" stroke-linecap="round"></path>
            <path d="M15 9h-6v6" stroke="#10b981" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </div>
        <h3 class="value-prop-title">VALUE PROPOSITION</h3>
      </div>

      <div class="value-prop-stats">
        <div class="stat-block">
          <h4 class="stat-highlight">1st</h4>
          <p class="stat-desc">IT Vendor in entire Western India in implementing Bar Code solution way back in 1989</p>
        </div>
        
        <div class="stat-block">
          <h4 class="stat-highlight">350+</h4>
          <p class="stat-desc">Happy customers in our stable and still counting</p>
        </div>

        <div class="stat-block">
          <h4 class="stat-highlight">20+</h4>
          <p class="stat-desc">Industry domains served for providing IT Enterprise Level Solutions</p>
        </div>

        <div class="stat-block">
          <h4 class="stat-highlight">Awarded</h4>
          <p class="stat-desc">"Best Software Implementer in South Gujarat" many a times</p>
        </div>

        <div class="stat-block">
          <h4 class="stat-highlight">PAN India</h4>
          <p class="stat-desc">Presence with offices in Surat and Mumbai</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-facts {
  margin: 5rem 0;
  width: 100%;
}

.section-header {
  background-color: #1e3a8a;
  color: white;
  text-align: center;
  padding: 15px 20px;
  margin-bottom: 30px;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.section-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
  text-transform: uppercase;
}

/* Facts Grid */
.facts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3rem 2rem;
  margin-bottom: 5rem;
  text-align: center;
}

@media (min-width: 768px) {
  .facts-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.fact-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.fact-icon {
  width: 80px;
  height: 80px;
  background: #eff6ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1e3a8a;
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease, background 0.3s ease;
}

.fact-icon svg {
  width: 40px;
  height: 40px;
}

.fact-item:hover .fact-icon {
  transform: scale(1.1);
  background: #dbeafe;
}

.fact-text {
  font-weight: 600;
  color: #475569;
  font-size: 1rem;
  line-height: 1.4;
  margin: 0;
}

/* Value Proposition */
.value-prop-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 3rem;
  background: #f8fafc;
  padding: 3rem;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
}

@media (min-width: 992px) {
  .value-prop-container {
    grid-template-columns: 1fr 1.5fr;
    align-items: center;
  }
}

.value-prop-card {
  background: white;
  border: 2px solid #1e3a8a;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.target-icon-wrapper {
  width: 120px;
  height: 120px;
  margin-bottom: 2rem;
}

.target-icon {
  width: 100%;
  height: 100%;
}

.value-prop-title {
  color: #1e3a8a;
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: 1.5px;
  margin: 0;
}

.value-prop-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stat-block {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.stat-block:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.stat-highlight {
  color: #1e3a8a;
  font-size: 1.5rem;
  font-weight: 800;
  margin: 0 0 0.5rem 0;
}

.stat-desc {
  color: #475569;
  font-size: 1rem;
  line-height: 1.5;
  margin: 0;
}
</style>
