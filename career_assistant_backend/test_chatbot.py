"""
Complete test of the chatbot functionality
"""
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

load_dotenv()

# Import the FastAPI app
from app.main import app

client = TestClient(app)

def test_chat_endpoint():
    """Test the /chat/ endpoint"""
    print("=" * 60)
    print("Testing Chatbot Endpoint")
    print("=" * 60)
    
    # Test question
    test_question = "What is a career assistant?"
    
    print(f"\n📤 Sending question: '{test_question}'")
    print(f"📍 Endpoint: POST /chat/")
    
    try:
        response = client.post(
            "/chat/",
            json={"question": test_question},
            timeout=30
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📥 Response:")
            print(f"   Answer: {data.get('answer', 'No answer')[:200]}...")
            print(f"\n✅ SUCCESS! Your chatbot is working!")
            return True
        else:
            print(f"\n❌ Error Response:")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"\n❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chat_endpoint()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 CHATBOT IS WORKING!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Start the server: uvicorn app.main:app --reload")
        print("2. Access the API at: http://localhost:8000/chat/")
        print("3. Send POST requests with JSON: {\"question\": \"your question\"}")
    else:
        print("\n" + "=" * 60)
        print("⚠️  CHATBOT TEST FAILED")
        print("=" * 60)
        print("\nPlease check:")
        print("1. Vector database exists at app/rag/db")
        print("2. GOOGLE_API_KEY is set in .env file")
        print("3. All dependencies are installed")
