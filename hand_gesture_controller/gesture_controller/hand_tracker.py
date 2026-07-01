import time
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarksConnections

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

HAND_CONNECTIONS = HandLandmarksConnections.HAND_CONNECTIONS


class HandTracker:
    """Wraps MediaPipe's HandLandmarker for use inside a webcam loop."""

    def __init__(self, model_path="hand_landmarker.task", num_hands=2,
                 min_hand_detection_confidence=0.6,
                 min_hand_presence_confidence=0.6,
                 min_tracking_confidence=0.6):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=min_hand_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.landmarker = HandLandmarker.create_from_options(options)

    def detect(self, rgb_frame):
        """Runs detection on an RGB frame and returns the first hand's
        21 landmarks (or None if no hand was detected)."""
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(time.time() * 1000)
        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.hand_landmarks:
            return result.hand_landmarks[0]
        return None

    def close(self):
        self.landmarker.close()
