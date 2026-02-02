"""
Migration script to add achievement_density column to resume_analysis table
"""
import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    # Check if column exists
    cursor.execute("PRAGMA table_info(resume_analysis)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'achievement_density' not in columns:
        print("Adding achievement_density column to resume_analysis table...")
        # Add the column with a default value (empty JSON object)
        cursor.execute("""
            ALTER TABLE resume_analysis 
            ADD COLUMN achievement_density TEXT DEFAULT '{}'
        """)
        conn.commit()
        print("✅ Column added successfully!")
    else:
        print("✅ Column already exists!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()
