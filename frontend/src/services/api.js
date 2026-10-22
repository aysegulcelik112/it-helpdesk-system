/**
 * API Servis Katmanı
 * 
 * Backend ile iletişim için Axios tabanlı servis fonksiyonları.
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - her isteğe token ekle
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - hata yönetimi
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth API
export const authAPI = {
  login: (email, password) => 
    api.post('/auth/login', { username: email, password }),

  
  register: (userData) => 
    api.post('/auth/register', userData),
  
  getMe: () => 
    api.get('/auth/me'),
};

// Tickets API
export const ticketsAPI = {
  create: (ticketData) => 
    api.post('/tickets/', ticketData),
  
  list: (filters = {}) => {
    const params = new URLSearchParams();
    if (filters.status) params.append('status_filter', filters.status);
    if (filters.category) params.append('category', filters.category);
    if (filters.priority) params.append('priority', filters.priority);
    return api.get(`/tickets/?${params.toString()}`);
  },
  
  getById: (ticketId) => 
    api.get(`/tickets/${ticketId}`),
  
  update: (ticketId, updateData) => 
    api.patch(`/tickets/${ticketId}`, updateData),
  
  assignToMe: (ticketId) => 
    api.post(`/tickets/${ticketId}/assign-to-me`),
  
  close: (ticketId) => 
    api.post(`/tickets/${ticketId}/close`),
};

// Comments API
export const commentsAPI = {
  create: (ticketId, message) => 
    api.post(`/tickets/${ticketId}/comments`, { message }),
  
  list: (ticketId) => 
    api.get(`/tickets/${ticketId}/comments`),
};

