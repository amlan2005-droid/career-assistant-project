import sys
import os
import json
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_adaptive_flow():
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
    data = start_resp.json()
    session_id = data["session_id"]
    print(f"Session ID: {session_id}")
    print(f"Q1: {data['question']}")
    
    # 3. Flow Loop
    for i in range(1, 4):
        print(f"\n--- Turn {i} ---")
        # Submit answer
        print(f"Submitting answer for Q{i}...")
        ans_payload = {"session_id": session_id, "answer": f"Adaptive test answer for Q{i}."}
        ans_resp = requests.post(f"{BASE_URL}/interview/answer", json=ans_payload, headers=headers)
        print(f"Answer Status: {ans_resp.status_code}")
        try:
            print(f"Answer Body: {ans_resp.json()}")
        except:
            print(f"FAILED TO DECODE JSON. RAW BODY: {ans_resp.text}")
            return

        if i < 3:
            # Get next question
            print(f"Fetching next question...")
            next_resp = requests.get(f"{BASE_URL}/interview/next/{session_id}", headers=headers)
            print(f"Next Status: {next_resp.status_code}")
            next_data = next_resp.json()
            if next_data.get("interview_finished"):
                print("Interview finished ahead of schedule?")
                break
            print(f"Next Q: {next_data['question']}")
        else:
            # Final check
            print("Finished 3 turns. Checking final state...")
            summary_resp = requests.get(f"{BASE_URL}/interview/summary/{session_id}", headers=headers)
            print(f"Summary Status: {summary_resp.status_code}")
            print(f"Summary: {json.dumps(summary_resp.json(), indent=2)}")

if __name__ == "__main__":
    test_adaptive_flow()
