import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print(f"--- Testing Key: {api_key[:10]}...{api_key[-5:]} ---")

try:
    genai.configure(api_key=api_key)
    # Using explicit 'models/' prefix
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content("Say 'Prefix test with new key successful'")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error Message: {e}")
