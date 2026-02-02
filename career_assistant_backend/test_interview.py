import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_interview_start():
    print("Testing /interview/start endpoint...")
    
    # First, login to get a token
    try:
        login_resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.status_code}")
            print(f"Response: {login_resp.text}")
            return
        
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print(f"✓ Login successful, token obtained")
        
        # Test interview start
        payload = {"domain": "python"}
        print(f"\nSending request: POST /interview/start")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        interview_resp = requests.post(
            f"{BASE_URL}/interview/start",
            headers=headers,
            json=payload
        )
        
        print(f"\nStatus Code: {interview_resp.status_code}")
        print(f"Response: {json.dumps(interview_resp.json(), indent=2)}")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"ERROR: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")

if __name__ == "__main__":
    test_interview_start()
