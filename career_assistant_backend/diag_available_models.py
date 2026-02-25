import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print(f"--- Testing Available Models for Key: {api_key[:10]}... ---")

models_to_try = ["gemini-2.0-flash", "gemini-flash-latest", "gemini-pro-latest"]

for model_name in models_to_try:
    print(f"\n--- Testing model: {model_name} ---")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Test successful with " + model_name + "'")
        print(f"✅ Success! Response: {response.text}")
        break
    except Exception as e:
        print(f"❌ Failed: {e}")
