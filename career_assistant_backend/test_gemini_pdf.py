import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

def extract_text_gemini(file_path):
    key = os.getenv("GOOGLE_API_KEY")
    print(f"API Key found: {bool(key)}")
    if key:
        print(f"Key starts with: {key[:5]}...")
    genai.configure(api_key=key)
    
    print(f"Uploading {file_path} to Gemini...")
    sample_file = genai.upload_file(path=file_path, display_name="Resume")
    
    while sample_file.state.name == "PROCESSING":
        print(".", end="")
        time.sleep(2)
        sample_file = genai.get_file(sample_file.name)
    
    if sample_file.state.name == "FAILED":
        raise Exception("Gemini file processing failed")

    print("\nFile processed. Prompting Gemini for text...")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        sample_file,
        "Extract all the text from this resume exactly as it appears. "
        "Maintain the layout structure as much as possible."
    ])
    
    # Cleanup
    genai.delete_file(sample_file.name)
    
    return response.text

if __name__ == "__main__":
    target = r"c:\Users\DELL\career_assistant_project\career_assistant_backend\uploads\resume aiml engineer.pdf"
    if os.path.exists(target):
        try:
            text = extract_text_gemini(target)
            print("--- Extracted Text ---")
            print(text)
            with open("extracted_gemini.txt", "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("File not found.")
