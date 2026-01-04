import os
import json
import time
import numpy as np
from PIL import Image
import tensorflow as tf
from flask import current_app
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input # type: ignore
from tensorflow.keras.preprocessing.image import img_to_array # type: ignore


def focal_loss(gamma=1.0, alpha=0.25):
    """Recreate the custom focal loss from training for model loading."""
    def focal_loss_fn(y_true, y_pred):
        epsilon = tf.keras.backend.epsilon()
        y_pred = tf.clip_by_value(y_pred, epsilon, 1. - epsilon)

        cross_entropy = -y_true * tf.math.log(y_pred)
        weight = alpha * y_true * tf.pow((1 - y_pred), gamma)
        focal_cross_entropy = weight * cross_entropy
        focal_cross_entropy = tf.reduce_sum(focal_cross_entropy, axis=1)

        return tf.reduce_mean(focal_cross_entropy)

    return focal_loss_fn


class ClassificationService:
    """Service for waste classification using TensorFlow model"""
    
    def __init__(self):
        self.model = None
        self.class_indices = None
        self.index_to_class = None
        self.model_version = 'v1.0'
        self._model_loaded = False
        # Default input size used during training; keep exported for reuse
        self.input_size = (224, 224)
    
    def _ensure_model_loaded(self):
        """Ensure model is loaded (lazy loading)"""
        if self._model_loaded and self.model is not None:
            return
        
        try:
            from flask import has_app_context
            if not has_app_context():
                raise Exception("Flask application context required")
            # Get paths from config with sensible fallbacks to models_improved
            model_path = current_app.config.get('MODEL_PATH', 'models_improved/waste_model_improved_v1.h5')
            class_indices_path = current_app.config.get('CLASS_INDICES_PATH', 'models_improved/class_indices.json')
            
            # Convert relative paths to absolute if needed
            # Get project root (3 levels up from api/services/classification_service.py)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            
            if not os.path.isabs(model_path):
                # Handle relative paths like '../models/best_model.h5'
                if model_path.startswith('../'):
                    model_path = os.path.join(project_root, model_path.replace('../', '', 1))
                else:
                    model_path = os.path.join(project_root, model_path)
            
            if not os.path.isabs(class_indices_path):
                # Handle relative paths like '../models/class_indices.json'
                if class_indices_path.startswith('../'):
                    class_indices_path = os.path.join(project_root, class_indices_path.replace('../', '', 1))
                else:
                    class_indices_path = os.path.join(project_root, class_indices_path)
            
            # Load model with custom objects (focal loss) used during training
            if os.path.exists(model_path):
                custom_objects = {
                    'focal_loss_fn': focal_loss(gamma=1.0, alpha=0.25)
                }
                self.model = tf.keras.models.load_model(
                    model_path,
                    custom_objects=custom_objects,
                    compile=False
                )
                current_app.logger.info(f"Model loaded from {model_path}")
            else:
                current_app.logger.warning(f"Model file not found at {model_path}")
                return
            
            # Load class indices
            if os.path.exists(class_indices_path):
                with open(class_indices_path, 'r') as f:
                    self.class_indices = json.load(f)
                # Create reverse mapping (index -> class name)
                self.index_to_class = {v: k for k, v in self.class_indices.items()}
                current_app.logger.info(f"Class indices loaded from {class_indices_path}")
                self._model_loaded = True
            else:
                current_app.logger.warning(f"Class indices file not found at {class_indices_path}")
                self._model_loaded = False
                
        except Exception as e:
            current_app.logger.error(f"Error loading model: {str(e)}")
            self.model = None
            self._model_loaded = False
    
    def _load_model(self):
        """Load the TensorFlow model and class indices"""
        self._ensure_model_loaded()
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for model prediction
        Args:
            image_path: Path to the image file
        Returns:
            Preprocessed image array ready for model input
        """
        try:
            # Load and resize image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to model input size (typically 224x224 for most models)
            img = img.resize(self.input_size)
            
            # (# Convert to array and normalize
            # img_array = np.array(img) / 255.0)
            
            # Convert image to array
            img_array = img_to_array(img)
            
            # Convert to array and normalize
            img_array = preprocess_input(img_array)
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            current_app.logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def predict(self, image_path):
        """
        Predict waste type from image
        Args:
            image_path: Path to the image file
        Returns:
            dict with 'waste_type', 'confidence_score', 'all_predictions', 'processing_time_ms'
        """
        self._ensure_model_loaded()
        
        if self.model is None:
            raise Exception("Model not loaded")
        
        start_time = time.time()
        
        try:
            # Preprocess image
            img_array = self.preprocess_image(image_path)
            
            # Make prediction
            predictions = self.model.predict(img_array, verbose=0)
            
            # Get top prediction
            predicted_index = np.argmax(predictions[0])
            confidence_score = float(predictions[0][predicted_index])
            
            # Get class name
            waste_type_name = self.index_to_class.get(predicted_index, 'unknown')
            
            # Get all predictions for debugging/analysis
            all_predictions = {}
            for idx, prob in enumerate(predictions[0]):
                class_name = self.index_to_class.get(idx, 'unknown')
                all_predictions[class_name] = float(prob)
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            return {
                'waste_type': waste_type_name,
                'confidence_score': confidence_score,
                'all_predictions': all_predictions,
                'processing_time_ms': processing_time_ms,
                'model_version': self.model_version
            }
        except Exception as e:
            current_app.logger.error(f"Error during prediction: {str(e)}")
            raise
    
    def reload_model(self):
        """Reload the model (useful for model updates)"""
        self._model_loaded = False
        self.model = None
        self.class_indices = None
        self.index_to_class = None
        self._ensure_model_loaded()

    def get_model_and_classes(self):
        """
        Ensure model is loaded and return model plus index->class mapping.
        Returns:
            tuple: (model, index_to_class)
        """
        self._ensure_model_loaded()
        return self.model, self.index_to_class


# Global instance
classification_service = ClassificationService()

