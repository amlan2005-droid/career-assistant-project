"""
Check ALL columns in resume_analysis table
"""
import sqlite3

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    # Get table schema
    cursor.execute("PRAGMA table_info(resume_analysis)")
    columns = cursor.fetchall()
    print("=== RESUME_ANALYSIS TABLE SCHEMA ===")
    for col in columns:
        print(f"{col[1]} ({col[2]})")
    
    print("\n=== RESUME_ANALYSIS DATA ===")
    cursor.execute("SELECT * FROM resume_analysis")
    rows = cursor.fetchall()
    
    if not rows:
        print("No data found")
    else:
        col_names = [col[1] for col in columns]
        for row in rows:
            print(f"\nUser ID: {row[1]}")
            for i, col_name in enumerate(col_names):
                value = row[i]
                if isinstance(value, str) and len(value) > 100:
                    print(f"  {col_name}: {value[:100]}...")
                else:
                    print(f"  {col_name}: {value}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
