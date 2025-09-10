from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from config.config import GOOGLE_GEMINI_API_KEY

def get_gemini_model():
    model = ChatGoogleGenerativeAI(api_key=GOOGLE_GEMINI_API_KEY, model="gemini-1.5-pro")
    return model
