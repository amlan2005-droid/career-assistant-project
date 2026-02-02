import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def reproduce_interview_403():
    # 1. Login/Register
    email = "repro_user@example.com"
    password = "password123"
    
    print(f"Logging in user: {email}...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if resp.status_code == 401:
        print("User not found, registering...")
        resp = requests.post(f"{BASE_URL}/auth/register", json={
            "username": "repro_user",
            "email": email,
            "password": password
        })
    
    if resp.status_code not in [200, 201]:
        print(f"Auth failed: {resp.text}")
        return

    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Logged in successfully.")

    # 2. Upload a dummy resume if needed (for domains)
    print("Uploading dummy resume...")
    files = {"file": ("resume.txt", "Expert in Python, Backend, and Fast API.", "text/plain")}
    requests.post(f"{BASE_URL}/resume/upload", headers=headers, files=files)

    # 3. Start Interview
    print("Starting interview...")
    resp = requests.post(f"{BASE_URL}/interview/start", headers=headers, json={"domain": "python"})
    if resp.status_code != 200:
        print(f"Failed to start interview: {resp.text}")
        return
    
    data = resp.json()
    session_id = data["session_id"]
    print(f"Interview started. session_id: {session_id}")

    # 4. Submit Answer (The problematic step)
    print("Submitting answer...")
    resp = requests.post(f"{BASE_URL}/interview/answer", headers=headers, json={
        "session_id": session_id,
        "answer": "A decorator is a function that takes another function and extends its behavior."
    })
    
    print(f"Submit Answer Status: {resp.status_code}")
    print(f"Submit Answer Response: {resp.text}")

    if resp.status_code == 403:
        print("REPRODUCED: Got 403 Forbidden on /interview/answer")
    else:
        print(f"Result: {resp.status_code}")

if __name__ == "__main__":
    reproduce_interview_403()
