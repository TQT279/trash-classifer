// Utility Functions

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Format file size
function formatFileSize(bytes) {
    if (!bytes) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format percentage
function formatPercentage(value) {
    if (value === null || value === undefined) return '0%';
    return (value * 100).toFixed(2) + '%';
}

// Get waste type color
function getWasteTypeColor(wasteType) {
    const colors = {
        'cardboard': '#8B4513',
        'e-waste': '#FF6B35',
        'glass': '#4ECDC4',
        'medical': '#FF0000',
        'metal': '#708090',
        'paper': '#FFD700',
        'plastic': '#1E90FF'
    };
    return colors[wasteType?.toLowerCase()] || '#757575';
}

// Get waste type icon
function getWasteTypeIcon(wasteType) {
    const icons = {
        'cardboard': 'inventory_2',
        'e-waste': 'devices',
        'glass': 'wine_bar',
        'medical': 'medical_services',
        'metal': 'build',
        'paper': 'description',
        'plastic': 'category'
    };
    return icons[wasteType?.toLowerCase()] || 'help';
}

// Validate email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate file type
function validateImageFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    return allowedTypes.includes(file.type);
}

// Validate file size (max 16MB)
function validateFileSize(file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    return file.size <= maxSize;
}

// Create image preview URL
function createImagePreview(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Capitalize first letter
function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Truncate text
function truncate(text, maxLength) {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Get image URL from path (assuming images are served from uploads folder)
function getImageUrl(imagePath) {
    if (!imagePath) return '';
    // Normalize backslashes to forward slashes for Windows paths
    imagePath = imagePath.replace(/\\/g, '/');
    // If it's already a full URL, return as is
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        return imagePath;
    }
    // Otherwise, construct URL from API base
    const baseUrl = 'http://localhost:5000'; // API base URL without /api
    return `${baseUrl}/${imagePath}`;
}

