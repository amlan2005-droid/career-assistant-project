import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

for m in genai.list_models():
    if "flash" in m.name:
        print(f"FOUND: {m.name}")
