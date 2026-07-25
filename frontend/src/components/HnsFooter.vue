<script setup>
import { ref, onMounted } from 'vue'
import { showError } from '../utils/toastHandler'

const footerMenuItems = ref([])
const left_side_content = ref('')
const right_side_content = ref('')
const footer_css = ref('')

onMounted(async () => {
  try {
    const response = await fetch('/api/method/web_pages.api.get_menu_tree?menu_type=Footer')
    const data = await response.json()
    if (data.message) {
      footerMenuItems.value = data.message.menu_items || []
      left_side_content.value = data.message.left_side_content || ''
      right_side_content.value = data.message.right_side_content || ''
      footer_css.value = data.message.css || ''
    }
  } catch (error) {
    console.error('Error fetching footer menu:', error)
    showError('Failed to load footer menu.')
  }
})
</script>

<template>
  <footer class="footer">
    <component is="style" v-if="footer_css">{{ footer_css }}</component>
    <div class="footer-overlay"></div>
    <div class="footer-content">
      
      <!-- About HNS Column -->
      <div class="footer-section about-section" v-if="left_side_content" v-html="left_side_content">
      </div>

      <!-- Quick Links Column -->
      <div class="footer-section links-section" v-if="footerMenuItems.length > 0">
        <h3>Quick Links</h3>
        <ul class="footer-links">
          <li v-for="item in footerMenuItems" :key="item.label">
            <a :href="item.page_url">{{ item.label }}</a>
          </li>
        </ul>
      </div>

      <!-- Contact Column -->
      <div class="footer-section contact-section" v-if="right_side_content" v-html="right_side_content">
      </div>
      
    </div>
    
    <div class="footer-bottom">
      &copy; {{ new Date().getFullYear() }} HNS India. All rights reserved.
    </div>
  </footer>
</template>

