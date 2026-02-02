"""
Test the comprehensive skill extraction directly
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.resume_parser import extract_features

# Test with two different resumes
resume1 = """
Software Engineer
Skills: Python, Django, PostgreSQL, Docker, AWS, React
Experience: 5 years building web applications
"""

resume2 = """
Frontend Developer  
Skills: Angular, TypeScript, MongoDB, Azure, Vue.js, Node.js
Experience: 3 years in frontend development
"""

print("Testing Resume 1 (Python/Django stack):")
print("=" * 50)
features1 = extract_features(resume1)
print(f"Skills found: {features1['skills']}")
print(f"Count: {features1['skills_count']}")

print("\n\nTesting Resume 2 (Angular/TypeScript stack):")
print("=" * 50)
features2 = extract_features(resume2)
print(f"Skills found: {features2['skills']}")
print(f"Count: {features2['skills_count']}")

print("\n\nComparison:")
print("=" * 50)
if features1['skills'] == features2['skills']:
    print("❌ PROBLEM: Both resumes showing same skills!")
else:
    print("✅ SUCCESS: Different resumes showing different skills!")
