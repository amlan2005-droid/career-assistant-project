
import sys
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    print("SUCCESS: google.genai imported successfully")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("API Key found.")
        client = genai.Client(api_key=api_key)
        print("Client initialized.")
    else:
        print("WARNING: GEMINI_API_KEY not set.")
        
except ImportError as e:
    print(f"FAILURE: {e}")
except Exception as e:
    print(f"ERROR: {e}")
