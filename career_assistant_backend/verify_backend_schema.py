"""
Verify that analyze_resume_text returns the keys expected by the frontend.
"""
import sys
import os

# Add the backend directory to path
sys.path.insert(0, os.path.abspath('.'))

from app.services.resume_analysis_service import analyze_resume_text

test_text = "Experienced Python developer with skills in FastAPI, React, and SQL. 5 years of experience."

print("Analyzing test text...")
result = analyze_resume_text(test_text)

# Keys expected by the frontend (based on ResumeUpload.jsx)
expected_keys = ["score", "skills_found", "education", "experience_years"]

print("\nVerifying keys in response:")
print("-" * 30)
missing_keys = []
for key in expected_keys:
    if key in result:
        print(f"✅ Key '{key}' is present")
    else:
        print(f"❌ Key '{key}' is MISSING")
        missing_keys.append(key)

if not missing_keys:
    print("\n✅ Verification SUCCESS: All expected keys are present in the response.")
else:
    print(f"\n❌ Verification FAILED: Missing keys {missing_keys}")
    sys.exit(1)

# Check a sample of values
print("\nSample values:")
print(f"Score: {result.get('score')}")
print(f"Skills Found: {result.get('skills_found')}")
print(f"Education: {result.get('education')}")
print(f"Experience Years: {result.get('experience_years')}")
