"""
Check resume_profiles table for skills data
"""
import sqlite3
import json

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    print("=== RESUME_PROFILES TABLE ===")
    cursor.execute("PRAGMA table_info(resume_profiles)")
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    print("\n=== DATA ===")
    cursor.execute("SELECT * FROM resume_profiles")
    rows = cursor.fetchall()
    
    if not rows:
        print("No data found")
    else:
        for row in rows:
            print(f"\nUser ID: {row[1]}")
            # Assuming skills is in JSON format
            if len(row) > 2 and row[2]:
                try:
                    skills = json.loads(row[2]) if isinstance(row[2], str) else row[2]
                    print(f"  Skills: {skills}")
                except:
                    print(f"  Skills (raw): {row[2]}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
