import sys
import traceback
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

# Add project root to sys.path
sys.path.append('.')

from app.main import app
from app.database.db import get_db, Base
from app.models.user import User
from app.models.resume_analysis import ResumeAnalysis
from app.models.resume_profile import ResumeProfile
from app.auth.auth_handler import create_access_token

client = TestClient(app)

def debug_flow():
    email = "user@example.com"
    
    # 1. Setup mock auth
    token = create_access_token({"sub": "1"}) # Assuming user ID 1 exists
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 2. Start Interview
        print("--- Starting Interview ---")
        start_payload = {
            "domain": "python",
            "difficulty": "medium",
            "question_count": 5
        }
        resp = client.post("/interview/start", json=start_payload, headers=headers)
        print(f"Start Status: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.json())
            return
            
        data = resp.json()
        session_id = data.get("session_id")
        
        # 3. Submit Answer
        print("--- Submitting Answer ---")
        answer_payload = {
            "session_id": session_id,
            "answer": "Test answer"
        }
        resp = client.post("/interview/answer", json=answer_payload, headers=headers)
        print(f"Answer Status: {resp.status_code}")
        if resp.status_code != 200:
            print(resp.text)
            
    except Exception:
        print("Exception occurred in test script:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_flow()
