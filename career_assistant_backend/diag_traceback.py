import sys
import os
import traceback
import json

# Add project root to sys.path
sys.path.append('.')

from fastapi.testclient import TestClient
from app.main import app
from app.auth.auth_handler import create_access_token

client = TestClient(app)

def run_diag():
    print("--- DIAGNOSTIC START ---")
    try:
        # 1. Login/Token
        token = create_access_token({"sub": "1"})
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Start Interview
        print("Starting interview...")
        start_payload = {
            "domain": "python",
            "difficulty": "medium",
            "question_count": 5
        }
        resp = client.post("/interview/start", json=start_payload, headers=headers)
        if resp.status_code != 200:
            print(f"Start failed ({resp.status_code}): {resp.text}")
            return
            
        session_id = resp.json()["session_id"]
        print(f"Session ID: {session_id}")
        
        # 3. Submit Answer (The failure point)
        print("Submitting answer...")
        answer_payload = {
            "session_id": session_id,
            "answer": "Python is a great language."
        }
        resp = client.post("/interview/answer", json=answer_payload, headers=headers)
        if resp.status_code != 200:
            print(f"Answer failed ({resp.status_code}):")
            try:
                print(json.dumps(resp.json(), indent=2))
            except:
                print(resp.text)
        else:
            print("Answer Success!")
            
    except Exception:
        print("EXCEPTION IN DIAG SCRIPT:")
        traceback.print_exc()
    print("--- DIAGNOSTIC END ---")

if __name__ == "__main__":
    # Ensure uvicorn logs are shown if possible (FastAPI TestClient doesn't always show them)
    # But print() in router should show up here.
    run_diag()
    sys.stdout.flush()
