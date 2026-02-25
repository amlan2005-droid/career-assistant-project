import base64
import numpy as np
import cv2
from app.services.cv_engine import CVEngine, CVStatus

def test_cv_engine():
    cv = CVEngine()
    print("---- CV ENGINE TEST START ----")

    # 1. Test invalid frame
    print("\n[Test 1] Invalid Frame")
    res1 = cv.analyze_frame("invalid_base64_data")
    print(f"Result: {res1}")
    assert res1["status"] == CVStatus.INVALID_FRAME.value

    # 2. Test valid image but no face (black image)
    print("\n[Test 2] Valid Image, No Face")
    # Create a black 100x100 image
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    _, buffer = cv2.imencode(".jpg", img)
    b64_img = base64.b64encode(buffer).decode("utf-8")
    
    res2 = cv.analyze_frame(b64_img)
    print(f"Result: {res2}")
    assert res2["status"] == CVStatus.NO_FACE.value
    assert res2["meta"]["no_face_frames"] == 1

    # 3. Test counter increment
    print("\n[Test 3] Face Missing Counter")
    res3 = cv.analyze_frame(b64_img)
    print(f"Result: {res3}")
    assert res3["meta"]["no_face_frames"] == 2

    print("\n---- CV ENGINE TEST PASSED ----")

if __name__ == "__main__":
    test_cv_engine()
