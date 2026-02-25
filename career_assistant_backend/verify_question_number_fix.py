import requests
import json
import uuid
import os

BASE_URL = "http://127.0.0.1:8000"

def verify_fix():
    # 1. Login/Register
    email = f"test_fix_{uuid.uuid4().hex[:6]}@example.com"
    password = "password123"
    username = "test_fix_user"
    
    print(f"Registering {email}...")
    requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })

    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return

    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Logged in successfully.")

    # 2. Upload Resume
    print("Uploading mock resume...")
    resume_content = "Experienced Python Developer with expertise in FastAPI, PostgreSQL, and AWS. Strong background in backend engineering and system design."
    with open("mock_resume.txt", "w") as f:
        f.write(resume_content)
    
    with open("mock_resume.txt", "rb") as f:
        resp = requests.post(f"{BASE_URL}/resume/upload", headers=headers, files={"file": ("mock_resume.txt", f, "text/plain")})
    
    if resp.status_code != 200 and resp.status_code != 201:
        print(f"Resume upload failed: {resp.text}")
        return
    print("Resume uploaded successfully.")

    # 3. Start Interview
    print("Starting interview...")
    resp = requests.post(f"{BASE_URL}/interview/start", json={
        "domain": "python",
        "question_count": 5
    }, headers=headers)
    
    if resp.status_code != 200:
        print(f"Start interview failed: {resp.text}")
        return
    
    start_data = resp.json()
    session_id = start_data["session_id"]
    print(f"Session ID: {session_id}")
    print(f"First Question: {start_data['question']}")
    print(f"First Question Number: {start_data['question_number']}")

    # 4. Submit Answer
    print("\nSubmitting answer to first question...")
    resp = requests.post(f"{BASE_URL}/interview/answer", json={
        "session_id": session_id,
        "answer": "Python is a high-level, interpreted programming language known for its readability and versatile libraries."
    }, headers=headers)
    
    if resp.status_code != 200:
        print(f"Submit answer failed: {resp.text}")
        return
    
    answer_data = resp.json()
    print(f"Answer Response: {json.dumps(answer_data, indent=2)}")
    
    # 5. Assertions
    if "question" in answer_data and "question_number" in answer_data:
        print("\n✅ SUCCESS: 'question' and 'question_number' found in response!")
        if answer_data["question_number"] == 2:
            print("✅ SUCCESS: 'question_number' is correctly incremented to 2.")
        else:
            print(f"❌ FAILURE: 'question_number' is {answer_data['question_number']}, expected 2.")
    else:
        print("\n❌ FAILURE: Missing 'question' or 'question_number' in response.")
    
    # Cleanup
    if os.path.exists("mock_resume.txt"):
        os.remove("mock_resume.txt")

if __name__ == "__main__":
    verify_fix()
