<template>
  <div class="new-consultation-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">New Consultation</h1>
        <p class="page-subtitle">Record a new patient consultation note</p>
      </div>
      <router-link to="/" class="btn btn-outline">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>
        </svg>
        Back to List
      </router-link>
    </div>

    <div class="card">
      <div class="card-body">
        <form @submit.prevent="submitForm" class="consultation-form" novalidate>

          <!-- Section 1: Patient Information -->
          <div class="form-section">
            <div class="form-section-header">
              <div class="form-section-icon icon-patient">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div>
                <div class="form-section-title">Patient Information</div>
                <div class="form-section-subtitle">Enter the patient's details</div>
              </div>
            </div>

            <div class="form-group">
              <label for="patientName" class="form-label required">Patient Full Name</label>
              <input
                id="patientName"
                v-model="form.patientName"
                type="text"
                class="form-control"
                :class="{ error: errors.patientName }"
                placeholder="e.g. Karim"
                autocomplete="off"
                @blur="validateField('patientName')"
              />
              <p v-if="errors.patientName" class="form-error">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 13px; height: 13px; flex-shrink: 0;">
                  <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                {{ errors.patientName }}
              </p>
            </div>
          </div>

          <!-- Section 2: Diagnosis Selection -->
          <div class="form-section">
            <div class="form-section-header">
              <div class="form-section-icon icon-diagnosis">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>
                  <rect x="9" y="3" width="6" height="4" rx="1"/>
                  <path d="m9 14 2 2 4-4"/>
                </svg>
              </div>
              <div>
                <div class="form-section-title">Diagnosis Codes</div>
                <div class="form-section-subtitle">Search and select ICD-10 diagnosis codes</div>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label required">ICD-10 Code Search</label>
              <div class="diagnosis-search dropdown">
                <div class="search-input-wrapper">
                  <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                  </svg>
                  <input
                    v-model="diagnosisSearch"
                    type="text"
                    class="form-control search-input"
                    :class="{ error: errors.diagnosisCodes }"
                    placeholder="Search by code or description (e.g. E11.9 or diabetes)"
                    autocomplete="off"
                    @input="searchDiagnosis"
                    @focus="showDropdown = true"
                    role="combobox"
                    :aria-expanded="showDropdown && (diagnosisResults.length > 0 || (diagnosisSearch && !searchLoading))"
                    aria-haspopup="listbox"
                  />
                  <div v-if="searchLoading" class="search-spinner">
                    <div class="spinner"></div>
                  </div>
                </div>

                <!-- Dropdown Results -->
                <div
                  v-if="showDropdown && diagnosisResults.length > 0"
                  class="dropdown-menu"
                  role="listbox"
                >
                  <div
                    v-for="diagnosis in diagnosisResults"
                    :key="diagnosis.id"
                    class="dropdown-item"
                    role="option"
                    @click="selectDiagnosis(diagnosis)"
                  >
                    <span class="dropdown-item-code">{{ diagnosis.code }}</span>
                    <span class="dropdown-item-description">{{ diagnosis.description }}</span>
                  </div>
                </div>

                <!-- No Results -->
                <div
                  v-if="showDropdown && diagnosisSearch && !searchLoading && diagnosisResults.length === 0"
                  class="dropdown-menu"
                >
                  <div class="dropdown-item no-results">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px; opacity: 0.4;">
                      <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    No codes matching "{{ diagnosisSearch }}"
                  </div>
                </div>
              </div>

              <!-- Selected Diagnoses -->
              <div v-if="form.diagnosisCodes.length > 0" class="selected-diagnoses">
                <div
                  v-for="code in form.diagnosisCodes"
                  :key="code"
                  class="selected-chip"
                >
                  <span class="selected-chip-code">{{ code }}</span>
                  <button
                    type="button"
                    class="chip-remove"
                    @click="removeDiagnosis(code)"
                    :title="`Remove ${code}`"
                    :aria-label="`Remove diagnosis ${code}`"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 12px; height: 12px;">
                      <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                  </button>
                </div>
              </div>

              <p v-if="errors.diagnosisCodes" class="form-error">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 13px; height: 13px; flex-shrink: 0;">
                  <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                {{ errors.diagnosisCodes }}
              </p>
            </div>
          </div>

          <!-- Section 3: Consultation Notes -->
          <div class="form-section">
            <div class="form-section-header">
              <div class="form-section-icon icon-notes">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14 2 14 8 20 8"/>
                  <line x1="16" y1="13" x2="8" y2="13"/>
                  <line x1="16" y1="17" x2="8" y2="17"/>
                </svg>
              </div>
              <div>
                <div class="form-section-title">Treatment Notes</div>
                <div class="form-section-subtitle">Document the treatment plan and recommendations</div>
              </div>
            </div>

            <div class="form-group">
              <label for="treatmentNotes" class="form-label required">Notes</label>
              <textarea
                id="treatmentNotes"
                v-model="form.treatmentNotes"
                class="form-control"
                :class="{ error: errors.treatmentNotes }"
                placeholder="Enter treatment plan, prescriptions, follow-up recommendations…"
                rows="6"
                @blur="validateField('treatmentNotes')"
              ></textarea>
              <div class="form-control-footer">
                <p v-if="errors.treatmentNotes" class="form-error">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 13px; height: 13px; flex-shrink: 0;">
                    <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  {{ errors.treatmentNotes }}
                </p>
                <span v-else class="char-count" :class="{ 'char-count-warn': form.treatmentNotes.length > 900 }">
                  {{ form.treatmentNotes.length }} characters
                </span>
              </div>
            </div>
          </div>

          <!-- Section 4: Date (optional) -->
          <div class="form-section form-section-last">
            <div class="form-section-header">
              <div class="form-section-icon icon-calendar">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
              </div>
              <div>
                <div class="form-section-title">Consultation Date</div>
                <div class="form-section-subtitle">Defaults to current date and time if left empty</div>
              </div>
            </div>

            <div class="form-group" style="margin-bottom: 0;">
              <label for="consultationDate" class="form-label">Date &amp; Time</label>
              <input
                id="consultationDate"
                v-model="form.consultationDate"
                type="datetime-local"
                class="form-control"
                style="max-width: 280px;"
              />
            </div>
          </div>

          <!-- Form Actions -->
          <div class="form-actions">
            <router-link to="/" class="btn btn-outline">
              Cancel
            </router-link>
            <button type="submit" class="btn btn-primary btn-lg" :disabled="submitting">
              <span v-if="submitting" class="spinner"></span>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
                <polyline points="17 21 17 13 7 13 7 21"/>
                <polyline points="7 3 7 8 15 8"/>
              </svg>
              {{ submitting ? 'Saving…' : 'Save Consultation' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { searchDiagnosisCodes, createConsultation } from '../services/api'

const router = useRouter()
const showToast = inject('showToast')

// Form state
const form = reactive({
  patientName: '',
  diagnosisCodes: [],
  treatmentNotes: '',
  consultationDate: ''
})

// Validation state
const errors = reactive({
  patientName: '',
  diagnosisCodes: '',
  treatmentNotes: ''
})

// UI state
const diagnosisSearch = ref('')
const diagnosisResults = ref([])
const showDropdown = ref(false)
const searchLoading = ref(false)
const submitting = ref(false)

let searchTimeout = null

// Search diagnosis codes with debounce
const searchDiagnosis = () => {
  clearTimeout(searchTimeout)

  if (!diagnosisSearch.value.trim()) {
    diagnosisResults.value = []
    return
  }

  searchLoading.value = true

  searchTimeout = setTimeout(async () => {
    try {
      const results = await searchDiagnosisCodes(diagnosisSearch.value)
      diagnosisResults.value = results.filter(
        d => !form.diagnosisCodes.includes(d.code)
      )
    } catch (err) {
      console.error('Search error:', err)
      diagnosisResults.value = []
    } finally {
      searchLoading.value = false
    }
  }, 300)
}

// Select a diagnosis code
const selectDiagnosis = (diagnosis) => {
  if (!form.diagnosisCodes.includes(diagnosis.code)) {
    form.diagnosisCodes.push(diagnosis.code)
  }
  diagnosisSearch.value = ''
  diagnosisResults.value = []
  showDropdown.value = false
  errors.diagnosisCodes = ''
}

// Remove a diagnosis code
const removeDiagnosis = (code) => {
  form.diagnosisCodes = form.diagnosisCodes.filter(c => c !== code)
}

// Validate individual field
const validateField = (field) => {
  switch (field) {
    case 'patientName':
      if (!form.patientName.trim()) {
        errors.patientName = 'Patient name is required'
      } else if (form.patientName.trim().length < 2) {
        errors.patientName = 'Name must be at least 2 characters'
      } else {
        errors.patientName = ''
      }
      break
    case 'treatmentNotes':
      if (!form.treatmentNotes.trim()) {
        errors.treatmentNotes = 'Treatment notes are required'
      } else if (form.treatmentNotes.trim().length < 10) {
        errors.treatmentNotes = 'Notes must be at least 10 characters'
      } else {
        errors.treatmentNotes = ''
      }
      break
    case 'diagnosisCodes':
      if (form.diagnosisCodes.length === 0) {
        errors.diagnosisCodes = 'At least one diagnosis code is required'
      } else {
        errors.diagnosisCodes = ''
      }
      break
  }
}

// Validate entire form
const validateForm = () => {
  validateField('patientName')
  validateField('treatmentNotes')
  validateField('diagnosisCodes')
  return !errors.patientName && !errors.treatmentNotes && !errors.diagnosisCodes
}

// Submit the form
const submitForm = async () => {
  if (!validateForm()) return

  submitting.value = true

  try {
    const consultationData = {
      patient_name: form.patientName.trim(),
      diagnosis_codes: form.diagnosisCodes,
      treatment_notes: form.treatmentNotes.trim()
    }

    if (form.consultationDate) {
      consultationData.consultation_date = new Date(form.consultationDate).toISOString()
    }

    await createConsultation(consultationData)
    showToast?.('Consultation saved successfully', 'success')

    setTimeout(() => {
      router.push('/')
    }, 800)
  } catch (err) {
    showToast?.(err.response?.data?.detail || 'Failed to save consultation. Please try again.', 'error')
  } finally {
    submitting.value = false
  }
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  const dropdown = document.querySelector('.diagnosis-search')
  if (dropdown && !dropdown.contains(event.target)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  clearTimeout(searchTimeout)
})
</script>

<style scoped>
.new-consultation-page {
  max-width: 680px;
  margin: 0 auto;
}

.consultation-form {
  display: flex;
  flex-direction: column;
}

/* --- Search Input --- */
.search-input-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  padding-left: 36px;
}

.search-spinner {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
}

/* --- Selected Diagnoses --- */
.selected-diagnoses {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
  padding: 12px;
  background-color: var(--gray-50);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
}

.selected-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 8px 5px 12px;
  background-color: var(--primary-color);
  color: var(--text-inverse);
  border-radius: var(--radius-full);
  font-size: 0.8125rem;
  font-weight: 500;
  transition: background-color var(--transition-fast);
}

.selected-chip-code {
  font-family: 'SF Mono', 'Fira Code', Menlo, Consolas, monospace;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.selected-chip .chip-remove {
  color: rgba(255, 255, 255, 0.7);
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.selected-chip .chip-remove:hover {
  color: white;
  background-color: rgba(255, 255, 255, 0.2);
}

/* --- No Results --- */
.no-results {
  color: var(--text-muted);
  font-style: normal;
  cursor: default;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8125rem;
}

.no-results:hover {
  background-color: transparent !important;
}

/* --- Character Count --- */
.form-control-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-top: 4px;
  min-height: 20px;
}

.char-count {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-left: auto;
}

.char-count-warn {
  color: var(--warning-color);
}

/* --- Form Section Last (no bottom border) --- */
.form-section-last {
  margin-bottom: 0;
}

/* --- Form Actions --- */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-light);
}

/* --- Responsive --- */
@media (max-width: 768px) {
  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>