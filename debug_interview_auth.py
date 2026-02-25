import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_interview_start():
    # 1. Login to get token
    email = "test_repro@example.com"
    password = "password123"

    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        # Try registering if login fails (first run cleanup?)
        print("Registering new user just in case...")
        reg_resp = requests.post(f"{BASE_URL}/auth/register", json={
            "username": "debug_user",
            "email": email,
            "password": password
        })
        if reg_resp.status_code == 201:
             print("Registered. Logging in again...")
             resp = requests.post(f"{BASE_URL}/auth/login", json={
                "email": email,
                "password": password
            })
        else:
             print(f"Registration also failed/exists: {reg_resp.status_code}")
             if resp.status_code != 200:
                 return

    if resp.status_code != 200:
         print("Could not get token.")
         return

    token = resp.json()["access_token"]
    print(f"Got token: {token[:10]}...")

    # 2. Start Interview
    print("Starting interview...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"domain": "python"}
    
    # We expect this to work if backend is fine
    resp = requests.post(f"{BASE_URL}/interview/start", headers=headers, json=payload)
    
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    test_interview_start()
