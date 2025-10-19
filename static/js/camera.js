const startBtn = document.getElementById('start-camera');
const takeBtn = document.getElementById('take-photo');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const cameraImageInput = document.getElementById('camera_image');
const cameraWrap = document.getElementById('camera-wrap');
const photoPreview = document.getElementById('photo-preview');
const clearPhotoBtn = document.getElementById('clear-photo');
let stream;

startBtn.addEventListener('click', async (e) => {
  e.preventDefault();
  if (stream) {
    // stop
    stream.getTracks().forEach(t=>t.stop());
    stream = null;
    startBtn.textContent = 'Start Camera';
    takeBtn.disabled = true;
    return;
  }
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
    video.srcObject = stream;
    startBtn.textContent = 'Stop Camera';
    takeBtn.disabled = false;
    // once metadata loaded we can set container aspect ratio to match video
    video.addEventListener('loadedmetadata', () => {
      const vw = video.videoWidth;
      const vh = video.videoHeight;
      if (vw && vh) {
        const ratio = (vh / vw) * 100; // percent padding-bottom
        const inner = cameraWrap.querySelector('.video-inner');
        if (inner) inner.style.paddingBottom = ratio + '%';
      }
    });
  } catch (err) {
    alert('Could not start camera: ' + err.message);
  }
});

// Limit longest side to maxSize to reduce upload but preserve whole image
const MAX_SIDE = 1024;

takeBtn.addEventListener('click', (e) => {
  e.preventDefault();
  const vw = video.videoWidth;
  const vh = video.videoHeight;
  // compute scaled size preserving aspect ratio
  let outW = vw, outH = vh;
  const maxSide = Math.max(vw, vh);
  if (maxSide > MAX_SIDE) {
    const scale = MAX_SIDE / maxSide;
    outW = Math.round(vw * scale);
    outH = Math.round(vh * scale);
  }
  canvas.width = outW;
  canvas.height = outH;
  const ctx = canvas.getContext('2d');
  // draw the entire video frame scaled into canvas (no cropping)
  ctx.drawImage(video, 0, 0, outW, outH);
  const data = canvas.toDataURL('image/jpeg', 0.9);
  cameraImageInput.value = data;
  // submit the hidden form
  // show preview instead of immediate submit so user can confirm
  photoPreview.src = data;
  photoPreview.hidden = false;
  // hide video to avoid confusion
  video.hidden = true;
  takeBtn.disabled = true;
  clearPhotoBtn.style.display = 'inline-block';
  // auto-submit after short delay? keep manual for now
  document.getElementById('camera-form').submit();
});

clearPhotoBtn?.addEventListener('click', (e) => {
  e.preventDefault();
  photoPreview.hidden = true;
  photoPreview.src = '';
  video.hidden = false;
  takeBtn.disabled = false;
  clearPhotoBtn.style.display = 'none';
  cameraImageInput.value = '';
});