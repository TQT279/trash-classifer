import os
import time
from datetime import datetime

import cv2
import numpy as np
from flask import current_app

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input  # type: ignore
from .classification_service import classification_service


class RealtimeClassifier:
    """
    OpenCV-powered real-time classifier that reuses the loaded Keras model
    from classification_service. Provides helpers to classify live frames or
    one-off captures.
    """

    def __init__(self, device_index=0):
        self.device_index = device_index

    def _ensure_model(self):
        model, index_to_class = classification_service.get_model_and_classes()
        if model is None or index_to_class is None:
            raise RuntimeError("Model not loaded; check MODEL_PATH and CLASS_INDICES_PATH.")
        return model, index_to_class

    def _preprocess_frame(self, frame):
        """
        Convert raw BGR frame to normalized model input.
        """
        # Convert BGR (OpenCV default) to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Resize to training input size
        target_size = classification_service.input_size
        resized = cv2.resize(rgb, target_size)
        # (# Normalize to 0-1 and add batch dim
        # normalized = resized.astype("float32") / 255.0)
        # Chuyển sang float để tính toán
        img_array = resized.astype("float32")
        # Dùng hàm của MobileNetV2 để đưa về [-1, 1]
        normalized = preprocess_input(img_array)
        return np.expand_dims(normalized, axis=0)

    def predict_frame(self, frame):
        """
        Run prediction on an in-memory frame (numpy array from OpenCV).
        Returns a dict with prediction metadata.
        """
        model, index_to_class = self._ensure_model()
        start_time = time.time()

        input_tensor = self._preprocess_frame(frame)
        predictions = model.predict(input_tensor, verbose=0)

        predicted_index = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_index])
        label = index_to_class.get(predicted_index, "unknown")

        all_predictions = {
            index_to_class.get(i, "unknown"): float(prob)
            for i, prob in enumerate(predictions[0])
        }

        return {
            "waste_type": label,
            "confidence_score": confidence,
            "all_predictions": all_predictions,
            "processing_time_ms": int((time.time() - start_time) * 1000),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model_version": classification_service.model_version,
        }

    def capture_and_predict(self, device_index=None):
        """
        Capture a single frame from a webcam/video device and predict.
        """
        index = self.device_index if device_index is None else device_index
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video device {index}")

        try:
            success, frame = cap.read()
            if not success or frame is None:
                raise RuntimeError("Failed to capture frame from device.")
            return self.predict_frame(frame)
        finally:
            cap.release()


# Global instance
realtime_classifier = RealtimeClassifier()

