import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

try:
    models = list(client.models.list())
    for m in models:
        # Print without the 'models/' prefix
        print(m.name.split('/')[-1])
except Exception as e:
    print(f"Error: {e}")
