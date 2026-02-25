import sys
import os
import json
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    # 1. Login
    print("--- Logging in ---")
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": "user@example.com", "password": "string"})
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.text}")
        return
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Start Interview
    print("--- Starting interview ---")
    start_payload = {"domain": "python", "difficulty": "medium", "question_count": 5}
    start_resp = requests.post(f"{BASE_URL}/interview/start", json=start_payload, headers=headers)
    if start_resp.status_code != 200:
        print(f"Start failed: {start_resp.text}")
        return
    session_id = start_resp.json()["session_id"]
    print(f"Session ID: {session_id}")
    
    # 3. Submit 3 answers
    print("--- Submitting 3 answers ---")
    for i in range(1, 4):
        print(f"Answering question {i}...")
        ans_payload = {"session_id": session_id, "answer": f"Test answer for question {i}."}
        ans_resp = requests.post(f"{BASE_URL}/interview/answer", json=ans_payload, headers=headers)
        if ans_resp.status_code != 200:
            print(f"Answer {i} failed: {ans_resp.text}")
            return
        print(f"Response: {ans_resp.json()}")
        time.sleep(1) # Small delay for AI
        
    # 4. Check State
    print("--- Checking State ---")
    state_resp = requests.get(f"{BASE_URL}/interview/state/{session_id}", headers=headers)
    if state_resp.status_code != 200:
        print(f"State check failed: {state_resp.text}")
        return
    
    state = state_resp.json()
    print("Interview State Result:")
    print(json.dumps(state, indent=2))
    
    # Verify the requested fields exist
    fields = ["questions_asked", "average_score", "skill_scores", "confidence_trend"]
    for f in fields:
        if f in state:
            print(f"[OK] Found field: {f}")
        else:
            print(f"[ERROR] Missing field: {f}")

if __name__ == "__main__":
    test_flow()
