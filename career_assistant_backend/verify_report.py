import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_complete_interview():
    print("🚀 Testing Complete Interview Flow and Report Generation...")
    
    # 1. Login
    try:
        print("\n🔑 Logging in...")
        login_resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        
        if login_resp.status_code != 200:
            print(f"❌ Login failed: {login_resp.status_code}")
            return
        
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login successful")
        
        # 2. Start Interview
        print("\n🏁 Starting interview...")
        start_resp = requests.post(
            f"{BASE_URL}/interview/start",
            headers=headers,
            json={"domain": "python", "difficulty": "medium"}
        )
        
        if start_resp.status_code != 200:
            print(f"❌ Failed to start interview: {start_resp.status_code}")
            return
            
        session_data = start_resp.json()
        session_id = session_data["session_id"]
        print(f"✅ Session started: {session_id}")
        
        # 3. Answer questions until finished
        finished = False
        iteration = 1
        while not finished and iteration < 10:
            print(f"\n📝 Answering question {iteration}...")
            answer_resp = requests.post(
                f"{BASE_URL}/interview/answer",
                headers=headers,
                json={
                    "session_id": session_id,
                    "answer": f"This is a test answer for question {iteration}. I know Python well."
                }
            )
            
            if answer_resp.status_code != 200:
                print(f"❌ Failed to submit answer: {answer_resp.status_code}")
                print(answer_resp.text)
                return
                
            data = answer_resp.json()
            finished = data.get("interview_finished", False)
            
            if finished:
                print("✅ Interview finished!")
                print("\n📊 --- POST-INTERVIEW REPORT ---")
                report = data.get("report")
                if report:
                    print(json.dumps(report, indent=2))
                    if "skills" in report and len(report["skills"]) > 0:
                        print("\n✨ SUCCESS: Skill report generated correctly!")
                    else:
                        print("\n⚠️ WARNING: Report generated but skills list is empty.")
                else:
                    print("\n❌ ERROR: Report missing from response!")
            else:
                print(f"Next question: {data.get('question')[:50]}...")
            
            iteration += 1
            time.sleep(0.5)

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server. Is it running?")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_complete_interview()
