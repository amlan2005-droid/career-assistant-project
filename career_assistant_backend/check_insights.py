"""
Script to check and update existing resume insights with proper domains
"""
import sqlite3

# Connect to the database
conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    # Check current state of resume_insights table
    print("=== Current Resume Insights ===")
    cursor.execute("SELECT id, user_id, domains, skills FROM resume_insights")
    rows = cursor.fetchall()
    
    if not rows:
        print("❌ No resume insights found in database")
    else:
        for row in rows:
            print(f"ID: {row[0]}, User ID: {row[1]}")
            print(f"  Domains: {row[2]}")
            print(f"  Skills: {row[3]}")
            print()
    
    print(f"Total records: {len(rows)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    conn.close()
