"""
Diagnostic script to check all resume-related tables
"""
import sqlite3
import json

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    print("=== RESUME ANALYSIS TABLE ===")
    cursor.execute("SELECT user_id, skills, domains FROM resume_analysis")
    rows = cursor.fetchall()
    for row in rows:
        skills = json.loads(row[1]) if row[1] else []
        domains = json.loads(row[2]) if row[2] else []
        print(f"User {row[0]}:")
        print(f"  Skills: {skills}")
        print(f"  Domains: {domains}\n")
    
    print("\n=== RESUME PROFILE TABLE ===")
    cursor.execute("SELECT user_id, skills FROM resume_profile")
    rows = cursor.fetchall()
    for row in rows:
        skills = json.loads(row[1]) if row[1] else []
        print(f"User {row[0]}:")
        print(f"  Skills: {skills}\n")
    
    print("\n=== RESUME INSIGHTS TABLE ===")
    cursor.execute("SELECT user_id, skills, domains FROM resume_insights")
    rows = cursor.fetchall()
    for row in rows:
        print(f"User {row[0]}:")
        print(f"  Skills: {row[1]}")
        print(f"  Domains: {row[2]}\n")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
