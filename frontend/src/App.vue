<script setup>
import { ref } from 'vue'
import EmployeeDirectory from './components/EmployeeDirectory.vue'

const urlParams = new URLSearchParams(window.location.search)
let t = urlParams.get('token')
if (!t) {
  const match = window.location.pathname.match(/\/token=([a-f0-9]+)/)
  if (match) {
    t = match[1]
  }
}
const token = ref(t)
</script>

<template>
  <EmployeeDirectory :token="token" />
</template>
