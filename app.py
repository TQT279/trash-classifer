from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename
from PIL import Image


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'


# Load model
MODEL_PATH = 'models/waste_model_final(v1).h5'
model = load_model(MODEL_PATH)
# Load class indices if available
CLASS_INDICES_PATH = 'models/class_indices.json'
if os.path.exists(CLASS_INDICES_PATH):
	import json
	with open(CLASS_INDICES_PATH, 'r', encoding='utf-8') as f:
		class_indices = json.load(f)
	# invert to get index->name
	idx_to_class = {int(v): k for k, v in class_indices.items()}
else:
	idx_to_class = None


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def prepare_image(img_path, target_size=None):
	"""Load an image, convert to RGB, resize preserving aspect ratio and pad to model input size.

	Args:
		img_path: path to image file
		target_size: (height, width) tuple. If None, infer from model.input_shape.

	Returns:
		Numpy array of shape (1, H, W, 3) normalized to [0,1]
	"""
	# Open with PIL and ensure RGB
	img = Image.open(img_path)
	img = img.convert('RGB')

	# Infer target size from model if needed
	if target_size is None:
		try:
			# model.input_shape is typically (None, height, width, channels)
			_, h, w, _ = model.input_shape
			target_size = (h, w)
		except Exception:
			target_size = (224, 224)

	target_h, target_w = target_size
	orig_w, orig_h = img.size

	# Compute aspect-preserving resize
	ratio = min(target_w / orig_w, target_h / orig_h)
	new_w = max(1, int(orig_w * ratio))
	new_h = max(1, int(orig_h * ratio))
	img_resized = img.resize((new_w, new_h), Image.LANCZOS)

	# Create a new image and paste centered (pad with black)
	new_img = Image.new('RGB', (target_w, target_h), (0, 0, 0))
	paste_x = (target_w - new_w) // 2
	paste_y = (target_h - new_h) // 2
	new_img.paste(img_resized, (paste_x, paste_y))

	# Convert to array and normalize
	x = np.array(new_img).astype('float32') / 255.0
	x = np.expand_dims(x, axis=0)

	# Debug log (can be removed later)
	try:
		print(f"prepare_image: orig={(orig_w, orig_h)} resized={(new_w, new_h)} target={(target_h, target_w)}")
	except Exception:
		pass

	return x


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
	# handle camera image (base64) or uploaded file
	camera_data = request.form.get('camera_image')
	file = request.files.get('file')
	img_path = None
	if camera_data:
		# data URL -> save
		import base64, re
		m = re.match(r'data:image/(png|jpeg|jpg);base64,(.*)', camera_data)
		if not m:
			return 'Invalid image data', 400
		ext = m.group(1)
		data = m.group(2)
		binary = base64.b64decode(data)
		filename = secure_filename(f'cam_{int(np.random.randint(1e9))}.{ext}')
		img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		with open(img_path, 'wb') as f:
			f.write(binary)
	elif file:
		filename = secure_filename(file.filename)
		img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(img_path)
	else:
		return redirect(url_for('index'))

	# prepare and predict
	x = prepare_image(img_path, target_size=None)
	preds = model.predict(x)[0]
	top_idx = int(np.argmax(preds))
	confidence = float(preds[top_idx]) * 100.0
	if idx_to_class:
		predicted_class = idx_to_class.get(top_idx, str(top_idx))
	else:
		predicted_class = str(top_idx)

	image_url = '/' + img_path.replace('\\', '/')
	return render_template('result.html', image_url=image_url, predicted_class=predicted_class, confidence=f"{confidence:.2f}")


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)