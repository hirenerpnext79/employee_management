<template>
  <div class="about-testimonials">
    <div class="section-header">
      <h2>ABOUT US AND CLIENTS TESTIMONIALS</h2>
    </div>
    
    <div class="video-grid">
      <!-- Video 1 -->
      <div class="video-wrapper">
        <iframe 
          src="https://www.youtube.com/embed/iU87Yi7gWLo" 
          title="HNS Company Profile with Team" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen>
        </iframe>
      </div>
      
      <!-- Video 2 -->
      <div class="video-wrapper">
        <iframe 
          src="https://www.youtube.com/embed/ScMzIvxBSi4" 
          title="Clients Speak about Hard n Soft Consultancy" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen>
        </iframe>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-testimonials {
  margin: 4rem 0;
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

.video-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 768px) {
  .video-grid {
    grid-template-columns: 1fr 1fr;
  }
}

.video-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-color: #000;
}

.video-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}
</style>
