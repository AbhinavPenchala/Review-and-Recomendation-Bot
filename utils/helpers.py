
def format_response(response_text):
    """Format the response with a prefix or styling."""
    return f"✅ Here’s what I found:\n{response_text}"

def needs_fallback(response_text):
    """Check if the response requires additional information."""
    fallback_keywords = ["I don't have enough information", "Let me check online", "I'm not sure"]
    return any(keyword.lower() in response_text.lower() for keyword in fallback_keywords)
