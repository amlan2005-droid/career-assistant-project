import os
import google.generativeai as genai

API_KEY = "AIzaSyBNbwHd0h9DfEJ93fXq4Zvdz8WLRwEjdYA"

print("--- Testing Gemini Pro (Legacy SDK) ---")
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Say 'Gemini Pro test successful'")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
