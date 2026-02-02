import os
import google.generativeai as genai

API_KEY = "AIzaSyBNbwHd0h9DfEJ93fXq4Zvdz8WLRwEjdYA"

print("--- Testing Explicit Prefix (Legacy SDK) ---")
try:
    genai.configure(api_key=API_KEY)
    # Using explicit 'models/' prefix
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content("Say 'Prefix test successful'")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
