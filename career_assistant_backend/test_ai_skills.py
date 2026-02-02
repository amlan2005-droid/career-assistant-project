"""
Test the AI skill extraction directly
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.reasoning_service import extract_skills_with_ai

# Test with sample resume text
test_resume = """
John Doe
Software Engineer

Skills:
- Python, JavaScript, TypeScript
- React, Angular, Vue.js
- Node.js, Express
- MongoDB, PostgreSQL, Redis
- Docker, Kubernetes, AWS
- Git, CI/CD, Jenkins

Experience:
5 years of experience in full-stack development
Built scalable microservices using Spring Boot and Django
"""

print("Testing AI skill extraction...")
print("=" * 50)

try:
    skills = extract_skills_with_ai(test_resume)
    print(f"✅ Extracted {len(skills)} skills:")
    for skill in skills:
        print(f"  - {skill}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
