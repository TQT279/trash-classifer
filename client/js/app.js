// Main Application
class WasteClassifierApp {
    constructor() {
        this.currentView = 'login';
        this.currentPage = 1;
        this.wasteTypes = [];
        this.init();
    }

    async init() {
        // Check authentication
        const isAuth = await authManager.checkAuthState();
        
        if (isAuth) {
            this.showView('dashboard');
            this.setupNavigation();
        } else {
            this.showView('login');
        }

        this.setupEventListeners();
        this.loadWasteTypes();
        // Initialize realtime controller (camera capture)
        if (typeof realtimeController !== 'undefined') {
            realtimeController.init();
        }
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const view = e.currentTarget.getAttribute('data-view');
                this.showView(view);
            });
        });

        // Logout
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                authManager.logout();
                this.showView('login');
            });
        }

        // Auth forms
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        // Show register/login
        const showRegister = document.getElementById('showRegister');
        if (showRegister) {
            showRegister.addEventListener('click', (e) => {
                e.preventDefault();
                this.showView('register');
            });
        }

        const showLogin = document.getElementById('showLogin');
        if (showLogin) {
            showLogin.addEventListener('click', (e) => {
                e.preventDefault();
                this.showView('login');
            });
        }

        // Dashboard
        this.setupDashboard();

        // History
        this.setupHistory();

        // Profile
        this.setupProfile();
    }

    setupNavigation() {
        const navbar = document.getElementById('navbar');
        if (navbar) {
            navbar.style.display = 'block';
        }
    }

    showView(viewName) {
        // Hide all views
        document.querySelectorAll('.view').forEach(view => {
            view.style.display = 'none';
        });

        // Show selected view
        const view = document.getElementById(`${viewName}View`);
        if (view) {
            view.style.display = 'block';
            this.currentView = viewName;
        }

        // Show/hide navbar
        const navbar = document.getElementById('navbar');
        if (navbar) {
            navbar.style.display = (viewName !== 'login' && viewName !== 'register') ? 'block' : 'none';
        }

        // Load view-specific data
        if (viewName === 'dashboard') {
            this.resetDashboard();
        } else if (viewName === 'history') {
            this.loadHistory();
        } else if (viewName === 'profile') {
            this.loadProfile();
        }

        // Stop camera when leaving dashboard to free resources
        if (viewName !== 'dashboard' && typeof realtimeController !== 'undefined') {
            realtimeController.stopCamera();
        }
    }

    // Authentication handlers
    async handleLogin(e) {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        showLoading('Signing in...');
        const result = await authManager.login(username, password);
        hideLoading();

        if (result.success) {
            showSnackbar('Login successful!', 'success');
            this.setupNavigation();
            this.showView('dashboard');
        } else {
            showSnackbar(result.error || 'Login failed', 'error');
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        showLoading('Creating account...');
        const result = await authManager.register(username, password, email || null);
        hideLoading();

        if (result.success) {
            showSnackbar('Registration successful!', 'success');
            this.setupNavigation();
            this.showView('dashboard');
        } else {
            showSnackbar(result.error || 'Registration failed', 'error');
        }
    }

    // Dashboard setup
    setupDashboard() {
        const selectImageBtn = document.getElementById('selectImageBtn');
        const imageInput = document.getElementById('imageInput');
        const uploadArea = document.getElementById('uploadArea');
        const classifyBtn = document.getElementById('classifyBtn');
        const removeImageBtn = document.getElementById('removeImageBtn');

        // File input
        if (selectImageBtn && imageInput) {
            selectImageBtn.addEventListener('click', () => imageInput.click());
        }

        if (imageInput) {
            imageInput.addEventListener('change', (e) => this.handleImageSelect(e));
        }

        // Drag and drop
        if (uploadArea) {
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('drag-over');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('drag-over');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('drag-over');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    this.handleImageFile(files[0]);
                }
            });
        }

        // Classify button
        if (classifyBtn) {
            classifyBtn.addEventListener('click', () => this.handleClassify());
        }

        // Remove image
        if (removeImageBtn) {
            removeImageBtn.addEventListener('click', () => this.resetDashboard());
        }
    }

    handleImageSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.handleImageFile(file);
        }
    }

    async handleImageFile(file) {
        // Validate file
        if (!validateImageFile(file)) {
            showSnackbar('Invalid file type. Please select an image.', 'error');
            return;
        }

        if (!validateFileSize(file)) {
            showSnackbar('File size too large. Maximum 16MB.', 'error');
            return;
        }

        // Show preview
        const preview = document.getElementById('imagePreview');
        const previewImg = document.getElementById('previewImg');
        const uploadArea = document.getElementById('uploadArea');
        const classifyBtn = document.getElementById('classifyBtn');

        try {
            const previewUrl = await createImagePreview(file);
            previewImg.src = previewUrl;
            preview.style.display = 'block';
            if (uploadArea) uploadArea.style.display = 'none';
            if (classifyBtn) classifyBtn.style.display = 'flex';
            
            // Store file for classification
            this.selectedFile = file;
        } catch (error) {
            showSnackbar('Error loading image preview', 'error');
        }
    }

    resetDashboard() {
        const preview = document.getElementById('imagePreview');
        const uploadArea = document.getElementById('uploadArea');
        const classifyBtn = document.getElementById('classifyBtn');
        const resultSection = document.getElementById('resultSection');
        const imageInput = document.getElementById('imageInput');

        if (preview) preview.style.display = 'none';
        if (uploadArea) uploadArea.style.display = 'block';
        if (classifyBtn) classifyBtn.style.display = 'none';
        if (resultSection) resultSection.style.display = 'none';
        if (imageInput) imageInput.value = '';
        this.selectedFile = null;
    }

    async handleClassify() {
        if (!this.selectedFile) {
            showSnackbar('Please select an image first', 'error');
            return;
        }

        showLoading('Classifying waste...');
        try {
            const response = await api.classifyImage(this.selectedFile);
            hideLoading();

            if (response.success && response.data.classification) {
                this.displayClassificationResult(response.data);
                showSnackbar('Classification completed!', 'success');
            } else {
                showSnackbar('Classification failed', 'error');
            }
        } catch (error) {
            hideLoading();
            showSnackbar(error.message || 'Classification failed', 'error');
        }
    }

    displayClassificationResult(data) {
        const resultSection = document.getElementById('resultSection');
        const resultContent = document.getElementById('resultContent');
        const classification = data.classification;
        const wasteType = classification.waste_type?.name || 'Unknown';
        const confidence = classification.confidence_score || 0;
        const color = getWasteTypeColor(wasteType);
        const icon = getWasteTypeIcon(wasteType);

        if (resultContent) {
            resultContent.innerHTML = `
                <div class="result-main">
                    <div class="result-type" style="color: ${color};">
                        <span class="material-icons">${icon}</span>
                        <h3>${capitalize(wasteType)}</h3>
                    </div>
                    <div class="result-confidence">
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${confidence * 100}%; background-color: ${color};"></div>
                        </div>
                        <span>${formatPercentage(confidence)}</span>
                    </div>
                </div>
                ${data.prediction_details?.all_predictions ? `
                    <div class="result-details">
                        <h4>All Predictions:</h4>
                        <div class="predictions-list">
                            ${Object.entries(data.prediction_details.all_predictions)
                                .sort((a, b) => b[1] - a[1])
                                .map(([type, score]) => `
                                    <div class="prediction-item">
                                        <span>${capitalize(type)}</span>
                                        <span>${formatPercentage(score)}</span>
                                    </div>
                                `).join('')}
                        </div>
                    </div>
                ` : ''}
                <div class="result-actions">
                    <button class="btn-primary btn-feedback" data-id="${classification.id}">
                        <span class="material-icons">feedback</span>
                        <span>Provide Feedback</span>
                    </button>
                </div>
            `;

            // Add feedback button handler
            const feedbackBtn = resultContent.querySelector('.btn-feedback');
            if (feedbackBtn) {
                feedbackBtn.addEventListener('click', () => {
                    this.showFeedbackModal(classification.id);
                });
            }
        }

        if (resultSection) {
            resultSection.style.display = 'block';
        }
    }

    // History setup
    setupHistory() {
        const filterWasteType = document.getElementById('filterWasteType');
        const searchInput = document.getElementById('searchInput');

        if (filterWasteType) {
            filterWasteType.addEventListener('change', () => {
                this.currentPage = 1;
                this.loadHistory();
            });
        }

        if (searchInput) {
            searchInput.addEventListener('input', debounce(() => {
                this.currentPage = 1;
                this.loadHistory();
            }, 500));
        }

        // Delegate event listeners for dynamic content
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-view-details')) {
                const id = e.target.closest('.btn-view-details').getAttribute('data-id');
                this.showClassificationDetails(id);
            }
            if (e.target.closest('.btn-feedback')) {
                const id = e.target.closest('.btn-feedback').getAttribute('data-id');
                this.showFeedbackModal(id);
            }
        });
    }

    async loadHistory() {
        const filterWasteType = document.getElementById('filterWasteType');
        const searchInput = document.getElementById('searchInput');
        const wasteType = filterWasteType ? filterWasteType.value : '';
        const search = searchInput ? searchInput.value.trim() : '';

        showLoading('Loading history...');
        try {
            const response = await api.getClassifications(this.currentPage, 20, wasteType, search);
            hideLoading();

            if (response.success && response.data) {
                this.displayHistory(response.data);
            }
        } catch (error) {
            hideLoading();
            showSnackbar(error.message || 'Failed to load history', 'error');
        }
    }

    displayHistory(data) {
        const historyList = document.getElementById('historyList');
        const pagination = document.getElementById('pagination');

        if (historyList) {
            if (data.classifications && data.classifications.length > 0) {
                historyList.innerHTML = data.classifications
                    .map(classification => createClassificationCard(classification))
                    .join('');
            } else {
                historyList.innerHTML = '<p class="empty-state">No classifications found</p>';
            }
        }

        // Pagination
        if (pagination && data.pagination) {
            const pag = data.pagination;
            let paginationHTML = '';

            if (pag.has_prev) {
                paginationHTML += `<button class="btn-text" data-page="${pag.page - 1}">Previous</button>`;
            }

            paginationHTML += `<span>Page ${pag.page} of ${pag.pages}</span>`;

            if (pag.has_next) {
                paginationHTML += `<button class="btn-text" data-page="${pag.page + 1}">Next</button>`;
            }

            pagination.innerHTML = paginationHTML;

            // Add page button handlers
            pagination.querySelectorAll('button[data-page]').forEach(btn => {
                btn.addEventListener('click', () => {
                    this.currentPage = parseInt(btn.getAttribute('data-page'));
                    this.loadHistory();
                });
            });
        }
    }

    async showClassificationDetails(id) {
        showLoading('Loading details...');
        try {
            const response = await api.getClassificationDetail(id);
            hideLoading();

            if (response.success && response.data.classification) {
                const classification = response.data.classification;
                const content = `
                    <div class="detail-content">
                        <div class="detail-image">
                            ${classification.image ? `
                                <img src="${getImageUrl(classification.image.image_path)}" alt="Classification">
                            ` : ''}
                        </div>
                        <div class="detail-info">
                            <div class="info-row">
                                <strong>Waste Type:</strong>
                                <span>${capitalize(classification.waste_type?.name || 'Unknown')}</span>
                            </div>
                            <div class="info-row">
                                <strong>Confidence:</strong>
                                <span>${formatPercentage(classification.confidence_score)}</span>
                            </div>
                            <div class="info-row">
                                <strong>Date:</strong>
                                <span>${formatDate(classification.classified_at)}</span>
                            </div>
                            ${classification.processing_time_ms ? `
                                <div class="info-row">
                                    <strong>Processing Time:</strong>
                                    <span>${classification.processing_time_ms}ms</span>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                `;
                showModal('Classification Details', content);
            }
        } catch (error) {
            hideLoading();
            showSnackbar(error.message || 'Failed to load details', 'error');
        }
    }

    // Profile setup
    setupProfile() {
        const profileForm = document.getElementById('profileForm');
        const passwordForm = document.getElementById('passwordForm');

        if (profileForm) {
            profileForm.addEventListener('submit', (e) => this.handleUpdateProfile(e));
        }

        if (passwordForm) {
            passwordForm.addEventListener('submit', (e) => this.handleChangePassword(e));
        }
    }

    async loadProfile() {
        const user = authManager.getCurrentUser();
        const profileUsername = document.getElementById('profileUsername');
        const profileEmail = document.getElementById('profileEmail');

        if (user) {
            if (profileUsername) profileUsername.value = user.username || '';
            if (profileEmail) profileEmail.value = user.email || '';
        }

        // Load stats
        showLoading('Loading statistics...');
        try {
            const response = await api.getUserStats();
            hideLoading();

            if (response.success && response.data.stats) {
                this.displayStats(response.data.stats);
            }
        } catch (error) {
            hideLoading();
            showSnackbar(error.message || 'Failed to load statistics', 'error');
        }
    }

    displayStats(stats) {
        document.getElementById('statTotalImages').textContent = stats.total_images || 0;
        document.getElementById('statTotalClassifications').textContent = stats.total_classifications || 0;
        document.getElementById('statAvgConfidence').textContent = formatPercentage(stats.average_confidence || 0);
        document.getElementById('statTotalFeedbacks').textContent = stats.total_feedbacks || 0;

        // Breakdown by type
        const breakdown = document.getElementById('statsBreakdown');
        if (breakdown && stats.classifications_by_type) {
            const types = Object.entries(stats.classifications_by_type);
            if (types.length > 0) {
                breakdown.innerHTML = `
                    <h3>By Waste Type</h3>
                    <div class="stats-types">
                        ${types.map(([type, count]) => `
                            <div class="stat-type-item">
                                <span class="material-icons">${getWasteTypeIcon(type)}</span>
                                <span>${capitalize(type)}</span>
                                <strong>${count}</strong>
                            </div>
                        `).join('')}
                    </div>
                `;
            }
        }
    }

    async handleUpdateProfile(e) {
        e.preventDefault();
        const email = document.getElementById('profileEmail').value;

        showLoading('Updating profile...');
        try {
            const response = await api.updateProfile(email, null);
            hideLoading();

            if (response.success) {
                showSnackbar('Profile updated successfully!', 'success');
                if (response.data.user) {
                    authManager.storeUser(response.data.user);
                }
            } else {
                showSnackbar('Failed to update profile', 'error');
            }
        } catch (error) {
            hideLoading();
            showSnackbar(error.message || 'Failed to update profile', 'error');
        }
    }

    async handleChangePassword(e) {
        e.preventDefault();
        const password = document.getElementById('newPassword').value;

        showLoading('Changing password...');
        try {
            const response = await api.updateProfile(null, password);
            hideLoading();

            if (response.success) {
                showSnackbar('Password changed successfully!', 'success');
                e.target.reset();
            } else {
                showSnackbar('Failed to change password', 'error');
            }
        } catch (error) {
            hideLoading();
            showSnackbar(error.message || 'Failed to change password', 'error');
        }
    }

    // Feedback modal
    showFeedbackModal(classificationId) {
        const content = `
            <form id="feedbackForm" class="feedback-form">
                <input type="hidden" id="feedbackClassificationId" value="${classificationId}">
                <div class="input-group">
                    <label>Feedback Type</label>
                    <select id="feedbackType" class="input-field" required>
                        <option value="positive">Positive</option>
                        <option value="negative">Negative</option>
                        <option value="neutral" selected>Neutral</option>
                    </select>
                </div>
                <div class="input-group">
                    <label>Feedback (optional)</label>
                    <textarea id="feedbackText" class="input-field" rows="4" placeholder="Enter your feedback..."></textarea>
                </div>
                <button type="submit" class="btn-primary btn-block">
                    <span>Submit Feedback</span>
                </button>
            </form>
        `;

        showModal('Provide Feedback', content);

        const feedbackForm = document.getElementById('feedbackForm');
        if (feedbackForm) {
            feedbackForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const feedbackType = document.getElementById('feedbackType').value;
                const feedbackText = document.getElementById('feedbackText').value;

                showLoading('Submitting feedback...');
                try {
                    const response = await api.submitFeedback(classificationId, feedbackText, feedbackType);
                    hideLoading();

                    if (response.success) {
                        showSnackbar('Feedback submitted successfully!', 'success');
                        hideModal();
                    } else {
                        showSnackbar('Failed to submit feedback', 'error');
                    }
                } catch (error) {
                    hideLoading();
                    showSnackbar(error.message || 'Failed to submit feedback', 'error');
                }
            });
        }
    }

    async loadWasteTypes() {
        // This would typically come from an API endpoint
        // For now, using known types from the model
        this.wasteTypes = ['cardboard', 'e-waste', 'glass', 'medical', 'metal', 'paper', 'plastic'];
        
        const filterSelect = document.getElementById('filterWasteType');
        if (filterSelect) {
            filterSelect.innerHTML = '<option value="">All Types</option>' +
                this.wasteTypes.map(type => 
                    `<option value="${type}">${capitalize(type)}</option>`
                ).join('');
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new WasteClassifierApp();
});

