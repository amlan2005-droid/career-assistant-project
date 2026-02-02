"""
Simple test to verify the chat endpoint works without importing query.py
"""
import os
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "test_key")

# Test imports
try:
    print("Testing imports...")
    from app.routers.chat import router, chat_endpoint
    print(" Chat router imported successfully")
    
    from app.rag.vectorstore import get_vectorstore
    print(" Vectorstore imported successfully")
    
    from app.rag.prompt import chat_prompt
    print(" Prompt imported successfully")
    
    print("\n All imports successful! The chatbot should work now.")
    print("\nTo test the chatbot:")
    print("1. Make sure your vectorstore DB exists at app/rag/db")
    print("2. Start the server with: uvicorn app.main:app --reload")
    print("3. Send a POST request to http://localhost:8000/chat/")
    
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
