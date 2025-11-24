// UI Components

// Show loading overlay
function showLoading(text = 'Loading...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    if (overlay) {
        loadingText.textContent = text;
        overlay.style.display = 'flex';
    }
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Show snackbar notification
function showSnackbar(message, type = 'info', duration = 3000) {
    const snackbar = document.getElementById('snackbar');
    if (!snackbar) return;

    snackbar.textContent = message;
    snackbar.className = `snackbar snackbar-${type} snackbar-show`;
    
    setTimeout(() => {
        snackbar.classList.remove('snackbar-show');
    }, duration);
}

// Show modal
function showModal(title, content) {
    const overlay = document.getElementById('modalOverlay');
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modalTitle');
    const modalContent = document.getElementById('modalContent');

    if (overlay && modal && modalTitle && modalContent) {
        modalTitle.textContent = title;
        modalContent.innerHTML = content;
        overlay.style.display = 'flex';
    }
}

// Hide modal
function hideModal() {
    const overlay = document.getElementById('modalOverlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

// Create classification card
function createClassificationCard(classification) {
    const wasteType = classification.waste_type?.name || 'Unknown';
    const confidence = classification.confidence_score || 0;
    const date = formatDate(classification.classified_at);
    const color = getWasteTypeColor(wasteType);
    const icon = getWasteTypeIcon(wasteType);

    return `
        <div class="classification-card" data-id="${classification.id}">
            <div class="card-header">
                <div class="waste-type-badge" style="background-color: ${color}20; color: ${color};">
                    <span class="material-icons">${icon}</span>
                    <span>${capitalize(wasteType)}</span>
                </div>
                <div class="confidence-badge">
                    ${formatPercentage(confidence)}
                </div>
            </div>
            ${classification.image ? `
                <div class="card-image">
                    <img src="${getImageUrl(classification.image.image_path)}" alt="Classification">
                </div>
            ` : ''}
            <div class="card-content">
                <div class="card-info">
                    <div class="info-item">
                        <span class="material-icons">schedule</span>
                        <span>${date}</span>
                    </div>
                    ${classification.processing_time_ms ? `
                        <div class="info-item">
                            <span class="material-icons">speed</span>
                            <span>${classification.processing_time_ms}ms</span>
                        </div>
                    ` : ''}
                </div>
                <div class="card-actions">
                    <button class="btn-text btn-view-details" data-id="${classification.id}">
                        <span class="material-icons">visibility</span>
                        <span>View Details</span>
                    </button>
                    <button class="btn-text btn-feedback" data-id="${classification.id}">
                        <span class="material-icons">feedback</span>
                        <span>Feedback</span>
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Create feedback card
function createFeedbackCard(feedback) {
    const type = feedback.feedback_type || 'neutral';
    const typeColors = {
        'positive': '#4CAF50',
        'negative': '#F44336',
        'neutral': '#757575'
    };
    const color = typeColors[type] || '#757575';

    return `
        <div class="feedback-card">
            <div class="feedback-header">
                <div class="feedback-type" style="color: ${color};">
                    <span class="material-icons">${type === 'positive' ? 'thumb_up' : type === 'negative' ? 'thumb_down' : 'remove'}</span>
                    <span>${capitalize(type)}</span>
                </div>
                <div class="feedback-date">${formatDate(feedback.created_at)}</div>
            </div>
            ${feedback.feedback_text ? `
                <div class="feedback-text">${feedback.feedback_text}</div>
            ` : ''}
            ${feedback.classification ? `
                <div class="feedback-classification">
                    Classification: ${feedback.classification.waste_type?.name || 'Unknown'}
                </div>
            ` : ''}
        </div>
    `;
}

// Initialize modal close handlers
document.addEventListener('DOMContentLoaded', () => {
    const closeModalBtn = document.getElementById('closeModal');
    const modalOverlay = document.getElementById('modalOverlay');

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', hideModal);
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                hideModal();
            }
        });
    }
});

