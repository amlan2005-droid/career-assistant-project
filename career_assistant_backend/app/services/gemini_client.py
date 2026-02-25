import os
import time
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

logger = logging.getLogger(__name__)

# Retry logic for the core Gemini client
retry_on_quota = retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=5, max=60),
    retry=retry_if_exception_type(Exception),
    reraise=True
)

# Try both common environment variable names
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Initialize the new SDK client
client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        key_censored = f"{GEMINI_API_KEY[:5]}...{GEMINI_API_KEY[-5:]}"
        print(f"[SUCCESS] Gemini API (New SDK) initialized successfully with key: {key_censored}")
    except Exception as e:
        print(f"[ERROR] Failed to initialize Gemini Client: {e}")
else:
    print("[WARNING] GEMINI_API_KEY or GOOGLE_API_KEY not found. AI features will be disabled.")

@retry_on_quota
def ask_gemini(prompt: str) -> str:
    if not client:
        print("[WARNING] Gemini client not initialized. Returning fallback response.")
        return "ERROR: API key missing or client initialization failed. Please check your .env file."

    try:
        # Using the new SDK's generate_content method
        response = client.models.generate_content(
            model="gemini-2.0-flash", # Upgrading to the latest recommended flash model
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=1000,
            )
        )

        if not response or not response.text:
            print(f"[WARNING] Gemini returned an empty response for prompt length: {len(prompt)}")
            return "ERROR: Empty response from Gemini"

        return response.text.strip()

    except Exception as e:
        error_msg = str(e).lower()
        print(f" Gemini API error ({GEMINI_API_KEY[:5]}...):", error_msg)
        
        # Simple error categorization for the new SDK
        if "429" in error_msg or "resource_exhausted" in error_msg:
            return "ERROR: Rate limit exceeded. Please wait a moment."
        if "404" in error_msg:
            return "ERROR: Model not found or invalid API configuration."
        if "400" in error_msg and ("expired" in error_msg or "invalid" in error_msg):
            return "ERROR: The API key provided is reported as invalid or expired."
            
        raise e
