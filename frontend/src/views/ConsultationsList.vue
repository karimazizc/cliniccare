<template>
  <div class="consultations-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Consultations</h1>
        <p class="page-subtitle">Patient consultation records</p>
      </div>
      <router-link to="/new" class="btn btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        New Consultation
      </router-link>
    </div>

    <!-- Loading Skeleton State -->
    <div v-if="loading" class="card">
      <div class="card-header">
        <div class="skeleton skeleton-line" style="width: 160px; height: 12px;"></div>
      </div>
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th style="width: 40px;"></th>
              <th>Patient</th>
              <th>Diagnosis</th>
              <th>Date</th>
              <th>Notes</th>
              <th style="width: 80px;"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="n in 5" :key="n">
              <td><div class="skeleton" style="width: 14px; height: 14px; border-radius: 3px;"></div></td>
              <td><div class="skeleton skeleton-line" style="width: 120px;"></div></td>
              <td>
                <div style="display: flex; gap: 6px;">
                  <div class="skeleton skeleton-chip"></div>
                  <div class="skeleton skeleton-chip" style="width: 50px;"></div>
                </div>
              </td>
              <td><div class="skeleton skeleton-line" style="width: 90px;"></div></td>
              <td><div class="skeleton skeleton-line" style="width: 140px;"></div></td>
              <td><div class="skeleton" style="width: 50px; height: 26px; border-radius: 6px;"></div></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-error">
      <svg class="alert-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
      </svg>
      <div>
        <strong>Unable to load consultations.</strong> {{ error }}
        <button @click="fetchConsultations" class="btn btn-sm btn-outline" style="margin-left: 0.75rem; vertical-align: baseline;">
          Retry
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="consultations.length === 0" class="card empty-state">
      <div class="empty-state-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
          <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
          <line x1="9" y1="12" x2="15" y2="12"/>
        </svg>
      </div>
      <h3 class="empty-state-title">No consultations recorded</h3>
      <p class="empty-state-description">Get started by creating your first patient consultation note.</p>
      <router-link to="/new" class="btn btn-primary">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        Create First Consultation
      </router-link>
    </div>

    <!-- Consultations Table -->
    <div v-else class="card">
      <div class="card-header">
        <span class="table-info">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px; opacity: 0.5;">
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
            <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
          </svg>
          {{ total }} consultation{{ total !== 1 ? 's' : '' }}
        </span>
      </div>
      <div class="table-container">
        <table class="table" role="table">
          <thead>
            <tr>
              <th style="width: 36px;"></th>
              <th>Patient</th>
              <th>Diagnosis Codes</th>
              <th>Date</th>
              <th>Notes Preview</th>
              <th style="width: 80px;"></th>
            </tr>
          </thead>
          <tbody>
            <template v-for="consultation in consultations" :key="consultation.id">
              <tr
                class="consultation-row"
                :class="{ expanded: expandedId === consultation.id }"
                @click="toggleExpand(consultation.id)"
                tabindex="0"
                role="row"
                @keydown.enter="toggleExpand(consultation.id)"
                @keydown.space.prevent="toggleExpand(consultation.id)"
              >
                <td>
                  <button
                    class="expand-btn"
                    :class="{ rotated: expandedId === consultation.id }"
                    :aria-expanded="expandedId === consultation.id"
                    aria-label="Expand row"
                    tabindex="-1"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="9 18 15 12 9 6"/>
                    </svg>
                  </button>
                </td>
                <td>
                  <div class="patient-cell">
                    <div class="patient-avatar">{{ getInitials(consultation.patient_name) }}</div>
                    <span class="patient-name">{{ consultation.patient_name }}</span>
                  </div>
                </td>
                <td>
                  <div class="diagnosis-chips">
                    <span
                      v-for="code in consultation.diagnosis_codes"
                      :key="code"
                      class="chip"
                    >{{ code }}</span>
                  </div>
                </td>
                <td>
                  <span class="date-cell">{{ formatDate(consultation.consultation_date) }}</span>
                </td>
                <td>
                  <span class="notes-preview">{{ truncate(consultation.treatment_notes, 50) }}</span>
                </td>
                <td>
                  <button
                    @click.stop="confirmDelete(consultation)"
                    class="btn btn-sm btn-danger"
                    title="Delete consultation"
                    aria-label="Delete consultation"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 13px; height: 13px;">
                      <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                    </svg>
                    Delete
                  </button>
                </td>
              </tr>

              <!-- Expanded Detail Row -->
              <tr v-if="expandedId === consultation.id" class="expanded-detail-row">
                <td colspan="6">
                  <div class="expanded-content">
                    <div class="expanded-grid">
                      <div class="detail-block detail-notes">
                        <div class="detail-label">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 13px; height: 13px;">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
                          </svg>
                          Treatment Notes
                        </div>
                        <p class="detail-value detail-notes-text">{{ consultation.treatment_notes }}</p>
                      </div>
                      <div class="detail-block detail-meta">
                        <div class="meta-item">
                          <span class="meta-label">Consultation ID</span>
                          <span class="meta-value">#{{ consultation.id }}</span>
                        </div>
                        <div class="meta-item">
                          <span class="meta-label">Created</span>
                          <span class="meta-value">{{ formatDateTime(consultation.created_at) }}</span>
                        </div>
                        <div class="meta-item">
                          <span class="meta-label">Diagnoses</span>
                          <span class="meta-value">{{ consultation.diagnosis_codes.length }} code{{ consultation.diagnosis_codes.length !== 1 ? 's' : '' }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <teleport to="body">
      <transition name="fade">
        <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
          <div class="modal" role="dialog" aria-labelledby="delete-title" aria-modal="true">
            <div class="modal-header">
              <h3 id="delete-title">Delete Consultation</h3>
            </div>
            <div class="modal-body">
              <p>Are you sure you want to delete the consultation for <strong>{{ consultationToDelete?.patient_name }}</strong>?</p>
              <p class="text-muted">This action cannot be undone.</p>
            </div>
            <div class="modal-footer">
              <button @click="showDeleteModal = false" class="btn btn-outline">
                Cancel
              </button>
              <button @click="deleteConsultationConfirm" class="btn btn-danger-fill" :disabled="deleting">
                <span v-if="deleting" class="spinner"></span>
                {{ deleting ? 'Deleting…' : 'Delete' }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script setup>
import { ref, inject, onMounted } from 'vue'
import { getConsultations, deleteConsultation } from '../services/api'

const showToast = inject('showToast')

const consultations = ref([])
const total = ref(0)
const loading = ref(true)
const error = ref(null)
const expandedId = ref(null)
const showDeleteModal = ref(false)
const consultationToDelete = ref(null)
const deleting = ref(false)

const fetchConsultations = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await getConsultations()
    consultations.value = response.consultations
    total.value = response.total
  } catch (err) {
    error.value = err.response?.data?.detail || 'Please check your connection and try again.'
  } finally {
    loading.value = false
  }
}

