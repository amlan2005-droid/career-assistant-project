from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv
import sys

# Force UTF-8 for output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

from app.main import app

client = TestClient(app)

def test_chat_endpoint():
    print("=" * 60)
    print("Testing Chatbot Endpoint (Clean)")
    print("=" * 60)
    
    test_question = "What is a career assistant?"
    print(f"Sending question: '{test_question}'")
    
    try:
        response = client.post(
            "/chat/",
            json={"question": test_question},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('answer', 'No answer')[:200]}...")
            print("SUCCESS! Your chatbot is working!")
            return True
        else:
            print(f"Error Response: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chat_endpoint()
    sys.exit(0 if success else 1)
