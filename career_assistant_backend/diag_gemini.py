import os
from dotenv import load_dotenv

load_dotenv()

def test_google_genai():
    print("--- Testing google-genai (SDK v1) ---")
    try:
        from google import genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents="Say 'Hello google-genai'"
        )
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"Error google-genai: {e}")
        return False

def test_google_generativeai():
    print("\n--- Testing google-generativeai (Legacy SDK) ---")
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Say 'Hello legacy genai'")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"Error legacy genai: {e}")
        return False

if __name__ == "__main__":
    test_google_genai()
    test_google_generativeai()
