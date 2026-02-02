import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

with open("flash_models_list.txt", "w") as f:
    for m in genai.list_models():
        if "flash" in m.name:
            f.write(m.name + "\n")
