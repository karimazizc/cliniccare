import axios from 'axios'

// Create axios instance with default configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('[API Error]', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

/**
 * Search ICD-10 diagnosis codes
 * @param {string} searchTerm - Search term for code or description
 * @returns {Promise<Array>} Array of diagnosis codes
 */
export const searchDiagnosisCodes = async (searchTerm = '') => {
  try {
    const response = await api.get('/api/diagnosis', {
      params: { search: searchTerm }
    })
    return response.data
  } catch (error) {
    console.error('Error searching diagnosis codes:', error)
    throw error
  }
}

/**
 * Create a new consultation
 * @param {Object} consultationData - Consultation data
 * @param {string} consultationData.patient_name - Patient's name
 * @param {Array<string>} consultationData.diagnosis_codes - Array of ICD-10 codes
 * @param {string} consultationData.treatment_notes - Treatment notes
 * @returns {Promise<Object>} Created consultation
 */
export const createConsultation = async (consultationData) => {
  try {
    const response = await api.post('/api/consultation', consultationData)
    return response.data
  } catch (error) {
    console.error('Error creating consultation:', error)
    throw error
  }
}

/**
 * Get all consultations
 * @param {number} skip - Number of records to skip
 * @param {number} limit - Maximum number of records to return
 * @returns {Promise<Object>} Object containing consultations array and total count
 */
export const getConsultations = async (skip = 0, limit = 100) => {
  try {
    const response = await api.get('/api/consultations', {
      params: { skip, limit }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching consultations:', error)
    throw error
  }
}

/**
 * Get a single consultation by ID
 * @param {number} id - Consultation ID
 * @returns {Promise<Object>} Consultation details
 */
export const getConsultation = async (id) => {
  try {
    const response = await api.get(`/api/consultation/${id}`)
    return response.data
  } catch (error) {
    console.error('Error fetching consultation:', error)
    throw error
  }
}

/**
 * Delete a consultation by ID
 * @param {number} id - Consultation ID
 * @returns {Promise<void>}
 */
export const deleteConsultation = async (id) => {
  try {
    await api.delete(`/api/consultation/${id}`)
  } catch (error) {
    console.error('Error deleting consultation:', error)
    throw error
  }
}

export default api
