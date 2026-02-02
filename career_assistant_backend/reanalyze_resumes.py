"""
Re-analyze existing resume to populate domains
This script will:
1. Get the resume text from resume_analysis table
2. Re-analyze it to extract skills
3. Infer domains from skills
4. Update both resume_analysis and resume_insights tables
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

import sqlite3
import json
from app.services.resume_analysis_service import analyze_resume_text, infer_domains_from_skills

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    print("=== Re-analyzing Existing Resumes ===\n")
    
    # Get all users with resume_analysis but empty skills
    cursor.execute("""
        SELECT user_id, resume_text 
        FROM resume_analysis
        WHERE resume_text IS NOT NULL AND resume_text != ''
    """)
    
    resumes = cursor.fetchall()
    
    if not resumes:
        print("❌ No resumes found to re-analyze")
    else:
        for user_id, resume_text in resumes:
            print(f"Processing User ID {user_id}...")
            
            if not resume_text or len(resume_text.strip()) < 50:
                print(f"  ⚠️  Resume text too short, skipping\n")
                continue
            
            # Re-analyze the resume
            analysis = analyze_resume_text(resume_text)
            
            skills = analysis.get("skills", [])
            domains = infer_domains_from_skills(skills)
            
            print(f"  Found {len(skills)} skills")
            print(f"  Skills: {skills[:5]}..." if len(skills) > 5 else f"  Skills: {skills}")
            print(f"  Inferred Domains: {domains}")
            
            # Update resume_analysis table
            cursor.execute("""
                UPDATE resume_analysis 
                SET skills = ?, domains = ?
                WHERE user_id = ?
            """, (json.dumps(skills), json.dumps(domains), user_id))
            
            # Update resume_insights table
            cursor.execute("""
                UPDATE resume_insights 
                SET skills = ?, domains = ?
                WHERE user_id = ?
            """, (",".join(skills), ",".join(domains), user_id))
            
            print(f"  ✅ Updated!\n")
        
        conn.commit()
        print(f"✅ Successfully re-analyzed {len(resumes)} resumes")
        
        # Verify
        print("\n=== Verification ===")
        cursor.execute("SELECT user_id, domains FROM resume_insights")
        for row in cursor.fetchall():
            print(f"User {row[0]}: {row[1]}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()
