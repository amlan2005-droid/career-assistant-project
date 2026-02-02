"""
Check what tables exist in the database
"""
import sqlite3

conn = sqlite3.connect('career.db')
cursor = conn.cursor()

try:
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("=== AVAILABLE TABLES ===")
    for table in tables:
        print(f"- {table[0]}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
