import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_score_fix():
    print("🚀 Verifying Final Score and Report Structure...")
    
    # 1. Login
    try:
        login_resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "user@example.com",
            "password": "string"
        })
        
        if login_resp.status_code != 200:
            print(f"❌ Login failed: {login_resp.status_code}")
            return
        
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Start Interview
        start_resp = requests.post(
            f"{BASE_URL}/interview/start",
            headers=headers,
            json={"domain": "python", "difficulty": "medium"}
        )
        
        if start_resp.status_code != 200:
            print(f"❌ Failed to start interview: {start_resp.status_code}")
            print(start_resp.text)
            return
            
        session_id = start_resp.json()["session_id"]
        
        # 3. Answer questions (assuming 5 questions)
        for i in range(5):
            print(f"Answering question {i+1}...")
            answer_resp = requests.post(
                f"{BASE_URL}/interview/answer",
                headers=headers,
                json={
                    "session_id": session_id,
                    "answer": "This is a comprehensive test answer about Python concepts."
                }
            )
            
            data = answer_resp.json()
            if data.get("interview_finished"):
                print("\n✅ Interview Finished!")
                print(f"Final Score Percentage: {data.get('final_score_percentage')}")
                print(f"Message: {data.get('message')}")
                
                report = data.get("report")
                if report and "skills" in report:
                    print(f"Skills in Report: {len(report['skills'])}")
                    for s in report['skills']:
                        print(f"  - {s['name']}: Resume {s['resume_confidence']} | Interview {s['interview_score']}")
                    
                    if data.get('final_score_percentage') is not None:
                        print("\n✨ SUCCESS: final_score_percentage is present and report is structured correctly!")
                    else:
                        print("\n❌ FAIL: final_score_percentage is still missing!")
                else:
                    print("\n❌ FAIL: report or report.skills is missing!")
                break
                
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_score_fix()
