// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API Client Class
class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    // Get authorization headers
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };
        
        if (includeAuth) {
            const token = localStorage.getItem('access_token');
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }
        
        return headers;
    }

    // Get headers for file upload
    getFileHeaders() {
        const headers = {};
        const token = localStorage.getItem('access_token');
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        return headers;
    }

    // Make API request
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                ...this.getHeaders(options.includeAuth !== false),
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error?.message || `HTTP error! status: ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication endpoints
    async register(username, password, email = null) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, password, email })
        });
    }

    async login(username, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
            includeAuth: false
        });
    }

    async refreshToken() {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        const response = await fetch(`${this.baseURL}/auth/refresh`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${refreshToken}`
            }
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error?.message || 'Token refresh failed');
        }

        return data;
    }

    async getCurrentUser() {
        return this.request('/auth/me');
    }

    // Classification endpoints
    async classifyImage(imageFile) {
        const formData = new FormData();
        formData.append('image', imageFile);

        const token = localStorage.getItem('access_token');
        const response = await fetch(`${this.baseURL}/classify`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error?.message || 'Classification failed');
        }

        return data;
    }

    async getClassifications(page = 1, perPage = 20, wasteType = '', search = '') {
        const params = new URLSearchParams();
        params.set('page', page);
        params.set('per_page', perPage);
        if (wasteType) params.set('waste_type', wasteType);
        if (search) params.set('q', search);
        return this.request(`/classifications?${params.toString()}`);
    }

    async getClassificationDetail(id) {
        return this.request(`/classifications/${id}`);
    }

    async realtimeCapture(imageBlob = null, deviceIndex = 0) {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('Not authenticated');
        }

        const headers = {
            'Authorization': `Bearer ${token}`
        };

        let body;
        let url = `${this.baseURL}/realtime/capture`;

        if (imageBlob) {
            body = new FormData();
            body.append('image', imageBlob, 'frame.jpg');
        } else {
            body = new FormData();
            body.append('device_index', deviceIndex);
        }

        const response = await fetch(url, {
            method: 'POST',
            headers,
            body
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error?.message || 'Realtime capture failed');
        }
        return data;
    }

    // Feedback endpoints
    async submitFeedback(classificationId, feedbackText, feedbackType = 'neutral') {
        return this.request('/feedbacks', {
            method: 'POST',
            body: JSON.stringify({
                classification_id: classificationId,
                feedback_text: feedbackText,
                feedback_type: feedbackType
            })
        });
    }

    async getFeedbacks(page = 1, perPage = 20, type = null) {
        let url = `/feedbacks?page=${page}&per_page=${perPage}`;
        if (type) {
            url += `&type=${type}`;
        }
        return this.request(url);
    }

    async deleteFeedback(feedbackId) {
        return this.request(`/feedbacks/${feedbackId}`, {
            method: 'DELETE'
        });
    }

    // User endpoints
    async getUserProfile() {
        return this.request('/users/me');
    }

    async updateProfile(email = null, password = null) {
        const body = {};
        if (email !== null) body.email = email;
        if (password !== null) body.password = password;

        return this.request('/users/me', {
            method: 'PUT',
            body: JSON.stringify(body)
        });
    }

    async getUserStats() {
        return this.request('/users/me/stats');
    }
}

// Create and export API client instance
const api = new APIClient();

