import axios from 'axios'

const API_BASE_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Customers API
export const customersAPI = {
  getAll: () => api.get('/customers'),
  getById: (id) => api.get(`/customers/${id}`),
  search: (name) => api.get('/customers/search', { params: { name } }),
  getPremium: () => api.get('/customers/premium'),
  create: (data) => api.post('/customers', data),
  update: (id, data) => api.put(`/customers/${id}`, data),
  delete: (id) => api.delete(`/customers/${id}`)
}

// Accounts API
export const accountsAPI = {
  getAll: () => api.get('/accounts'),
  getById: (id) => api.get(`/accounts/${id}`),
  search: (name) => api.get('/accounts/search', { params: { name } }),
  create: (data) => api.post('/accounts', data),
  update: (id, data) => api.put(`/accounts/${id}`, data),
  delete: (id) => api.delete(`/accounts/${id}`)
}

export default api
