import argparse
import os
import sys
from pathlib import Path

import cv2

# Make `api` importable when running as a script
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.services.realtime_classifier import realtime_classifier  # noqa: E402
from api.services.classification_service import classification_service  # noqa: E402


def parse_args():
    default_model = ROOT / "models_improved" / "waste_model_improved_v1.h5"
    default_indices = ROOT / "models_improved" / "class_indices.json"
    parser = argparse.ArgumentParser(description="Real-time trash classifier using OpenCV + CNN.")
    parser.add_argument("--device", type=int, default=0, help="Camera device index (default: 0)")
    parser.add_argument("--model-path", type=str, default=str(default_model), help="Path to Keras model")
    parser.add_argument("--class-indices", type=str, default=str(default_indices), help="Path to class_indices.json")
    parser.add_argument("--window", type=str, default="Trash Classifier", help="OpenCV window name")
    return parser.parse_args()


def main():
    args = parse_args()

    # Override config for this process if provided
    os.environ["MODEL_PATH"] = args.model_path
    os.environ["CLASS_INDICES_PATH"] = args.class_indices

    print(f"Loading model from {args.model_path} ...")
    classification_service.reload_model()
    print("Model ready. Press 'q' to quit.")

    cap = cv2.VideoCapture(args.device)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video device {args.device}")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Failed to read frame; exiting.")
                break

            prediction = realtime_classifier.predict_frame(frame)

            label = prediction["waste_type"]
            conf = prediction["confidence_score"]
            text = f"{label} ({conf:.2f})"

            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            cv2.imshow(args.window, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

