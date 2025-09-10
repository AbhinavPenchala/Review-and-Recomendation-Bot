from google.generativeai import Client
from config.config import GOOGLE_GEMINI_API_KEY

def get_gemini_model():
    """Initialize and return the Google Gemini client."""
    try:
        client = Client(api_key=GOOGLE_GEMINI_API_KEY)
        return client
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None
