"""
Migration script to populate domains for existing resume insights
This script will:
1. Read skills from resume_analysis table
2. Infer domains using the new infer_domains_from_skills function
3. Update resume_insights table with the inferred domains
"""
import sqlite3
import json

def infer_domains_from_skills(skills):
    """
    Infer domains from skills using pattern matching.
    """
    if not skills:
        return []
    
    # Convert to lowercase for matching
    skills_lower = [s.lower() for s in skills]
    domains = set()

    java = {"java", "spring", "spring boot", "jdbc", "hibernate"}
    python = {"python", "fastapi", "django", "flask"}
    devops = {"docker", "kubernetes", "ci/cd", "jenkins", "aws"}
    ml = {"machine learning", "deep learning", "nlp"}

    if any(s in skills_lower for s in java):
        domains.add("java-backend")

    if any(s in skills_lower for s in python):
        domains.add("python-backend")

    if any(s in skills_lower for s in devops):
        domains.add("devops")

    if any(s in skills_lower for s in ml):
        domains.add("machine-learning")

    return list(domains)


# Connect to the database
conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    print("=== Migrating Resume Insights ===\n")
    
    # Get all users with resume analysis
    cursor.execute("""
        SELECT user_id, skills 
        FROM resume_analysis
    """)
    
    resume_data = cursor.fetchall()
    
    if not resume_data:
        print("❌ No resume analysis found")
    else:
        for user_id, skills_json in resume_data:
            # Parse skills JSON
            skills = json.loads(skills_json) if skills_json else []
            
            # Infer domains
            domains = infer_domains_from_skills(skills)
            
            print(f"User ID {user_id}:")
            print(f"  Skills: {skills[:5]}..." if len(skills) > 5 else f"  Skills: {skills}")
            print(f"  Inferred Domains: {domains}")
            
            # Update resume_insights table
            cursor.execute("""
                UPDATE resume_insights 
                SET domains = ?, skills = ?
                WHERE user_id = ?
            """, (",".join(domains), ",".join(skills), user_id))
            
            print(f"  ✅ Updated!\n")
        
        conn.commit()
        print(f"✅ Successfully migrated {len(resume_data)} records")
        
        # Verify the update
        print("\n=== Verification ===")
        cursor.execute("SELECT user_id, domains FROM resume_insights")
        for row in cursor.fetchall():
            print(f"User {row[0]}: {row[1]}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
