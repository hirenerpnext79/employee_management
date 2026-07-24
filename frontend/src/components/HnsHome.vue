<template>
  <div class="hns-home-wrapper">
    <!-- Premium Slider Section -->
    <BannerSlider />

    <div class="homepage-sections">
      <!-- Section 1: Our Solution Platforms -->
      <section class="section platforms-section">
        <h2 class="section-heading">OUR SOLUTION PLATFORMS</h2>
        <div class="platforms-container">
          <img src="https://via.placeholder.com/150?text=ERPNext" alt="ERPNext" class="platform-logo" />
          <img src="https://via.placeholder.com/150?text=SAP" alt="SAP Partner" class="platform-logo" />
          <img src="https://via.placeholder.com/150?text=ZOHO" alt="ZOHO" class="platform-logo" />
        </div>
      </section>

      <!-- Section 2: Our Offerings -->
      <section class="section offerings-section">
        <h2 class="section-heading">OUR OFFERINGS</h2>
        <div class="offerings-grid">
          <div class="offering-card">
            <div class="offering-icon"><i class="fa fa-mobile fa-3x"></i></div>
            <h3 class="offering-title">ERPNext Solutions</h3>
            <p class="offering-desc">ERPNext, one of the best Open Source ERP Software, gets you totally free from recurring license costs. It is a truly Complete ERP in the sense it covers all aspects of managing any Business.</p>
          </div>
          <div class="offering-card">
            <div class="offering-icon"><i class="fa fa-laptop fa-3x"></i></div>
            <h3 class="offering-title">SAP B1 Solutions</h3>
            <p class="offering-desc">SAP Business One is an affordable, easy-to-implement business management solution designed specifically to meet the needs of emerging and dynamically growing small and medium-sized organizations.</p>
          </div>
          <div class="offering-card">
            <div class="offering-icon"><i class="fa fa-cogs fa-3x"></i></div>
            <h3 class="offering-title">ZOHO Solutions</h3>
            <p class="offering-desc">We offer Solutions & Support for the entire range of ZOHO Modules ranging from Accounts to CRM to ZIA.</p>
          </div>
          <div class="offering-card">
            <div class="offering-icon"><i class="fa fa-user-tie fa-3x"></i></div>
            <h3 class="offering-title">TEX NEXT</h3>
            <p class="offering-desc">Tex Next is a comprehensive solution for the Textile Industry powered by ERPNext. It is designed specifically to handle the complexities of the Textile Industry.</p>
          </div>
          <div class="offering-card">
            <div class="offering-icon"><i class="fa fa-file-text fa-3x"></i></div>
            <h3 class="offering-title">DYNAREPS</h3>
            <p class="offering-desc">DynaReps is a Reporting application which is external to SAP B1 and does not require any SAP B1 Licenses for User to access the reports.</p>
          </div>
          <div class="offering-card">
            <div class="offering-icon"><i class="fa fa-shopping-cart fa-3x"></i></div>
            <h3 class="offering-title">E-COMMERCE SOLUTION</h3>
            <p class="offering-desc">Specialising in Ecommerce solutions, Ecommerce websites and online retail solutions. BlueArc can help your business take advantage of the growing Ecommerce channel.</p>
          </div>
        </div>
      </section>

      <!-- Section 3: From the CEOs Desk -->
      <section class="section ceos-desk-section">
        <h2 class="section-heading">FROM THE CEOS DESK</h2>
        <div class="videos-container">
          <div class="video-placeholder">Video 1 Placeholder</div>
          <div class="video-placeholder">Video 2 Placeholder</div>
        </div>
      </section>

      <!-- Section 4: Why Hard 'N Soft -->
      <section class="section why-us-section">
        <h2 class="section-heading">WHY HARD 'N SOFT</h2>
        <div class="stats-container">
          <div class="stat-item">
            <h2 class="stat-number">35+</h2>
            <h4 class="stat-title">YEARS OF EXPERIENCE</h4>
            <p class="stat-desc">In delivering Enterprise Business Solutions</p>
          </div>
          <div class="stat-item">
            <h2 class="stat-number">50+</h2>
            <h4 class="stat-title">RESOURCES</h4>
            <p class="stat-desc">Seasoned Professionals with huge Techno Functional Expertise</p>
          </div>
          <div class="stat-item">
            <h2 class="stat-number">350+</h2>
            <h4 class="stat-title">CLIENTS</h4>
            <p class="stat-desc">Across a huge number of Manufacturing Domains</p>
          </div>
        </div>
      </section>

      <!-- Section 5: 100% Satisfaction Guarantee -->
      <section class="section guarantee-section">
        <h3>100% Satisfaction Guarantee</h3>
        <button class="btn-contact">CONTACT US</button>
      </section>

      <!-- Section 6: They've Already Trusted Us -->
      <section class="section trusted-section">
        <h3 class="trusted-heading">THEY'VE ALREADY TRUSTED US</h3>
        <div class="trusted-logos">
          <div class="logo-box">Logo 1</div>
          <div class="logo-box">Logo 2</div>
          <div class="logo-box">Logo 3</div>
          <div class="logo-box">Logo 4</div>
        </div>
        
        <div class="testimonial-slider">
          <p class="testimonial-text">"We needed a scalable, integrated solution that could grow with the organization, offer accurate insight into all areas of the business and provide easy access to real-time information..."</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import BannerSlider from './BannerSlider.vue'
