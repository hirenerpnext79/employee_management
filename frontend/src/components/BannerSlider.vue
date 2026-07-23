<template>
  <!-- Premium Slider Section -->
  <div class="slider-container" v-if="!loading && activeSlider && activeSlider.images && activeSlider.images.length">
    <div 
      class="slide" 
      v-for="(img, index) in activeSlider.images" 
      :key="index"
      :class="{ active: currentSlide === index }"
    >
      <img :src="img.image" :alt="img.title" class="slide-image" />
      <div class="slide-overlay">
        <h2 class="slide-title" v-if="img.title">{{ img.title }}</h2>
      </div>
    </div>
    
    <!-- Controls -->
    <button class="slider-btn prev" @click="prevSlide" v-if="activeSlider.images.length > 1">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
    </button>
    <button class="slider-btn next" @click="nextSlide" v-if="activeSlider.images.length > 1">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
    </button>
    
    <!-- Dots -->
    <div class="slider-dots" v-if="activeSlider.images.length > 1">
      <span 
        v-for="(_, index) in activeSlider.images" 
        :key="'dot-'+index"
        class="dot" 
        :class="{ active: currentSlide === index }"
        @click="setSlide(index)"
      ></span>
    </div>
  </div>
  
  <!-- Fallback if no slider is active -->
  <div class="home-hero" v-else>
    <h1>Welcome to Employee Management</h1>
    <p>Your complete solution for managing employee profiles and digital VCards.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const activeSlider = ref(null)
const loading = ref(true)
const currentSlide = ref(0)
let sliderInterval = null

const fetchSlider = async () => {
  try {
    const res = await fetch('/api/method/web_pages.api.get_active_slider')
    const data = await res.json()
    if (data.message) {
      activeSlider.value = data.message
    }
  } catch (e) {
    console.error('Failed to fetch slider', e)
  } finally {
    loading.value = false
  }
}

const nextSlide = () => {
  if (!activeSlider.value || !activeSlider.value.images) return
  currentSlide.value = (currentSlide.value + 1) % activeSlider.value.images.length
}

const prevSlide = () => {
  if (!activeSlider.value || !activeSlider.value.images) return
  currentSlide.value = (currentSlide.value - 1 + activeSlider.value.images.length) % activeSlider.value.images.length
}

const setSlide = (index) => {
  currentSlide.value = index
}

onMounted(() => {
  fetchSlider()
  // Auto-advance slide every 6 seconds
  sliderInterval = setInterval(nextSlide, 6000)
})

onUnmounted(() => {
  if (sliderInterval) clearInterval(sliderInterval)
})
</script>

<style scoped>
.slider-container {
  position: relative;
  /* Slightly reduced width to avoid scrollbar gap issues */
  width: calc(100vw - 16px);
  margin-left: calc(-50vw + 8px + 50%);
  /* Adjusted height to look more like a standard banner (not strictly 100vh) */
  height: 65vh;
  min-height: 500px;
  max-height: 700px;
  overflow: hidden;
  background: #000;
  /* Push up to eliminate gap with header */
  margin-top: -80px;
  padding-top: 80px;
}

.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 1.2s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.slide.active {
  opacity: 1;
  z-index: 2;
}

.slide-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.05);
  transition: transform 7s ease-out;
}

.slide.active .slide-image {
  transform: scale(1);
}

.slide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.1) 40%, rgba(0,0,0,0.4) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
}

.slide-title {
  color: white;
  font-size: 4.5rem;
  font-weight: 800;
  letter-spacing: -1.5px;
  line-height: 1.1;
  text-shadow: 0 4px 24px rgba(0,0,0,0.8);
  margin: 0;
  transform: translateY(40px);
  opacity: 0;
  transition: all 1s cubic-bezier(0.4, 0, 0.2, 1) 0.4s;
  max-width: 1100px;
}

.slide.active .slide-title {
  transform: translateY(0);
  opacity: 1;
}

.slider-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.25);
  color: white;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 3;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
}

.slider-container:hover .slider-btn {
  opacity: 1;
}

.slider-btn:hover {
  background: rgba(255,255,255,0.3);
  border-color: rgba(255,255,255,0.5);
  transform: translateY(-50%) scale(1.1);
}

.slider-btn.prev {
  left: 3rem;
}

.slider-btn.next {
  right: 3rem;
}

.slider-dots {
  position: absolute;
  bottom: 3rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 1rem;
  z-index: 3;
}

.dot {
  width: 12px;
  height: 12px;
  background: rgba(255,255,255,0.3);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.dot:hover {
  background: rgba(255,255,255,0.8);
}

.dot.active {
  background: white;
  width: 48px;
  border-radius: 6px;
  border-color: rgba(0,0,0,0.2);
}

/* Fallback styling */
.home-hero {
  background: #f8fafc;
  padding: 12rem 2rem;
  text-align: center;
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-top: -80px;
}

.home-hero h1 {
  font-size: 3.5rem;
  color: #0f172a;
  margin-bottom: 1.5rem;
  font-weight: 800;
  letter-spacing: -1px;
}

.home-hero p {
  font-size: 1.25rem;
  color: #475569;
  max-width: 600px;
}

@media (max-width: 768px) {
  .slider-container {
    height: 70vh;
    min-height: 450px;
  }
  .slide-title {
    font-size: 2.75rem;
  }
  .slider-btn {
    width: 48px;
    height: 48px;
    opacity: 1; /* Always visible on mobile */
  }
  .slider-btn.prev {
    left: 1rem;
  }
  .slider-btn.next {
    right: 1rem;
  }
}
</style>
