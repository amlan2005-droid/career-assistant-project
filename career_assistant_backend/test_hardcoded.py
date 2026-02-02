import os
import google.generativeai as genai

# Hardcoded test key from your .env
API_KEY = "AIzaSyBNbwHd0h9DfEJ93fXq4Zvdz8WLRwEjdYA"

print("--- Testing Hardcoded Key (Legacy SDK) ---")
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say 'Hardcoded test successful'")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
