"""
Final fix: Populate domains from existing skills in resume_profiles
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

import sqlite3
import json
from app.services.resume_analysis_service import infer_domains_from_skills

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    print("=== Populating Domains from Existing Skills ===\n")
    
    # Get skills from resume_profiles
    cursor.execute("SELECT user_id, skills FROM resume_profiles WHERE skills IS NOT NULL")
    profiles = cursor.fetchall()
    
    if not profiles:
        print("❌ No resume profiles found")
    else:
        for user_id, skills_json in profiles:
            # Parse skills
            try:
                skills = json.loads(skills_json) if isinstance(skills_json, str) else skills_json
                if not skills or len(skills) == 0:
                    print(f"User {user_id}: No skills found, skipping")
                    continue
            except:
                print(f"User {user_id}: Error parsing skills, skipping")
                continue
            
            # Infer domains
            domains = infer_domains_from_skills(skills)
            
            print(f"User {user_id}:")
            print(f"  Skills ({len(skills)}): {skills[:5]}..." if len(skills) > 5 else f"  Skills: {skills}")
            print(f"  Inferred Domains: {domains}")
            
            # Update resume_insights table
            cursor.execute("""
                UPDATE resume_insights 
                SET domains = ?, skills = ?
                WHERE user_id = ?
            """, (",".join(domains), ",".join(skills), user_id))
            
            # Also update resume_analysis table
            cursor.execute("""
                UPDATE resume_analysis 
                SET domains = ?, skills = ?
                WHERE user_id = ?
            """, (json.dumps(domains), json.dumps(skills), user_id))
            
            print(f"  ✅ Updated both tables!\n")
        
        conn.commit()
        print(f"\n✅ Successfully processed {len(profiles)} users")
        
        # Verify
        print("\n=== VERIFICATION ===")
        cursor.execute("SELECT user_id, domains, skills FROM resume_insights")
        for row in cursor.fetchall():
            skills_list = row[2].split(",") if row[2] else []
            print(f"User {row[0]}:")
            print(f"  Domains: {row[1]}")
            print(f"  Skills count: {len(skills_list)}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()
