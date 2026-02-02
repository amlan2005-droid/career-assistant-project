"""
Check what's actually in the database after our fixes
"""
import sqlite3
import json

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    print("=== RESUME ANALYSIS TABLE ===")
    cursor.execute("SELECT user_id, skills, domains FROM resume_analysis")
    rows = cursor.fetchall()
    if not rows:
        print("No data found\n")
    else:
        for row in rows:
            skills = json.loads(row[1]) if row[1] else []
            domains = json.loads(row[2]) if row[2] else []
            print(f"User {row[0]}:")
            print(f"  Skills ({len(skills)}): {skills[:3]}..." if len(skills) > 3 else f"  Skills: {skills}")
            print(f"  Domains: {domains}\n")
    
    print("=== RESUME INSIGHTS TABLE ===")
    cursor.execute("SELECT user_id, skills, domains FROM resume_insights")
    rows = cursor.fetchall()
    if not rows:
        print("No data found\n")
    else:
        for row in rows:
            print(f"User {row[0]}:")
            print(f"  Skills: {row[1]}")
            print(f"  Domains: {row[2]}\n")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
