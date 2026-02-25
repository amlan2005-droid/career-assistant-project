from app.services.cheating_rules import CheatingRulesEngine
import time

rules = CheatingRulesEngine()

print("---- TEST START ----")

# Simulate tab switch
rules.tab_switch_detected()

# Simulate face missing
rules.face_missing(seconds_missing=6.5)

# Simulate gaze away
rules.gaze_off_screen(duration=4)

# Simulate multiple faces
rules.multiple_faces_detected(face_count=2)

# Print final result
result = rules.summary()

print(result)