const toggleExpand = (id) => {
  expandedId.value = expandedId.value === id ? null : id
}

const getInitials = (name) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const truncate = (text, maxLen) => {
  if (!text) return ''
  return text.length > maxLen ? text.slice(0, maxLen) + '…' : text
}

const confirmDelete = (consultation) => {
  consultationToDelete.value = consultation
  showDeleteModal.value = true
}

const deleteConsultationConfirm = async () => {
  if (!consultationToDelete.value) return
  deleting.value = true

  try {
    await deleteConsultation(consultationToDelete.value.id)
    consultations.value = consultations.value.filter(
      c => c.id !== consultationToDelete.value.id
    )
    total.value--
    showDeleteModal.value = false
    showToast?.('Consultation deleted successfully', 'success')
    consultationToDelete.value = null
  } catch (err) {
    showToast?.(err.response?.data?.detail || 'Failed to delete consultation', 'error')
  } finally {
    deleting.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatDateTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchConsultations()
})
</script>

<style scoped>
.consultations-page {
  max-width: 1000px;
  margin: 0 auto;
}

/* --- Table Info --- */
.table-info {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-muted);
  font-size: 0.8125rem;
  font-weight: 500;
}

/* --- Patient Cell --- */
.patient-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.patient-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: var(--primary-100);
  color: var(--primary-700);
  font-size: 0.625rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  letter-spacing: 0.02em;
}

.patient-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.8125rem;
}

/* --- Date & Notes --- */
.date-cell {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  white-space: nowrap;
}

.notes-preview {
  font-size: 0.8125rem;
  color: var(--text-muted);
  line-height: 1.4;
}

/* --- Chips --- */
.diagnosis-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* --- Expand Button --- */
.consultation-row {
  cursor: pointer;
}

.expand-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  transition: transform var(--transition-fast), color var(--transition-fast);
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-xs);
}

.expand-btn svg {
  width: 14px;
  height: 14px;
}

.expand-btn.rotated {
  transform: rotate(90deg);
  color: var(--primary-color);
}

.expand-btn:hover {
  color: var(--primary-color);
}

/* --- Expanded Detail --- */
.expanded-detail-row {
  background-color: var(--gray-50) !important;
}

.expanded-detail-row:hover {
  background-color: var(--gray-50) !important;
}

.expanded-content {
  padding: 1rem 0.5rem;
}

.expanded-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1.5rem;
}

.detail-block {
  min-width: 0;
}

.detail-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.detail-notes-text {
  background-color: var(--bg-surface);
  padding: 0.875rem 1rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  font-size: 0.8125rem;
  line-height: 1.65;
  color: var(--text-primary);
  white-space: pre-wrap;
}

.detail-meta {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  min-width: 180px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.meta-label {
  font-size: 0.6875rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-weight: 500;
}

.meta-value {
  font-size: 0.8125rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* --- Responsive --- */
@media (max-width: 768px) {
  .expanded-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .detail-meta {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
    min-width: 0;
  }
}
</style>