from google import genai
from google.genai import types
import os
import time
from dotenv import load_dotenv

load_dotenv()

def extract_text_gemini(file_path):
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    print(f"API Key found: {bool(key)}")
    if key:
        print(f"Key starts with: {key[:5]}...")
    
    client = genai.Client(api_key=key)
    
    print(f"Uploading {file_path} to Gemini...")
    # New SDK handles file upload differently if using the files API
    # But for a simple script, we can pass the path directly or use the Files API
    with open(file_path, "rb") as f:
        # Note: The new SDK supports direct path in some contexts, 
        # but here's the formal way using the files API if desired.
        uploaded_file = client.files.upload(path=file_path, config=types.UploadFileConfig(display_name="Resume"))
    
    print(f"File uploaded as: {uploaded_file.name}")
    
    # Wait for processing
    while True:
        uploaded_file = client.files.get(name=uploaded_file.name)
        if uploaded_file.state == "ACTIVE":
            break
        elif uploaded_file.state == "FAILED":
            raise Exception("Gemini file processing failed")
        print(".", end="", flush=True)
        time.sleep(2)
    
    print("\nFile processed. Prompting Gemini for text...")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            uploaded_file,
            "Extract all the text from this resume exactly as it appears. "
            "Maintain the layout structure as much as possible."
        ]
    )
    
    # Cleanup (Optional, but good practice)
    try:
        client.files.delete(name=uploaded_file.name)
        print("File cleaned up from Gemini server.")
    except Exception as e:
        print(f"Cleanup failed: {e}")
    
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
