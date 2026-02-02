import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.getcwd()))

from app.services.gemini_client import ask_gemini

print("--- Testing updated gemini_client.py ---")
response = ask_gemini("Say 'The Gemini client is working correctly'")
print(f"Response: {response}")

if response.startswith("ERROR:"):
    print("❌ Test failed")
else:
    print("✅ Test passed")
