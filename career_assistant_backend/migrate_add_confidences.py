import sqlite3

def migrate():
    try:
        conn = sqlite3.connect('career.db')
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(interview_sessions)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'confidences' not in columns:
            print("Adding confidences column...")
            cursor.execute("ALTER TABLE interview_sessions ADD COLUMN confidences JSON")
            conn.commit()
            print("Migration successful.")
        else:
            print("confidences column already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
