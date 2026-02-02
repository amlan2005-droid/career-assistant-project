"""
Database Migration Script - Add skill_insights column to resume_analysis table
"""

import sqlite3
import os

# Database path - relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "career.db")

def migrate():
    """Add skill_insights column to resume_analysis table if it doesn't exist."""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(resume_analysis)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'skill_insights' in columns:
            print("✅ Column 'skill_insights' already exists in resume_analysis table")
        else:
            # Add the skill_insights column
            print("Adding 'skill_insights' column to resume_analysis table...")
            cursor.execute("ALTER TABLE resume_analysis ADD COLUMN skill_insights JSON")
            conn.commit()
            print("✅ Successfully added 'skill_insights' column")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
