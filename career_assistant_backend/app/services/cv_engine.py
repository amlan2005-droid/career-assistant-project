import cv2
import numpy as np
import base64
import logging
from typing import Dict, List, Optional, TypedDict
from enum import Enum

# Configure logging
logger = logging.getLogger(__name__)

# ---------------------------
# Load Haar Cascade models
# ---------------------------
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

EYE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)


class CVStatus(Enum):
    OK = "OK"
    NO_FACE = "NO_FACE"
    MULTIPLE_FACES = "MULTIPLE_FACES"
    EYES_NOT_DETECTED = "EYES_NOT_DETECTED"
    INVALID_FRAME = "INVALID_FRAME"


class CVResult(TypedDict):
    status: str
    meta: Dict


class CVEngine:
    """
    OpenCV Engine for Interview Monitoring
    - Face detection
    - Multiple face detection
    - Eye detection (basic attention check)
    """

    def __init__(self):
        self.no_face_counter = 0

    # ---------------------------
    # Decode base64 image
    # ---------------------------
    def decode_base64_image(self, base64_str: str) -> Optional[np.ndarray]:
        """
        Converts base64 image string to OpenCV image
        """
        try:
            if not base64_str:
                return None
            
            # Remove header if present
            if "," in base64_str:
                base64_str = base64_str.split(",")[-1]
                
            image_bytes = base64.b64decode(base64_str)
            np_arr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            logger.error(f"Error decoding base64 image: {str(e)}")
            return None

    # ---------------------------
    # Analyze a single frame
    # ---------------------------
    def analyze_frame(self, base64_frame: str) -> CVResult:
        """
        Analyze webcam frame and return cheating signals
        """

        image = self.decode_base64_image(base64_frame)
        if image is None:
            return self._result(CVStatus.INVALID_FRAME)

        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = FACE_CASCADE.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(80, 80)
            )

            # ---------- No face detected ----------
            if len(faces) == 0:
                self.no_face_counter += 1
                return self._result(
                    CVStatus.NO_FACE,
                    meta={"no_face_frames": self.no_face_counter}
                )

            # Reset counter if face is back
            self.no_face_counter = 0

            # ---------- Multiple faces ----------
            if len(faces) > 1:
                return self._result(
                    CVStatus.MULTIPLE_FACES,
                    meta={"face_count": len(faces)}
                )

            # ---------- Eye detection (attention) ----------
            (x, y, w, h) = faces[0]
            face_roi = gray[y:y + h, x:x + w]

            eyes = EYE_CASCADE.detectMultiScale(
                face_roi,
                scaleFactor=1.1,
                minNeighbors=2,
                minSize=(20, 20)
            )

            if len(eyes) < 1:
                return self._result(CVStatus.EYES_NOT_DETECTED)

            # ---------- All good ----------
            return self._result(
                CVStatus.OK,
                meta={
                    "faces": 1,
                    "eyes": len(eyes)
                }
            )
        except Exception as e:
            logger.error(f"Error analyzing frame: {str(e)}")
            return self._result(CVStatus.INVALID_FRAME, meta={"error": str(e)})

    # ---------------------------
    # Standard result format
    # ---------------------------
    def _result(self, status: CVStatus, meta: Optional[Dict] = None) -> CVResult:
        return {
            "status": status.value,
            "meta": meta or {}
        }
