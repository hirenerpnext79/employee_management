<template>
  <div class="employee-directory">
    <header class="directory-header">
      <h1>Employee Directory</h1>
      <div class="header-actions">
        <button v-if="selectedEmployee" @click="clearSelection" class="back-button">
          &larr; Back to List
        </button>
        <button v-if="!needsLogin" @click="handleLogout" class="logout-button">
          Logout
        </button>
      </div>
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
          
          <div class="detail-tabs-container">
            <div class="tabs">
              <button 
                v-for="tab in tabs" 
                :key="tab" 
                :class="['tab-button', { active: activeTab === tab }]"
                @click="activeTab = tab"
              >
                {{ tab }}
              </button>
            </div>

            <div class="tab-content">
              <!-- Overview Tab -->
              <div v-if="activeTab === 'Overview'" class="form-grid">
                <div class="form-field">
                  <label>First Name</label>
                  <div class="field-value">{{ selectedEmployee.first_name || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Middle Name</label>
                  <div class="field-value">{{ selectedEmployee.middle_name || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Last Name</label>
                  <div class="field-value">{{ selectedEmployee.last_name || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Full Name</label>
                  <div class="field-value">{{ selectedEmployee.employee_name || 'N/A' }}</div>
                </div>
                
                <div class="form-field">
                  <label>Gender</label>
                  <div class="field-value">{{ selectedEmployee.gender || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Date of Birth</label>
                  <div class="field-value">{{ selectedEmployee.date_of_birth || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Salutation</label>
                  <div class="field-value">{{ selectedEmployee.salutation || '-' }}</div>
                </div>

                <div class="form-field">
                  <label>Date of Joining</label>
                  <div class="field-value">{{ selectedEmployee.date_of_joining || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Status</label>
                  <div class="field-value">{{ selectedEmployee.status || 'N/A' }}</div>
                </div>
              </div>

              <!-- Company Details (can go in Overview or a separate section) -->
              <div v-if="activeTab === 'Overview'" class="section-title">Company Details</div>
              <div v-if="activeTab === 'Overview'" class="form-grid">
                <div class="form-field">
                  <label>Company</label>
                  <div class="field-value">{{ selectedEmployee.company || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Designation</label>
                  <div class="field-value">{{ selectedEmployee.designation || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Branch</label>
                  <div class="field-value">{{ selectedEmployee.branch || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Department</label>
                  <div class="field-value">{{ selectedEmployee.department || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Reports To</label>
                  <div class="field-value">{{ selectedEmployee.reports_to || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Employee Number</label>
                  <div class="field-value">{{ selectedEmployee.employee_number || '-' }}</div>
                </div>
              </div>

              <!-- Joining Tab -->
              <div v-if="activeTab === 'Joining'" class="form-grid">
                <div class="form-field">
                  <label>Offer Date</label>
                  <div class="field-value">{{ selectedEmployee.offer_date || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Confirmation Date</label>
                  <div class="field-value">{{ selectedEmployee.confirmation_date || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Contract End Date</label>
                  <div class="field-value">{{ selectedEmployee.contract_end_date || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Notice (Days)</label>
                  <div class="field-value">{{ selectedEmployee.notice_number_of_days || '0' }}</div>
                </div>
                <div class="form-field">
                  <label>Date of Retirement</label>
                  <div class="field-value">{{ selectedEmployee.date_of_retirement || 'N/A' }}</div>
                </div>
              </div>

              <!-- Address & Contacts Tab -->
              <div v-if="activeTab === 'Address & Contacts'" class="form-grid">
                <div class="form-field full-width">
                  <label>Current Address</label>
                  <div class="field-value">{{ selectedEmployee.current_address || 'N/A' }}</div>
                </div>
                <div class="form-field full-width">
                  <label>Permanent Address</label>
                  <div class="field-value">{{ selectedEmployee.permanent_address || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Personal Email</label>
                  <div class="field-value">{{ selectedEmployee.personal_email || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Company Email</label>
                  <div class="field-value">{{ selectedEmployee.company_email || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Cell Number</label>
                  <div class="field-value">{{ selectedEmployee.cell_number || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Emergency Phone Number</label>
                  <div class="field-value">{{ selectedEmployee.emergency_phone_number || '-' }}</div>
                </div>
              </div>

              <!-- Attendance & Leaves Tab -->
              <div v-if="activeTab === 'Attendance & Leaves'" class="form-grid">
                <div class="form-field">
                  <label>Holiday List</label>
                  <div class="field-value">{{ selectedEmployee.holiday_list || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Default Shift</label>
                  <div class="field-value">{{ selectedEmployee.default_shift || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Leave Policy</label>
                  <div class="field-value">{{ selectedEmployee.leave_policy || 'N/A' }}</div>
                </div>
              </div>

              <!-- Salary Tab -->
              <div v-if="activeTab === 'Salary'" class="form-grid">
                <div class="form-field">
                  <label>Salary Mode</label>
                  <div class="field-value">{{ selectedEmployee.salary_mode || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Bank Name</label>
                  <div class="field-value">{{ selectedEmployee.bank_name || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Bank A/C No</label>
                  <div class="field-value">{{ selectedEmployee.bank_ac_no || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Payroll Cost Center</label>
                  <div class="field-value">{{ selectedEmployee.payroll_cost_center || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>PAN Number</label>
                  <div class="field-value">{{ selectedEmployee.pan_number || '-' }}</div>
                </div>
              </div>

              <!-- Personal Details Tab -->
              <div v-if="activeTab === 'Personal Details'" class="form-grid">
                <div class="form-field">
                  <label>Blood Group</label>
                  <div class="field-value">{{ selectedEmployee.blood_group || 'N/A' }}</div>
                </div>
                <div class="form-field">
                  <label>Marital Status</label>
                  <div class="field-value">{{ selectedEmployee.marital_status || 'N/A' }}</div>
                </div>
                <div class="form-field full-width">
                  <label>Family Background</label>
                  <div class="field-value" v-html="selectedEmployee.family_background || 'N/A'"></div>
                </div>
              </div>

              <!-- Employee Exit Tab -->
              <div v-if="activeTab === 'Employee Exit'" class="form-grid">
                <div class="form-field">
                  <label>Resignation Letter Date</label>
                  <div class="field-value">{{ selectedEmployee.resignation_letter_date || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Relieving Date</label>
                  <div class="field-value">{{ selectedEmployee.relieving_date || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Reason for Leaving</label>
                  <div class="field-value">{{ selectedEmployee.reason_for_leaving || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Leave Encashed</label>
                  <div class="field-value">{{ selectedEmployee.leave_encashed || '-' }}</div>
                </div>
              </div>

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

const activeTab = ref('Overview')
const tabs = [
  'Overview', 
  'Joining', 
  'Address & Contacts', 
  'Attendance & Leaves', 
  'Salary', 
  'Personal Details', 
  'Employee Exit'
]

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
    activeTab.value = 'Overview' // Reset to overview on new selection
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

const handleLogout = async () => {
  needsLogin.value = true
  employees.value = []
  selectedEmployee.value = null
  try {
    await fetch('/api/method/logout', { method: 'POST' })
  } catch (e) {
    console.error("Logout failed:", e)
  }
}

const clearSelection = () => {
  selectedEmployee.value = null
}

onMounted(() => {
  fetchEmployees()
})
</script>
