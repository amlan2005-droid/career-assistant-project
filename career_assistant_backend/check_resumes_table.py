"""
Check the resumes table for original uploaded files
"""
import sqlite3

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    print("=== RESUMES TABLE ===")
    cursor.execute("PRAGMA table_info(resumes)")
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    print("\n=== DATA ===")
    cursor.execute("SELECT id, user_id, filename, uploaded_at FROM resumes")
    rows = cursor.fetchall()
    
    if not rows:
        print("No resumes found")
    else:
        for row in rows:
            print(f"Resume ID: {row[0]}, User: {row[1]}, File: {row[2]}, Uploaded: {row[3]}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
