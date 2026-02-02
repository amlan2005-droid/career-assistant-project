"""
Direct test of chat router without TestClient
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def test_chat_directly():
    """Test the chat endpoint directly"""
    print("=" * 60)
    print("Testing Chat Endpoint Directly")
    print("=" * 60)
    
    try:
        # Import the endpoint function
        from app.routers.chat import chat_endpoint, QueryRequest
        
        # Create a test request
        test_request = QueryRequest(question="What is a career assistant?")
        
        print(f"\n📤 Testing with question: '{test_request.question}'")
        
        # Call the endpoint
        result = await chat_endpoint(test_request)
        
        print(f"\n✅ SUCCESS!")
        print(f"📥 Answer: {result['answer'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_chat_directly())
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 CHATBOT IS WORKING!")
        print("=" * 60)
        print("\nYour chatbot is functional. Start the server with:")
        print("  uvicorn app.main:app --reload")
    else:
        print("\n" + "=" * 60)
        print("⚠️  TEST FAILED - Check error above")
        print("=" * 60)
