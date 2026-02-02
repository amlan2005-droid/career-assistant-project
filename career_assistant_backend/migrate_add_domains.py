"""
Database Migration Script - Add domains column to resume_analysis table

Run this script to add the missing 'domains' column to the resume_analysis table.
This fixes the error: "no such column: resume_analysis.domains"

Usage:
    python migrate_add_domains.py
"""

import sqlite3
import os

# Database path
DB_PATH = "career.db"

def migrate():
    """Add domains column to resume_analysis table if it doesn't exist."""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        print("The database will be created automatically when you start the server.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if domains column already exists
        cursor.execute("PRAGMA table_info(resume_analysis)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'domains' in columns:
            print("✅ Column 'domains' already exists in resume_analysis table")
        else:
            # Add the domains column
            print("Adding 'domains' column to resume_analysis table...")
            cursor.execute("ALTER TABLE resume_analysis ADD COLUMN domains TEXT")
            conn.commit()
            print("✅ Successfully added 'domains' column")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(resume_analysis)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"\nCurrent columns in resume_analysis: {', '.join(columns)}")
        
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print("❌ Table 'resume_analysis' does not exist yet")
            print("The table will be created when you start the server")
        else:
            print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add domains column")
    print("=" * 60)
    migrate()
    print("\n✅ Migration complete! You can now restart your server.")
