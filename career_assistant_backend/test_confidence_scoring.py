"""
Test the new confidence-based skill extraction
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.resume_parser import extract_features

# DevOps resume - mentions FastAPI once but Docker/AWS many times
devops_resume = """
AWS Certified DevOps Engineer

Skills:
- AWS, Docker, Kubernetes, Terraform
- CI/CD with Jenkins and GitLab
- Infrastructure as Code
- Monitoring with CloudWatch

Experience:
- Deployed microservices on AWS using Docker and Kubernetes
- Built CI/CD pipelines with Jenkins for FastAPI applications
- Managed AWS infrastructure with Terraform
- Implemented monitoring and alerting with AWS CloudWatch
- Automated deployments using Docker containers
- Configured Kubernetes clusters on AWS EKS
"""

# Backend resume - mentions Docker once but Python/Django many times
backend_resume = """
Senior Python Backend Developer

Skills:
- Python, Django, FastAPI, Flask
- PostgreSQL, Redis, MongoDB
- REST API design
- Microservices architecture

Experience:
- Built scalable REST APIs with Django and FastAPI
- Designed database schemas in PostgreSQL
- Implemented caching with Redis
- Developed microservices with FastAPI
- Optimized Python code for performance
- Integrated third-party APIs with Python
- Deployed applications using Docker
"""

print("=" * 70)
print("DEVOPS RESUME")
print("=" * 70)
features1 = extract_features(devops_resume)
print(f"\n✅ PRIMARY SKILLS: {features1['skills']}")
print(f"📊 All skills found: {features1['all_skills']}")

print("\n" + "=" * 70)
print("BACKEND RESUME")
print("=" * 70)
features2 = extract_features(backend_resume)
print(f"\n✅ PRIMARY SKILLS: {features2['skills']}")
print(f"📊 All skills found: {features2['all_skills']}")

print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"DevOps primary: {set(features1['skills'])}")
print(f"Backend primary: {set(features2['skills'])}")
print(f"\n✅ Different primary skills: {set(features1['skills']) != set(features2['skills'])}")
