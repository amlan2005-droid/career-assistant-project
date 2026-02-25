import sqlite3

def migrate():
    try:
        conn = sqlite3.connect('career.db')
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(interview_sessions)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'total_questions' not in columns:
            print("Adding total_questions column...")
            cursor.execute("ALTER TABLE interview_sessions ADD COLUMN total_questions INTEGER DEFAULT 5")
            conn.commit()
            print("Migration successful.")
        else:
            print("total_questions column already exists.")
            
        conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
