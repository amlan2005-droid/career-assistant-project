"""
Direct test with actual AWS DevOps resume content
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.resume_analysis_service import analyze_resume_text

# Simulate AWS DevOps resume text
aws_devops_text = """
AWS Certified DevOps Engineer

Professional Summary:
Experienced DevOps Engineer with AWS certification and expertise in cloud infrastructure,
containerization, and CI/CD automation.

Technical Skills:
- Cloud Platforms: AWS (EC2, S3, RDS, Lambda, CloudFormation)
- Containerization: Docker, Kubernetes, ECS
- CI/CD: Jenkins, GitLab CI, AWS CodePipeline
- Infrastructure as Code: Terraform, CloudFormation, Ansible
- Monitoring: CloudWatch, Prometheus, Grafana
- Version Control: Git, GitHub

Professional Experience:

Senior DevOps Engineer | Tech Corp | 2020-Present
- Designed and implemented AWS infrastructure using Terraform
- Built CI/CD pipelines with Jenkins for microservices deployment
- Managed Kubernetes clusters on AWS EKS
- Automated infrastructure provisioning with Terraform and Ansible
- Implemented monitoring and alerting using CloudWatch and Prometheus
- Reduced deployment time by 60% through automation
- Managed Docker containers across multiple AWS regions

DevOps Engineer | StartupCo | 2018-2020
- Deployed applications on AWS using Docker and Kubernetes
- Created CI/CD workflows with GitLab CI
- Configured AWS infrastructure with CloudFormation
- Implemented automated testing in CI/CD pipelines

Education:
Bachelor of Science in Computer Science

Certifications:
- AWS Certified DevOps Engineer - Professional
- Certified Kubernetes Administrator (CKA)
"""

print("=" * 70)
print("TESTING AWS DEVOPS RESUME")
print("=" * 70)

analysis = analyze_resume_text(aws_devops_text)

print(f"\n✅ SKILLS EXTRACTED: {analysis['skills']}")
print(f"\n📊 Skills count: {len(analysis['skills'])}")
print(f"📊 Experience: {analysis.get('experience_years', 0)} years")
print(f"📊 Resume score: {analysis.get('resume_score', 0)}/100")
