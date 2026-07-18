<template>
  <div class="employee-directory">
    <header class="directory-header">
      <h1>Employee Directory</h1>
      <button v-if="selectedEmployee" @click="clearSelection" class="back-button">
        &larr; Back to List
      </button>
    </header>

    <!-- Login Form -->
    <div v-if="needsLogin" class="login-container">
      <div class="login-card">
        <h2>Please Log In</h2>
        <p>You need to authenticate to view the Employee Directory.</p>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="loginForm.usr" required />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="loginForm.pwd" required />
          </div>
          <button type="submit" class="login-button" :disabled="loading">
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
          <p v-if="loginError" class="error-text">{{ loginError }}</p>
        </form>
      </div>
    </div>

    <!-- Main Content -->
    <template v-else>
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading employee data...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchEmployees" class="retry-button">Retry</button>
      </div>

      <!-- Detail View -->
      <div v-else-if="selectedEmployee" class="employee-detail">
        <div class="detail-card">
          <div class="detail-header">
            <img 
              :src="selectedEmployee.image || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(selectedEmployee.employee_name || 'Employee')" 
              :alt="selectedEmployee.employee_name" 
              class="detail-avatar" 
            />
            <div class="detail-title">
              <h2>{{ selectedEmployee.employee_name }}</h2>
              <p class="designation">{{ selectedEmployee.designation }}</p>
              <p class="department">{{ selectedEmployee.department }}</p>
            </div>
          </div>
          
          <div class="detail-body">
            <div class="detail-section">
              <h3>Contact Information</h3>
              <p><strong>Email:</strong> {{ selectedEmployee.company_email || selectedEmployee.personal_email || 'N/A' }}</p>
              <p><strong>Phone:</strong> {{ selectedEmployee.cell_number || 'N/A' }}</p>
            </div>
            
            <div class="detail-section">
              <h3>Employment Details</h3>
              <p><strong>Employee ID:</strong> {{ selectedEmployee.name }}</p>
              <p><strong>Status:</strong> <span :class="'status-badge ' + (selectedEmployee.status || '').toLowerCase()">{{ selectedEmployee.status }}</span></p>
              <p><strong>Date of Joining:</strong> {{ selectedEmployee.date_of_joining || 'N/A' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="employee-grid">
        <div 
          v-for="employee in employees" 
          :key="employee.name" 
          class="employee-card"
          @click="fetchEmployeeDetails(employee.name)"
        >
          <div class="card-avatar">
            <img 
              :src="employee.image || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(employee.employee_name || 'Employee')" 
              :alt="employee.employee_name" 
            />
          </div>
          <div class="card-info">
            <h3>{{ employee.employee_name }}</h3>
            <p class="designation">{{ employee.designation || 'No Designation' }}</p>
            <p class="department">{{ employee.department || 'No Department' }}</p>
          </div>
        </div>
        <div v-if="employees.length === 0" class="empty-state">
          <p>No employees found.</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const employees = ref([])
const selectedEmployee = ref(null)
const loading = ref(true)
const error = ref(null)

const needsLogin = ref(false)
const loginError = ref(null)
const loginForm = ref({ usr: '', pwd: '' })

const fetchEmployees = async () => {
  loading.value = true
  error.value = null
  needsLogin.value = false
  
  try {
    const response = await fetch('/api/resource/Employee?fields=["name","employee_name","designation","department","image","status"]')
    
    if (response.status === 401 || response.status === 403) {
      needsLogin.value = true
      loading.value = false
      return
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    employees.value = data.data || []
  } catch (e) {
    console.error("Failed to fetch employees:", e)
    error.value = "Failed to load employee directory."
  } finally {
    loading.value = false
  }
}

const fetchEmployeeDetails = async (employeeId) => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/resource/Employee/${employeeId}`)
    
    if (response.status === 401 || response.status === 403) {
      needsLogin.value = true
      return
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    selectedEmployee.value = data.data || null
  } catch (e) {
    console.error("Failed to fetch employee details:", e)
    error.value = "Failed to load employee details."
  } finally {
    loading.value = false
  }
}

const handleLogin = async () => {
  loading.value = true
  loginError.value = null
  
  try {
    const response = await fetch('/api/method/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(loginForm.value)
    })
    
    const data = await response.json()
    
    if (data.message === "Logged In") {
      needsLogin.value = false
      fetchEmployees()
    } else {
      loginError.value = "Invalid credentials."
    }
  } catch (e) {
    console.error("Login failed:", e)
    loginError.value = "An error occurred while logging in."
  } finally {
    loading.value = false
  }
}

const clearSelection = () => {
  selectedEmployee.value = null
}

onMounted(() => {
  fetchEmployees()
})
</script>
