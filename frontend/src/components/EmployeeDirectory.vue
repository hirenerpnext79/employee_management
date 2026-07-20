<template>
  <div class="employee-directory">
    <header class="directory-header">
      <h1>VCard</h1>
    </header>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading profile...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
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
                <div class="field-value">{{ selectedEmployee.first_name || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Middle Name</label>
                <div class="field-value">{{ selectedEmployee.middle_name || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Last Name</label>
                <div class="field-value">{{ selectedEmployee.last_name || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Full Name</label>
                <div class="field-value">{{ selectedEmployee.employee_name || '-' }}</div>
              </div>
              
              <div class="form-field">
                <label>Gender</label>
                <div class="field-value">{{ selectedEmployee.gender || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Date of Birth</label>
                <div class="field-value">{{ formatDate(selectedEmployee.date_of_birth) }}</div>
              </div>
              <div class="form-field">
                <label>Salutation</label>
                <div class="field-value">{{ selectedEmployee.salutation || '-' }}</div>
              </div>

              <div class="form-field">
                <label>Date of Joining</label>
                <div class="field-value">{{ formatDate(selectedEmployee.date_of_joining) }}</div>
              </div>
              <div class="form-field">
                <label>Status</label>
                <div class="field-value">{{ selectedEmployee.status || '-' }}</div>
              </div>
            </div>

            <!-- Company Details -->
            <div v-if="activeTab === 'Overview'" class="section-title">Company Details</div>
            <div v-if="activeTab === 'Overview'" class="form-grid">
              <div class="form-field">
                <label>Company</label>
                <div class="field-value">{{ selectedEmployee.company || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Designation</label>
                <div class="field-value">{{ selectedEmployee.designation || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Branch</label>
                <div class="field-value">{{ selectedEmployee.branch || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Department</label>
                <div class="field-value">{{ selectedEmployee.department || '-' }}</div>
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
                <div class="field-value">{{ formatDate(selectedEmployee.scheduled_confirmation_date) }}</div>
              </div>
              <div class="form-field">
                <label>Confirmation Date</label>
                <div class="field-value">{{ formatDate(selectedEmployee.final_confirmation_date) }}</div>
              </div>
              <div class="form-field">
                <label>Notice (days)</label>
                <div class="field-value">{{ selectedEmployee.notice_number_of_days || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Contract End Date</label>
                <div class="field-value">{{ formatDate(selectedEmployee.contract_end_date) }}</div>
              </div>
              <div class="form-field">
                <label>Date Of Retirement</label>
                <div class="field-value">{{ formatDate(selectedEmployee.date_of_retirement) }}</div>
              </div>
            </div>

            <!-- Address & Contacts Tab -->
            <div v-if="activeTab === 'Address & Contacts'" class="form-grid">
              <div class="form-field">
                <label>Mobile</label>
                <div class="field-value">{{ selectedEmployee.cell_number || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Personal Email</label>
                <div class="field-value">{{ selectedEmployee.personal_email || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Preferred Contact Email</label>
                <div class="field-value">{{ selectedEmployee.prefered_contact_email || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Company Email</label>
                <div class="field-value">{{ selectedEmployee.company_email || '-' }}</div>
                <div style="font-size: 12px; color: gray; margin-top: 4px;">Provide Email Address registered in company</div>
              </div>
              <div class="form-field">
                <label>Preferred Email</label>
                <div class="field-value">{{ selectedEmployee.prefered_email || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Unsubscribed</label>
                <div class="field-value">
                  <input type="checkbox" :checked="selectedEmployee.unsubscribed" disabled />
                </div>
              </div>
              
              <div class="section-title full-width" style="display: flex; align-items: center; gap: 8px;">
                Address 
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="18 15 12 9 6 15"></polyline>
                </svg>
              </div>
              
              <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div class="form-field">
                  <label>Current Address</label>
                  <div class="field-value">{{ selectedEmployee.current_address || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Current Address Is</label>
                  <div class="field-value">{{ selectedEmployee.current_accommodation_type || '-' }}</div>
                </div>
              </div>
              
              <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                <div class="form-field">
                  <label>Permanent Address</label>
                  <div class="field-value">{{ selectedEmployee.permanent_address || '-' }}</div>
                </div>
                <div class="form-field">
                  <label>Permanent Address Is</label>
                  <div class="field-value">{{ selectedEmployee.permanent_accommodation_type || '-' }}</div>
                </div>
              </div>

              <div class="section-title full-width">Emergency Contact</div>
              <div class="form-field">
                <label>Emergency Contact Name</label>
                <div class="field-value">{{ selectedEmployee.person_to_be_contacted || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Emergency Phone</label>
                <div class="field-value">{{ selectedEmployee.emergency_phone_number || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Relation</label>
                <div class="field-value">{{ selectedEmployee.relation || '-' }}</div>
              </div>
            </div>

            <!-- Attendance & Leaves Tab -->
            <div v-if="activeTab === 'Attendance & Leaves'" class="form-grid">
              <div class="form-field full-width">
                <label>Attendance Device ID (Biometric/RF tag ID)</label>
                <div class="field-value">{{ selectedEmployee.attendance_device_id || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Holiday List</label>
                <div class="field-value">{{ selectedEmployee.holiday_list || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Applicable Holiday List</label>
                <div class="field-value">{{ selectedEmployee.applicable_holiday_list || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Default Shift</label>
                <div class="field-value">{{ selectedEmployee.default_shift || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Leave Policy</label>
                <div class="field-value">{{ selectedEmployee.leave_policy || '-' }}</div>
              </div>
            </div>

            <!-- Salary Tab -->
            <div v-if="activeTab === 'Salary'" class="form-grid">
              <div class="form-field">
                <label>Cost to Company (CTC)</label>
                <div class="field-value">{{ selectedEmployee.ctc || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Salary Currency</label>
                <div class="field-value">{{ selectedEmployee.salary_currency || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Salary Mode</label>
                <div class="field-value">{{ selectedEmployee.salary_mode || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Bank Name</label>
                <div class="field-value">{{ selectedEmployee.bank_name || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Bank A/C No</label>
                <div class="field-value">{{ selectedEmployee.bank_ac_no || '-' }}</div>
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
                <label>Marital Status</label>
                <div class="field-value">{{ selectedEmployee.marital_status || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Blood Group</label>
                <div class="field-value">{{ selectedEmployee.blood_group || '-' }}</div>
              </div>
              <div class="form-field full-width">
                <label>Family Background</label>
                <div class="field-value" v-html="selectedEmployee.family_background || '-'"></div>
                <div style="font-size: 12px; color: gray; margin-top: 4px;">Here you can maintain family details like name and occupation of parent, spouse and children</div>
              </div>
              <div class="form-field full-width">
                <label>Health Details</label>
                <div class="field-value" v-html="selectedEmployee.health_details || '-'"></div>
                <div style="font-size: 12px; color: gray; margin-top: 4px;">Here you can maintain height, weight, allergies, medical concerns etc</div>
              </div>
              
              <div class="section-title full-width">Passport Details</div>
              <div class="form-field">
                <label>Passport Number</label>
                <div class="field-value">{{ selectedEmployee.passport_number || '-' }}</div>
              </div>
              <div class="form-field">
                <label>Date of Issue</label>
                <div class="field-value">{{ formatDate(selectedEmployee.date_of_issue) }}</div>
              </div>
              <div class="form-field">
                <label>Valid Upto</label>
                <div class="field-value">{{ formatDate(selectedEmployee.valid_upto) }}</div>
              </div>
              <div class="form-field">
                <label>Place of Issue</label>
                <div class="field-value">{{ selectedEmployee.place_of_issue || '-' }}</div>
              </div>
            </div>

            <!-- Employee Exit Tab -->
            <div v-if="activeTab === 'Employee Exit'" class="form-grid">
              <div class="form-field">
                <label>Resignation Letter Date</label>
                <div class="field-value">{{ formatDate(selectedEmployee.resignation_letter_date) }}</div>
              </div>
              <div class="form-field">
                <label>Relieving Date</label>
                <div class="field-value">{{ formatDate(selectedEmployee.relieving_date) }}</div>
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
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  token: {
    type: String,
    default: null
  }
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const parts = dateStr.split('-')
  if (parts.length === 3) {
    return `${parts[2]}-${parts[1]}-${parts[0]}`
  }
  return dateStr
}

const selectedEmployee = ref(null)
const loading = ref(true)
const error = ref(null)

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

const fetchEmployeeDetailsByToken = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`/api/method/employee_management.api.get_vcard_details?token=${props.token}`)
    if (!response.ok) {
      throw new Error('Employee not found')
    }
    const data = await response.json()
    selectedEmployee.value = data.message || null
    activeTab.value = 'Overview'
  } catch (e) {
    console.error("Failed to fetch employee details by token:", e)
    error.value = "This employee does not exist"
  } finally {
    loading.value = false
  }
}

watch(() => props.token, (newToken) => {
  if (newToken) {
    fetchEmployeeDetailsByToken()
  } else {
    error.value = "No token provided. Access denied."
    loading.value = false
  }
}, { immediate: true })
</script>
