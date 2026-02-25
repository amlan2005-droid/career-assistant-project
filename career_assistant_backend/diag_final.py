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
    log_file = 'diag_final_log.txt'
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("--- DIAGNOSTIC START ---\n")
        try:
            # 1. Login/Token
            token = create_access_token({"sub": "1"})
            headers = {"Authorization": f"Bearer {token}"}
            
            # 2. Start Interview
            f.write("Starting interview...\n")
            start_payload = {
                "domain": "python",
                "difficulty": "medium",
                "question_count": 5
            }
            resp = client.post("/interview/start", json=start_payload, headers=headers)
            f.write(f"Start Status: {resp.status_code}\n")
            if resp.status_code != 200:
                f.write(f"Start failed: {resp.text}\n")
                return
                
            session_id = resp.json()["session_id"]
            f.write(f"Session ID: {session_id}\n")
            
            # 3. Submit Answer
            f.write("Submitting answer...\n")
            answer_payload = {
                "session_id": session_id,
                "answer": "Test Answer"
            }
            resp = client.post("/interview/answer", json=answer_payload, headers=headers)
            f.write(f"Answer Status: {resp.status_code}\n")
            if resp.status_code != 200:
                f.write(f"Answer failed: {resp.text}\n")
            else:
                f.write("Answer Success!\n")
                
        except Exception:
            f.write("EXCEPTION IN DIAG SCRIPT:\n")
            f.write(traceback.format_exc())
        f.write("\n--- DIAGNOSTIC END ---")

if __name__ == "__main__":
    run_diag()
