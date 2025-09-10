
from config.config import GOOGLE_GEMINI_API_KEY

def get_gemini_model():
    """Initialize and return the Google Gemini chat model."""
    try:
        model = ChatGoogleGenerativeAI(api_key=GOOGLE_GEMINI_API_KEY, model="gemini-1.5-pro")
        return model
    except Exception as e:
        print(f"Error initializing Gemini model: {e}")
        return None
