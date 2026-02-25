import json
import sys
import os

# Add the project root to sys.path to allow importing app
sys.path.append(os.getcwd())

from app.services.resume_analysis_service import analyze_resume_text

def test_diversity():
    # 1. Java Backend Resume
    java_resume = """
    John Doe - Senior Java Developer
    Skills: Java, Spring Boot, Microservices, Hibernate, MySQL, Docker, Kubernetes, AWS.
    Experience: 5 years at Tech Corp.
    Projects: 
    - Migrated monolithic app to microservices using Spring Boot.
    - Optimized SQL queries reducing latency by 40%.
    - Implemented CI/CD pipelines with Jenkins.
    Education: Bachelor of Computer Science.
    """

    # 2. Python Data Scientist Resume
    python_resume = """
    Jane Smith - Data Scientist
    Skills: Python, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, SQL, FastAPI, Docker.
    Experience: 2 years at AI Labs.
    Projects:
    - Developed NLP model for sentiment analysis with 92% accuracy.
    - Built real-time prediction API using FastAPI.
    - Visualized complex datasets using Matplotlib and Seaborn.
    Education: Master of Science in Artificial Intelligence.
    """

    print("--- Analyzing Java Backend Resume ---")
    java_analysis = analyze_resume_text(java_resume)
    print(f"Strengths: {java_analysis['strengths']}")
    print(f"Weaknesses: {java_analysis['weaknesses']}")
    print(f"Suggestions: {java_analysis['suggestions']}")
    print("\n")

    print("--- Analyzing Python Data Scientist Resume ---")
    python_analysis = analyze_resume_text(python_resume)
    print(f"Strengths: {python_analysis['strengths']}")
    print(f"Weaknesses: {python_analysis['weaknesses']}")
    print(f"Suggestions: {python_analysis['suggestions']}")
    print("\n")

    # Basic diversity check
    strengths_overlap = set(java_analysis['strengths']).intersection(set(python_analysis['strengths']))
    suggestions_overlap = set(java_analysis['suggestions']).intersection(set(python_analysis['suggestions']))

    print(f"Strengths overlap: {len(strengths_overlap)}")
    print(f"Suggestions overlap: {len(suggestions_overlap)}")

    if len(suggestions_overlap) > 1:
        print("WARNING: High overlap in suggestions. Check prompt.")
    else:
        print("SUCCESS: Feedback appears diverse and resume-specific.")

if __name__ == "__main__":
    test_diversity()
