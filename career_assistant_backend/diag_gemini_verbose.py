import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

models_to_try = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-2.0-flash-exp"]

for model_name in models_to_try:
    print(f"\n--- Testing model: {model_name} ---")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Hello"
        )
        print(f"✅ Success! Response: {response.text}")
        break
    except Exception as e:
        print(f"❌ Failed: {e}")
