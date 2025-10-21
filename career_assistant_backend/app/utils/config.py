import os
from dotenv import load_dotenv

load_dotenv()  # load from .env file

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Base URL (India example, change country if needed)
ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"