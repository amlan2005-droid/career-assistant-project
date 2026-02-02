import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

flash_models = [m.name for m in genai.list_models() if 'flash' in m.name.lower()]
print(flash_models)
