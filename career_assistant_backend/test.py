import os
import google.generativeai as genai

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Environment variables might not be loaded from .env")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    print("Please ensure you have a .env file with GOOGLE_API_KEY=...")
else:
    print(f"Found API Key: {api_key[:4]}...{api_key[-4:]}")
    genai.configure(api_key=api_key)
    
    with open("models_list.txt", "w", encoding="utf-8") as f:
        f.write("Listing models:\n")
        try:
            found_any = False
            for m in genai.list_models():
                if 'gemini' in m.name:
                    f.write(f"MODEL: {m.name}\n")
                    found_any = True
            
            if not found_any:
                f.write("No models containing 'gemini' found.\n")
            else:
                f.write("Done listing models.\n")
                
        except Exception as e:
            f.write(f"Error: {e}\n")
    print("Written to models_list.txt")
