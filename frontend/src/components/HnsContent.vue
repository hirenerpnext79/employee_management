<template>
  <main class="main-content">
    <section class="hero">
      <div class="hero-text">
        <h1>Empowering Businesses with Custom ERP Solutions</h1>
        <p>Providing Business Solutions since 1987. We offer SAP B1, Zoho Software & Creator based Customised Solutions tailored to your growth.</p>
        <button class="cta-button">Discover Solutions</button>
      </div>
    </section>
    
    <section class="details">
      <h2>Our Expertise</h2>
      <div class="cards-container">
        <div class="card">
          <div class="card-icon">🏢</div>
          <h3>SAP B1 Solutions</h3>
          <p>Comprehensive SAP Business One solutions tailored for manufacturing, textiles, and enterprise management.</p>
        </div>
        <div class="card">
          <div class="card-icon">☁️</div>
          <h3>Zoho Creator</h3>
          <p>Agile and highly customized cloud-based workflows built seamlessly on the Zoho infrastructure.</p>
        </div>
        <div class="card">
          <div class="card-icon">📈</div>
          <h3>ERPNext</h3>
          <p>Robust, open-source ERP implementations designed to intuitively scale alongside your business.</p>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.main-content {
  min-height: 80vh;
  font-family: 'Inter', sans-serif;
  background-color: #0f172a;
  color: #f8fafc;
}

.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 100px 5%;
  background: radial-gradient(circle at top, rgba(59, 130, 246, 0.15), transparent 60%);
}

.hero-text {
  max-width: 800px;
}

.hero h1 {
  font-size: 3.5rem;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.hero p {
  font-size: 1.2rem;
  color: #94a3b8;
  margin-bottom: 2rem;
}

.cta-button {
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
}

.details {
  padding: 50px 5%;
  text-align: center;
}

.details h2 {
  font-size: 2.5rem;
  margin-bottom: 3rem;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.card {
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 16px;
  backdrop-filter: blur(5px);
  transition: transform 0.3s, border-color 0.3s;
  text-align: left;
}

.card:hover {
  transform: translateY(-5px);
  border-color: #3b82f6;
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.card p {
  color: #94a3b8;
}

@media (max-width: 768px) {
  .hero h1 { font-size: 2.5rem; }
}
</style>
