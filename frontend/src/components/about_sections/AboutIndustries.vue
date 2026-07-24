<template>
  <div class="about-industries">
    <div class="section-header">
      <h2>INDUSTRY SEGMENTS</h2>
    </div>

    <div class="industries-grid">
      
      <!-- Textiles -->
      <div class="industry-item">
        <div class="industry-icon-wrapper bg-orange">
          <svg class="industry-svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20.38 3.46L16 2a8.5 8.5 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>
          </svg>
        </div>
        <p class="industry-title">Textiles</p>
      </div>

      <!-- Pharma -->
      <div class="industry-item">
        <div class="industry-icon-wrapper bg-green">
          <svg class="industry-svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 2v7.31M14 9.31V2M8.5 2h7M14 9.31L6.52 17.02c-.7.73-.34 2.98.98 2.98h9c1.32 0 1.68-2.25.98-2.98L14 9.31z"/>
            <circle cx="10" cy="15" r="1" fill="white"/>
            <circle cx="13" cy="18" r="1.5" fill="white"/>
            <circle cx="14" cy="14" r="0.5" fill="white"/>
          </svg>
        </div>
        <p class="industry-title">Pharma & Chemicals Manufacturing</p>
      </div>

      <!-- Engineering -->
      <div class="industry-item">
        <div class="industry-icon-wrapper bg-blue">
          <svg class="industry-svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.77 3.77z"/>
          </svg>
        </div>
        <p class="industry-title">Engineering</p>
      </div>

      <!-- Footwear -->
      <div class="industry-item">
        <div class="industry-icon-wrapper bg-yellow">
          <svg class="industry-svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 17c0 1.1-.9 2-2 2h-4.3a4 4 0 0 1-3.9-3.13l-.43-2.12a6 6 0 0 0-4.87-4.7l-2.07-.4A3.5 3.5 0 0 1 2 5.25V5a2 2 0 0 1 2-2h4c1.8 0 3.33 1.25 3.82 2.97L13 9.5l3.24 1.62c2.05 1.03 3.4 3 3.71 5.26l.05.62z"/>
          </svg>
        </div>
        <p class="industry-title">Footwear Manufacturing</p>
      </div>

      <!-- Packaging -->
      <div class="industry-item">
        <div class="industry-icon-wrapper bg-cyan">
          <svg class="industry-svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
            <line x1="12" y1="22.08" x2="12" y2="12"/>
          </svg>
        </div>
        <p class="industry-title">Packaging flexible & rigid</p>
      </div>

      <!-- Professionals -->
      <div class="industry-item">
        <div class="industry-icon-wrapper bg-orange-light">
          <svg class="industry-svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </div>
        <p class="industry-title">Professionals - CAs, Lawyers, Consultants etc</p>
      </div>

    </div>
  </div>
</template>

<style scoped>
.about-industries {
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

.industries-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3rem 1.5rem;
  text-align: center;
}

@media (min-width: 768px) {
  .industries-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 4rem 2rem;
  }
}

.industry-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.industry-icon-wrapper {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.industry-item:hover .industry-icon-wrapper {
  transform: scale(1.1) translateY(-5px);
  box-shadow: 0 12px 25px rgba(0,0,0,0.15);
}

.industry-svg {
  width: 45px;
  height: 45px;
}

.industry-title {
  font-weight: 600;
  color: #334155;
  font-size: 1.05rem;
  line-height: 1.4;
  margin: 0;
  max-width: 250px;
}

/* Colors matching the screenshots but modernized */
.bg-orange { background: linear-gradient(135deg, #f97316, #ea580c); }
.bg-green { background: linear-gradient(135deg, #84cc16, #65a30d); }
.bg-blue { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.bg-yellow { background: linear-gradient(135deg, #eab308, #ca8a04); }
.bg-cyan { background: linear-gradient(135deg, #06b6d4, #0891b2); }
.bg-orange-light { background: linear-gradient(135deg, #fb923c, #f97316); }
</style>
