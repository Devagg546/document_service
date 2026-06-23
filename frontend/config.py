import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This must run before anything tries to read os.getenv()
load_dotenv()

# ── Backend ────────────────────────────────────────────────────────────────────
# The URL where Sarvesh's Django server is running
# Change this to the real server URL when deploying
BASE_URL = "https://doclens-backend-wix2.onrender.com"

# ── AI ─────────────────────────────────────────────────────────────────────────
# Groq API key — loaded from .env file, never hardcoded
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Which Groq model to use
GROQ_MODEL = "llama-3.3-70b-versatile"
