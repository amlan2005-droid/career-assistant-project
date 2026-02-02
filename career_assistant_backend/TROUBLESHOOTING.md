# Troubleshooting Gemini AI Issues

If you encounter "Model Not Found" or "General AI Error" messages in the future, follow these steps to diagnose and fix them.

## 1. Check Model Availability
Google occasionally changes model names or availability for specific API tiers. To see exactly which models your API key can access:

1. Create a temporary file `check_models.py`:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")
```
2. Run it: `python check_models.py`
3. Compare the names in the list (e.g., `models/gemini-2.0-flash`) with the names in your code.

## 2. Update Model Names in Code
If the model names have changed, update them in these three locations:

*   **Chatbot:** `app/services/chat_services.py` (look for `ChatGoogleGenerativeAI(model="...")`)
*   **Interview Engine:** `app/services/gemini_client.py` (look for `model="..."` in `generate_content`)
*   **Embeddings:** `app/rag/vectorstore.py` (look for `GoogleGenerativeAIEmbeddings(model="...")`)

## 3. Handle "Dimension Mismatch" (ChromaDB)
If you update the **Embedding model**, you will likely see a dimension error. This happens because the new model produces vectors of a different size (e.g., 3072 instead of 768).

**To fix this:**
1. Stop your server.
2. Delete the old database folder: `app/rag/db_v2` (or whatever the current path is).
3. Run the ingest script to rebuild the database:
   ```bash
   python -m app.rag.ingest
   ```
4. Restart your server.

## 4. Handle Rate Limiting (429 Errors)
If you see "I'm temporarily rate-limited":
*   Wait **60 seconds** and try again.
*   The Free Tier has a limit of **15 requests per minute**. If you need more, consider creating a second Google Cloud project and getting a new API key.

## 5. View Logs
Always check the terminal window where `uvicorn` is running. If something goes wrong, it will print a "Traceback" which contains the exact error message and line number.
