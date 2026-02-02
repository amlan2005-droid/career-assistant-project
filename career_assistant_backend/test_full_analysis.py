"""
Simulate the full resume upload flow to see what's being returned
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.resume_analysis_service import analyze_resume_text

# Simulate two different resumes
resume_text_1 = """
John Doe
Senior Python Developer

Skills:
- Python, Django, Flask
- PostgreSQL, Redis
- Docker, Kubernetes
- AWS, Linux

Experience:
5 years building scalable web applications using Python and Django.
Deployed microservices on AWS using Docker and Kubernetes.
"""

resume_text_2 = """
Jane Smith  
Frontend Developer

Skills:
- Angular, TypeScript, Vue.js
- MongoDB, Node.js
- Azure, Git
- HTML, CSS, Bootstrap

Experience:
3 years developing modern web applications with Angular and TypeScript.
Built RESTful APIs with Node.js and MongoDB.
"""

print("Testing Resume 1 (Python Backend):")
print("=" * 60)
analysis1 = analyze_resume_text(resume_text_1)
print(f"Skills: {analysis1.get('skills', [])}")

print("\n\nTesting Resume 2 (Frontend):")
print("=" * 60)
analysis2 = analyze_resume_text(resume_text_2)
print(f"Skills: {analysis2.get('skills', [])}")

print("\n\nComparison:")
print("=" * 60)
if analysis1.get('skills') == analysis2.get('skills'):
    print("❌ PROBLEM: analyze_resume_text returning same skills!")
    print("This means there's an issue in the analysis function.")
else:
    print("✅ SUCCESS: analyze_resume_text returns different skills!")
    print("The backend is working correctly.")
