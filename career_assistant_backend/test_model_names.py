"""
Test what model names are available
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Testing different model names...")
print("=" * 50)

# Try different model name formats
model_names = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-pro",
    "models/gemini-1.5-pro",
    "models/gemini-pro",
]

for model_name in model_names:
    try:
        print(f"\nTrying: {model_name}")
        response = client.models.generate_content(
            model=model_name,
            contents="Say 'test' if you can read this",
            config={"temperature": 0.1, "max_output_tokens": 10}
        )
        print(f"  ✅ SUCCESS! Response: {response.text[:50]}")
        break
    except Exception as e:
        print(f"  ❌ Failed: {str(e)[:100]}")
