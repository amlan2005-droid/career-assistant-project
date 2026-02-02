
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.services.chat_services import handle_chat
from app.database.db import Base
import uuid

load_dotenv()

# Setup a temporary in-memory DB or local SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_chat.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def debug_chat():
    db = TestingSessionLocal()
    session_id = str(uuid.uuid4())
    message = "Hello, what skills are in my resume?"
    
    print(f"--- Debugging Chat Flow ---")
    print(f"Session: {session_id}")
    print(f"Message: {message}")
    
    try:
        response = handle_chat(db, session_id, message)
        print(f"\nResponse: {response}")
    except Exception as e:
        print(f"\nUNCAUGHT EXCEPTION in debug script: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_chat()
