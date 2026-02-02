"""
Verification script for skill insights integration
"""
import sys
import os
import json
import sqlite3

# Add backend to path
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.resume_analysis_service import analyze_resume_text

def test_analysis_skill_insights():
    print("Testing analyze_resume_text for skill_insights...")
    
    test_resume = """
    Software Engineer with experience in Python, FastAPI, and Docker.
    Developed multiple microservices using Python and FastAPI.
    Used Docker for containerization and deployment.
    Mentions Python multiple times to ensure high confidence.
    Python, Python, Python.
    """
    
    analysis = analyze_resume_text(test_resume)
    
    if "skill_insights" in analysis:
        print("✅ skill_insights found in analysis")
        insights = analysis["skill_insights"]
        print(f"Number of insights: {len(insights)}")
        for i in insights[:3]:
            print(f"  - {i['name']}: {i['confidence']:.2f} ({i['level']})")
    else:
        print("❌ skill_insights NOT found in analysis")

def test_db_storage():
    print("\nTesting DB storage...")
    DB_PATH = "c:/Users/DELL/career_assistant_project/career_assistant_backend/career.db"
    
    if not os.path.exists(DB_PATH):
        print(f"❌ DB not found at {DB_PATH}")
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("PRAGMA table_info(resume_analysis)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'skill_insights' in columns:
            print("✅ Column 'skill_insights' exists in DB")
        else:
            print("❌ Column 'skill_insights' MISSING in DB")
    finally:
        conn.close()

if __name__ == "__main__":
    test_analysis_skill_insights()
    test_db_storage()
