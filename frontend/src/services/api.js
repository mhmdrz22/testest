import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const taskAPI = {
  // Get all tasks
  getTasks: () => apiClient.get('/tasks/'),

  // Get single task
  getTask: (id) => apiClient.get(`/tasks/${id}/`),

  // Create task
  createTask: (data) => apiClient.post('/tasks/', data),

  // Update task
  updateTask: (id, data) => apiClient.patch(`/tasks/${id}/`, data),

  // Delete task
  deleteTask: (id) => apiClient.delete(`/tasks/${id}/`),
}

export const userAPI = {
  // Get all users
  getUsers: () => apiClient.get('/users/'),

  // Get current user
  getCurrentUser: () => apiClient.get('/users/me/'),

  // Get user profile
  getProfile: (id) => apiClient.get(`/users/${id}/`),
}

export const adminAPI = {
  // Get admin overview
  getOverview: () => apiClient.get('/admin/overview/'),

  // Send notification email
  sendNotification: (data) => apiClient.post('/admin/notify/', data),

  // Get email templates
  getEmailTemplates: () => apiClient.get('/admin/email-templates/'),
}

export const authAPI = {
  // Login
  login: (email, password) =>
    apiClient.post('/token/', { email, password }),

  // Logout
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  },

  // Register
  register: (data) => apiClient.post('/register/', data),
}

export default apiClient
