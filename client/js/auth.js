// Authentication Module
class AuthManager {
    constructor() {
        this.currentUser = null;
        this.checkAuthState();
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }

    // Get stored tokens
    getTokens() {
        return {
            accessToken: localStorage.getItem('access_token'),
            refreshToken: localStorage.getItem('refresh_token')
        };
    }

    // Store tokens
    storeTokens(accessToken, refreshToken) {
        localStorage.setItem('access_token', accessToken);
        if (refreshToken) {
            localStorage.setItem('refresh_token', refreshToken);
        }
    }

    // Clear tokens and user data
    clearAuth() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        this.currentUser = null;
    }

    // Store user data
    storeUser(user) {
        localStorage.setItem('user', JSON.stringify(user));
        this.currentUser = user;
    }

    // Get stored user
    getStoredUser() {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            return JSON.parse(userStr);
        }
        return null;
    }

    // Check authentication state
    async checkAuthState() {
        if (this.isAuthenticated()) {
            try {
                const response = await api.getCurrentUser();
                if (response.success && response.data.user) {
                    this.currentUser = response.data.user;
                    this.storeUser(response.data.user);
                    return true;
                }
            } catch (error) {
                // Token might be expired, try refresh
                try {
                    await this.refreshAccessToken();
                    const response = await api.getCurrentUser();
                    if (response.success && response.data.user) {
                        this.currentUser = response.data.user;
                        this.storeUser(response.data.user);
                        return true;
                    }
                } catch (refreshError) {
                    // Refresh failed, logout
                    this.logout();
                    return false;
                }
            }
        }
        return false;
    }

    // Refresh access token
    async refreshAccessToken() {
        try {
            const response = await api.refreshToken();
            if (response.success && response.data.access_token) {
                this.storeTokens(response.data.access_token, null);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
            throw error;
        }
        return false;
    }

    // Login
    async login(username, password) {
        try {
            const response = await api.login(username, password);
            if (response.success && response.data) {
                this.storeTokens(
                    response.data.access_token,
                    response.data.refresh_token
                );
                if (response.data.user) {
                    this.storeUser(response.data.user);
                }
                return { success: true, user: response.data.user };
            }
            throw new Error('Login failed');
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Register
    async register(username, password, email = null) {
        try {
            const response = await api.register(username, password, email);
            if (response.success && response.data) {
                this.storeTokens(
                    response.data.access_token,
                    response.data.refresh_token
                );
                if (response.data.user) {
                    this.storeUser(response.data.user);
                }
                return { success: true, user: response.data.user };
            }
            throw new Error('Registration failed');
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    // Logout
    logout() {
        this.clearAuth();
        window.location.hash = '#login';
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser || this.getStoredUser();
    }
}

// Create and export auth manager instance
const authManager = new AuthManager();

