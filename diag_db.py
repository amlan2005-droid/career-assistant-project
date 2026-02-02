import sqlite3
import os
import json

DB_PATH = r"C:\Users\DELL\career_assistant_project\career_assistant_backend\career.db"

def check_db():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- Database Diagnostic ---")
    
    # Check users
    cursor.execute("SELECT id, email, username FROM users")
    users = cursor.fetchall()
    print(f"\nTotal Users: {len(users)}")
    for u in users:
        print(f"  - User: {u[0]} | {u[1]} | {u[2]}")

    # Check resume_analysis
    try:
        cursor.execute("SELECT id, user_id, domains, skill_insights FROM resume_analysis ORDER BY created_at DESC")
        analyses = cursor.fetchall()
        print(f"\nTotal Resume Analyses: {len(analyses)}")
        for a in analyses:
            domains = a[2]
            insights = a[3]
            print(f"  - ID: {a[0]} | UserID: {a[1]} | Domains: {domains}")
            if insights:
                try:
                    ins_data = json.loads(insights) if isinstance(insights, str) else insights
                    print(f"    Insights count: {len(ins_data) if ins_data else 0}")
                except:
                    print(f"    Insights (raw): {len(str(insights))} chars")
            else:
                print("    ❌ No skill_insights")
    except Exception as e:
        print(f"❌ Error checking resume_analysis: {e}")

    conn.close()

if __name__ == "__main__":
    check_db()
