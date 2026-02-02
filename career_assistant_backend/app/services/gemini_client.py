import os
import time
import logging
from dotenv import load_dotenv
import google.generativeai as genai
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

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("✅ Gemini API (Legacy SDK) initialized successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize Gemini Client: {e}")
else:
    print("⚠️ WARNING: GEMINI_API_KEY or GOOGLE_API_KEY not found. AI features will be disabled.")

@retry_on_quota
def ask_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        print("⚠️ Gemini API key missing. Returning fallback response.")
        return "ERROR: API key missing. Please check your .env file."

    try:
        # Use Gemini 1.5 Flash (stable)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(
            contents=prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                max_output_tokens=1000,
            )
        )

        if not response or not response.text:
            print(f"⚠️ Gemini returned an empty response for prompt length: {len(prompt)}")
            return "ERROR: Empty response from Gemini"

        return response.text.strip()

    except Exception as e:
        error_msg = str(e).lower()
        print(" Gemini API error:", error_msg)
        if "429" in error_msg or "resource_exhausted" in error_msg:
            return "ERROR: Rate limit exceeded. Please wait a moment."
        if "404" in error_msg:
            return "ERROR: Model not found or invalid API configuration."
        raise e
