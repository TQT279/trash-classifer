class RealtimeController {
    constructor() {
        this.video = null;
        this.canvas = null;
        this.startBtn = null;
        this.stopBtn = null;
        this.captureBtn = null;
        this.resultBox = null;
        this.stream = null;
        this.active = false;
    }

    init() {
        this.video = document.getElementById('realtimeVideo');
        this.canvas = document.createElement('canvas');
        this.startBtn = document.getElementById('startRealtime');
        this.stopBtn = document.getElementById('stopRealtime');
        this.captureBtn = document.getElementById('captureRealtime');
        this.resultBox = document.getElementById('realtimeResult');

        // Hide/disable controls until camera is active
        this.setButtonsState(false, true);

        if (this.startBtn) {
            this.startBtn.addEventListener('click', () => this.startCamera());
        }
        if (this.stopBtn) {
            this.stopBtn.addEventListener('click', () => this.stopCamera());
        }
        if (this.captureBtn) {
            this.captureBtn.addEventListener('click', () => this.captureAndSend());
        }
    }

    async startCamera() {
        if (this.active) return;
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
            this.video.srcObject = this.stream;
            this.video.play();
            this.active = true;
            this.setButtonsState(true, false);
            showSnackbar('Camera started', 'success');
        } catch (err) {
            showSnackbar('Unable to access camera', 'error');
            console.error(err);
        }
    }

    stopCamera() {
        if (this.stream) {
            this.stream.getTracks().forEach(t => t.stop());
        }
        if (this.video) {
            this.video.srcObject = null;
        }
        this.active = false;
        this.setButtonsState(false, true);
    }

    async captureAndSend() {
        if (!this.active || !this.video) {
            showSnackbar('Start the camera first', 'error');
            return;
        }

        try {
            const blob = await this.captureFrame();
            showLoading('Classifying frame...');
            const response = await api.realtimeCapture(blob);
            hideLoading();
            this.renderResult(response.data?.prediction);
        } catch (err) {
            hideLoading();
            showSnackbar(err.message || 'Realtime classification failed', 'error');
        }
    }

    captureFrame() {
        return new Promise((resolve, reject) => {
            const video = this.video;
            if (!video) return reject(new Error('Video element not found'));

            this.canvas.width = video.videoWidth;
            this.canvas.height = video.videoHeight;
            const ctx = this.canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, this.canvas.width, this.canvas.height);
            this.canvas.toBlob(blob => {
                if (blob) resolve(blob);
                else reject(new Error('Failed to capture frame'));
            }, 'image/jpeg');
        });
    }

    setButtonsState(isActive, hideStop = false) {
        if (this.startBtn) this.startBtn.disabled = isActive;
        if (this.stopBtn) {
            this.stopBtn.disabled = !isActive;
            this.stopBtn.style.display = hideStop ? 'none' : 'inline-flex';
        }
        if (this.captureBtn) this.captureBtn.disabled = !isActive;
    }

    renderResult(prediction) {
        if (!prediction || !this.resultBox) return;
        const wasteType = prediction.waste_type || 'Unknown';
        const confidence = prediction.confidence_score || 0;
        const time = prediction.timestamp || '';

        this.resultBox.innerHTML = `
            <div class="result-main">
                <div class="result-type">
                    <span class="material-icons">${getWasteTypeIcon(wasteType)}</span>
                    <h3>${capitalize(wasteType)}</h3>
                </div>
                <div class="result-confidence">
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: ${confidence * 100}%;"></div>
                    </div>
                    <span>${formatPercentage(confidence)}</span>
                </div>
                <div class="result-meta">
                    <small>${time}</small>
                </div>
            </div>
        `;
    }
}

// Global instance
const realtimeController = new RealtimeController();

