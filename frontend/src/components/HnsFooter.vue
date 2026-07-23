<template>
  <footer class="footer">
    <div class="footer-overlay"></div>
    <div class="footer-content">
      
      <!-- About HNS Column -->
      <div class="footer-section about-section">
        <h3>About HNS</h3>
        <p class="about-text">Headquartered in Surat, Gujarat, India, Established in 1987, we focus on delivering solutions based on :</p>
        <ul class="star-list">
          <li><span class="star">★</span> ERPNext</li>
          <li><span class="star">★</span> SAP Business One (SAP B1)</li>
        </ul>
        <p class="about-text mt-3">We also specialise in adding immense value to these powerful ERP platforms :</p>
        <p class="highlight-text">Our Value Additions to ERPNext</p>
        
        <div class="search-box">
          <p class="search-label">Search</p>
          <div class="search-input-group">
            <input type="text" class="search-input" />
            <button class="search-btn">Search</button>
          </div>
        </div>
      </div>

      <!-- Quick Links Column -->
      <div class="footer-section links-section">
        <h3>Quick Links</h3>
        <ul class="footer-links">
          <li><a href="#what-we-do">What We Do</a></li>
          <li><a href="#why-us">Why Hard n Soft ?</a></li>
          <li><a href="#our-team">Our Team</a></li>
          <li><a href="#contact">Contact Us</a></li>
        </ul>
      </div>

      <!-- Contact Column -->
      <div class="footer-section contact-section">
        <h3>Get In Touch With Us</h3>
        
        <div class="contact-item">
          <svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
          <div class="contact-details">
            <span class="contact-title">Surat Office</span>
            <p>111 & 112, Valentino Business Complex,<br>Near INS Hospital, Khatodara, Surat -<br>395002.</p>
          </div>
        </div>

        <div class="contact-item">
          <svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
          <div class="contact-details">
            <span class="contact-title">Mumbai Office</span>
            <p>Mumbai Office: 711 - Crescent Business<br>Park, Nr. International Airport Sakinaka,<br>Andheri East, Mumbai.</p>
          </div>
        </div>

        <div class="contact-links mt-4">
          <a href="#" class="contact-link">
            <svg class="contact-icon-small" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
            +91 93777 78878
          </a>
          <a href="#" class="contact-link">
            <svg class="contact-icon-small" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 00-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99 3 13.28 10.73 21 20.03 21c.75 0 .99-.65.99-1.19v-3.44c0-.54-.45-.99-.99-.99z"/></svg>
            +91 99044 11154
          </a>
          <a href="mailto:dhaval@hnsindia.com" class="contact-link">
            <svg class="contact-icon-small" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
            dhaval@hnsindia.com
          </a>
        </div>

        <a href="#" class="whatsapp-btn">Chat on WhatsApp</a>
      </div>
      
    </div>
    
    <div class="footer-bottom">
      &copy; {{ new Date().getFullYear() }} HNS India. All rights reserved.
    </div>
  </footer>
</template>

<style scoped>
.footer {
  position: relative;
  background: #0f172a; /* Premium Dark Navy */
  padding: 4rem 5% 1.5rem;
  font-family: 'Inter', sans-serif;
  color: #cbd5e1;
  overflow: hidden;
  border-top: 2px solid #1e293b;
}

.footer-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(circle at 10% 90%, rgba(30, 58, 138, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 90% 10%, rgba(56, 189, 248, 0.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.footer-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr 1.2fr;
  gap: 3rem;
  max-width: 1280px;
  margin: 0 auto 3rem;
}

.footer-section h3 {
  color: #ffffff;
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  letter-spacing: 0.5px;
}

/* About Section */
.about-text {
  line-height: 1.7;
  font-size: 0.95rem;
  color: #94a3b8;
  margin-bottom: 0.75rem;
}

.mt-3 { margin-top: 1.25rem; }
.mt-4 { margin-top: 1.5rem; }

.star-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.star-list li {
  margin-bottom: 0.5rem;
  color: #e2e8f0;
  font-weight: 500;
}
.star { color: #cbd5e1; margin-right: 0.5rem; }

.highlight-text {
  color: #ffffff;
  font-weight: 600;
  margin-top: 0.5rem;
  font-size: 0.95rem;
}

/* Search Box */
.search-box {
  margin-top: 2rem;
}
.search-label {
  font-size: 0.9rem;
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  font-weight: 500;
}
.search-input-group {
  display: flex;
  height: 42px;
  max-width: 300px;
}
.search-input {
  flex: 1;
  padding: 0 1rem;
  border: 1px solid #334155;
  background: #ffffff;
  color: #0f172a;
  border-radius: 4px 0 0 4px;
  outline: none;
  font-size: 0.95rem;
}
.search-btn {
  background: #1e3a8a;
  color: #ffffff;
  border: 1px solid #1e3a8a;
  padding: 0 1.25rem;
  font-weight: 600;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  transition: background 0.2s;
}
.search-btn:hover { background: #1d4ed8; }

/* Links Section */
.footer-links {
  list-style: none;
  padding: 0;
}
.footer-links li { margin-bottom: 1rem; }
.footer-links a {
  color: #cbd5e1;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.2s;
}
.footer-links a:hover { color: #38bdf8; }

/* Contact Section */
.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.contact-icon {
  width: 20px;
  height: 20px;
  color: #94a3b8;
  flex-shrink: 0;
  margin-top: 3px;
}
.contact-title {
  display: block;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}
.contact-details p {
  color: #94a3b8;
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
}

.contact-links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2rem;
}
.contact-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #cbd5e1;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s;
}
.contact-link:hover { color: #ffffff; }
.contact-icon-small { width: 16px; height: 16px; color: #94a3b8; }

/* WhatsApp Button */
.whatsapp-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #22c55e;
  color: #ffffff;
  text-decoration: none;
  padding: 0.6rem 1.25rem;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background 0.3s, transform 0.2s;
  box-shadow: 0 4px 6px -1px rgba(34, 197, 94, 0.2);
}
.whatsapp-btn:hover { background: #16a34a; transform: translateY(-1px); }

/* Footer Bottom */
.footer-bottom {
  position: relative;
  z-index: 1;
  text-align: center;
  color: #64748b;
  font-size: 0.9rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding-top: 1.5rem;
  max-width: 1280px;
  margin: 0 auto;
}

/* Responsiveness */
@media (max-width: 992px) {
  .footer-content { grid-template-columns: 1fr 1fr; }
  .about-section { grid-column: span 2; }
}
@media (max-width: 768px) {
  .footer-content { grid-template-columns: 1fr; gap: 2.5rem; }
  .about-section { grid-column: span 1; }
}
</style>
