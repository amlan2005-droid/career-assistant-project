
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

def test_model(model_name):
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    print(f"Testing model: {model_name}")
    
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.3,
    )
    
    try:
        response = llm.invoke([HumanMessage(content="Hi")])
        print(f"✅ Success for {model_name}: {response.content}")
        return True
    except Exception as e:
        print(f"❌ Failed for {model_name}: {e}")
        return False

if __name__ == "__main__":
    # Test with and without models/ prefix
    test_model("gemini-2.0-flash")
    test_model("models/gemini-2.0-flash")
    # Also test an alternative that was in the list
    test_model("gemini-flash-latest")
