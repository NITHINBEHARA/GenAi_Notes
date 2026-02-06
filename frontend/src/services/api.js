import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add Tenant ID and Auth Token
api.interceptors.request.use(
    (config) => {
        const tenantId = localStorage.getItem('tenant_id');
        const token = localStorage.getItem('auth_token');

        if (tenantId) {
            config.headers['X-Tenant-ID'] = tenantId;
        }
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const authService = {
    login: (email, password) => api.post('/auth/login', { email, password }),
    logout: () => {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('tenant_id');
        localStorage.removeItem('user_info');
    },
};

export const documentService = {
    upload: (formData) => api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    }),
    list: () => api.get('/documents/list'),
    delete: (docId) => api.delete(`/documents/${docId}`),
};

export const ragService = {
    query: (query) => api.post('/rag/query', { query }),
};

export default api;
