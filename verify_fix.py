import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def verify_fix():
    print("Verifying /interview/start...")
    try:
        # 1. Login
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "test_repro@example.com",
            "password": "password123"
        })
        if resp.status_code != 200:
            print(f"Login failed: {resp.status_code}")
            return

        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Start Interview
        # Note: We now support 'difficulty' in payload, but it defaults.
        payload = {"domain": "python", "difficulty": "hard"}
        resp = requests.post(f"{BASE_URL}/interview/start", headers=headers, json=payload)
        
        if resp.status_code == 200:
            print("SUCCESS: /interview/start worked.")
            print(resp.json())
        else:
            print(f"FAILURE: {resp.status_code} - {resp.text}")

    except Exception as e:
        print(f"ERROR: Could not connect to server. {e}")

if __name__ == "__main__":
    verify_fix()
