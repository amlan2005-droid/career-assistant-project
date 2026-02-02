"""
Test if the existing gemini_client works
"""
import sys
sys.path.insert(0, 'c:/Users/DELL/career_assistant_project/career_assistant_backend')

from app.services.gemini_client import ask_gemini

print("Testing existing Gemini client...")
print("=" * 50)

try:
    response = ask_gemini("List 5 common programming languages")
    print(f"✅ Response: {response}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
