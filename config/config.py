import os

# API key for Google Gemini via Google AI Studio
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY", "your_google_gemini_api_key_here")

# API key for Apify for web scraping
APIFY_API_KEY = os.getenv("APIFY_API_KEY", "your_apify_api_key_here")

# Optional fallback API key placeholder if needed in future expansions
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "your_optional_search_api_key_here")

# Instructions:
# 1. Replace the placeholder strings with your actual API keys or set environment variables.