</script>

<style scoped>
.hns-home-wrapper {
  padding: 0;
  width: 100%;
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
}

.homepage-sections {
  display: flex;
  flex-direction: column;
  gap: 40px;
  margin-top: 40px;
}

.section-heading, .trusted-heading {
  margin: 0 auto 30px auto;
  padding: 15px 20px;
  font-weight: bold;
  font-size: 1.5rem;
  background-color: #1e3a8a;
  color: white;
  text-align: center;
  border-radius: 6px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
  width: calc(100% - 40px);
  text-transform: uppercase;
}

.platforms-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  padding: 40px 20px;
  flex-wrap: wrap;
}

.platform-logo {
  max-height: 80px;
  object-fit: contain;
}

.offerings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.offering-card {
  border: 1px solid #cce5ff;
  padding: 40px 20px;
  background: #fff;
  transition: transform 0.3s;
  text-align: center;
}

.offering-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.offering-icon {
  color: #0056b3;
  margin-bottom: 20px;
}

.offering-title {
  color: #002b5e;
  font-weight: bold;
  margin-bottom: 15px;
}

.offering-desc {
  color: #666;
  line-height: 1.6;
}

.videos-container {
  display: flex;
  justify-content: center;
  gap: 40px;
  padding: 40px 20px;
  flex-wrap: wrap;
}

.video-placeholder {
  width: 45%;
  min-width: 300px;
  height: 300px;
  border: 2px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  color: #888;
}

.stats-container {
  display: flex;
  justify-content: space-around;
  text-align: center;
  padding: 60px 20px;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-item {
  width: 30%;
  min-width: 250px;
  margin-bottom: 30px;
}

.stat-number {
  font-size: 4rem;
  font-weight: bold;
  color: #0056b3;
  margin-bottom: 10px;
}

.stat-title {
  font-weight: bold;
  color: #002b5e;
  margin-bottom: 15px;
}

.stat-desc {
  color: #666;
  font-size: 1rem;
}

.guarantee-section {
  background-color: #1e3a8a;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px 60px;
  flex-wrap: wrap;
  gap: 20px;
}

.guarantee-section h3 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: normal;
}

.btn-contact {
  background: white;
  color: #002b5e;
  border: none;
  padding: 12px 30px;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-contact:hover {
  background: #f0f0f0;
}

/* .trusted-heading styling merged into .section-heading above */

.trusted-logos {
  background-color: #1e3a8a;
  display: flex;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  flex-wrap: wrap;
}

.logo-box {
  background: white;
  padding: 15px 30px;
  min-width: 120px;
  text-align: center;
  color: #333;
}

.testimonial-slider {
  background: #f4f6f9;
  padding: 60px 20px;
  text-align: center;
}

.testimonial-text {
  font-style: italic;
  color: #555;
  font-size: 1.2rem;
  line-height: 1.8;
  max-width: 800px;
  margin: 0 auto;
}
</style>
