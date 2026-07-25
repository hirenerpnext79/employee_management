<template>
  <HnsCustomPage pageName="About Us">
    <template #after-sections>
      <!-- Static Premium Sections -->
      <AboutTestimonials />
      <AboutSolutions />
      <AboutFacts />
      <AboutIndustries />
    </template>
  </HnsCustomPage>
</template>

<script setup>
import HnsCustomPage from './HnsCustomPage.vue'
import AboutTestimonials from './about_sections/AboutTestimonials.vue'
import AboutSolutions from './about_sections/AboutSolutions.vue'
import AboutFacts from './about_sections/AboutFacts.vue'
import AboutIndustries from './about_sections/AboutIndustries.vue'
</script>

<style scoped>
/* Page-specific styles for About Us can go here, if any */
</style>
