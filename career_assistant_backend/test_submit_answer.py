import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_submit_answer():
    print("Testing submit answer flow...\n")
    
    try:
        # 1. Login
        print("1. Logging in...")
        login_resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        
        if login_resp.status_code != 200:
            print(f"❌ Login failed: {login_resp.status_code}")
            print(f"Response: {login_resp.text}")
            return
        
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✓ Login successful\n")
        
        # 2. Start interview
        print("2. Starting interview...")
        start_resp = requests.post(
            f"{BASE_URL}/interview/start",
            headers=headers,
            json={"domain": "python", "difficulty": "medium"}
        )
        
        if start_resp.status_code != 200:
            print(f"❌ Start interview failed: {start_resp.status_code}")
            print(f"Response: {start_resp.text}")
            return
        
        start_data = start_resp.json()
        session_id = start_data["session_id"]
        print(f"✓ Interview started, session_id: {session_id}")
        print(f"First question: {start_data['question']}\n")
        
        # 3. Submit answer
        print("3. Submitting answer...")
        answer_payload = {
            "session_id": session_id,
            "answer": "Python is a high-level programming language known for its simplicity and readability."
        }
        
        print(f"Payload: {json.dumps(answer_payload, indent=2)}")
        
        answer_resp = requests.post(
            f"{BASE_URL}/interview/answer",
            json=answer_payload
        )
        
        print(f"\nStatus Code: {answer_resp.status_code}")
        
        if answer_resp.status_code == 200:
            print("✓ Answer submitted successfully!")
            print(f"Response: {json.dumps(answer_resp.json(), indent=2)}")
        else:
            print(f"❌ Submit answer failed!")
            print(f"Response: {answer_resp.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running on port 8000?")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_submit_answer()
