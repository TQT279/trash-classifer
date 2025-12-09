## Realtime Classification Endpoint

- Ensure environment paths (or defaults) point to the improved model:
  - `MODEL_PATH=models_improved/waste_model_improved_v1.h5`
  - `CLASS_INDICES_PATH=models_improved/class_indices.json`

### Request Examples

**Capture from server webcam (if available)**
```
POST /api/realtime/capture
Authorization: Bearer <access_token>
```
(Optional) `device_index` form/query param to pick a camera.

**Send a frame from client**
```
POST /api/realtime/capture
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
image: <jpeg/png frame>
```

Response payload:
```
{
  "success": true,
  "data": {
    "prediction": {
      "waste_type": "plastic",
      "confidence_score": 0.92,
      "timestamp": "2025-01-01T00:00:00Z",
      "all_predictions": { "...": 0.0 },
      "processing_time_ms": 45
    }
  }
}
```

