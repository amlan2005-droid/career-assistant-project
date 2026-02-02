
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def check_models():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        with open("models_v2_list.txt", "w", encoding="utf-8") as f:
            f.write("No API key found!")
        return
        
    genai.configure(api_key=api_key)
    
    try:
        with open("models_v2_list.txt", "w", encoding="utf-8") as f:
            f.write("Available models:\n")
            for m in genai.list_models():
                f.write(f"- {m.name} (Methods: {m.supported_generation_methods})\n")
    except Exception as e:
        with open("models_v2_list.txt", "w", encoding="utf-8") as f:
            f.write(f"Error listing models: {e}\n")

if __name__ == "__main__":
    check_models()
