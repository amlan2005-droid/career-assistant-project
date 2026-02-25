import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8000"

def test_interview_flow():
    email = "user@example.com"
    password = "string"
    
    # 1. Login
    print(f"--- Logging in as {email} ---")
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.status_code} {login_resp.text}")
        return
    
    token = login_resp.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 2. Start Interview
    print("--- Starting Interview ---")
    start_payload = {
        "domain": "python",
        "difficulty": "medium",
        "question_count": 5
    }
    start_resp = requests.post(f"{BASE_URL}/interview/start", json=start_payload, headers=headers)
    
    if start_resp.status_code != 200:
        print(f"Start interview failed: {start_resp.status_code} {start_resp.text}")
        return
    
    start_data = start_resp.json()
    session_id = start_data.get("session_id")
    first_question = start_data.get("question")
    print(f"Interview started. Session ID: {session_id}")
    print(f"First Question: {first_question}")

    # 3. Submit Answer
    print("--- Submitting Answer ---")
    answer_payload = {
        "session_id": session_id,
        "answer": "Python is a high-level, interpreted programming language known for its readability and versatility."
    }
    answer_resp = requests.post(f"{BASE_URL}/interview/answer", json=answer_payload, headers=headers)
    
    if answer_resp.status_code != 200:
        print(f"Submit answer failed: {answer_resp.status_code} {answer_resp.text}")
        return
    
    answer_data = answer_resp.json()
    print(f"Answer submitted. Next Question: {answer_data.get('question')}")
    print(f"Feedback on last answer: {answer_data.get('feedback')}")

    # 4. Get Summary
    print("--- Getting Summary ---")
    summary_resp = requests.get(f"{BASE_URL}/interview/summary/{session_id}", headers=headers)
    
    if summary_resp.status_code != 200:
        print(f"Get summary failed: {summary_resp.status_code} {summary_resp.text}")
        return
    
    print("Summary retrieved successfully:")
    print(json.dumps(summary_resp.json(), indent=2))

if __name__ == "__main__":
    test_interview_flow()
