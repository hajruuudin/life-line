import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Only clear token for actual JWT auth errors, not Google API errors
    if (error.response?.status === 401) {
      const url = error.config?.url || ''
      
      // Check if this is a Google API endpoint
      const isGoogleEndpoint = url.includes('/drive') || url.includes('/calendar')
      
      // Only logout if it's NOT a Google endpoint and IS a LifeLine endpoint
      if (!isGoogleEndpoint) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api

