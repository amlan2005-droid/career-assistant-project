
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import google.api_core.exceptions

load_dotenv()

def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    print(f"Using API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")
    
    # Trying gemini-2.0-flash which was in the list
    model_name = "gemini-2.0-flash" 
    print(f"Testing model: {model_name}")
    
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.3,
    )
    
    try:
        print("Sending message to Gemini...")
        response = llm.invoke([HumanMessage(content="Hello, are you there?")])
        print("Response received:")
        print(response.content)
    except Exception as e:
        print(f"Caught exception: {type(e).__name__}")
        print(f"Error message: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini()
