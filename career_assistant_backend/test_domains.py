"""
Test script to verify the domain inference is working
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.resume_analysis_service import infer_domains_from_skills

# Test cases
test_skills = [
    ["Python", "FastAPI", "Django"],
    ["Java", "Spring Boot", "Hibernate"],
    ["Docker", "Kubernetes", "AWS"],
    ["Machine Learning", "Deep Learning", "NLP"],
    ["Python", "Docker", "Machine Learning"],
    []
]

print("=== Testing infer_domains_from_skills() ===\n")

for skills in test_skills:
    domains = infer_domains_from_skills(skills)
    print(f"Skills: {skills}")
    print(f"Domains: {domains}")
    print()
