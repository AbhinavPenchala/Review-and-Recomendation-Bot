
import requests
from config.config import APIFY_API_KEY

def web_search(query):
    """
    Perform a fallback web search using Apify's API for additional information.
    Searches for restaurants, food reviews, malls, services, and electronics stores.
    """
    try:
        # Placeholder URL for Apify API search — replace with actual endpoint if needed
        url = "https://api.apify.com/v2/acts/placeholder/search/run-sync-get"
        
        params = {
            "token": APIFY_API_KEY,  # API key placeholder
            "q": query,
            "limit": 5  # limit the number of results
        }

        # Send request to Apify API
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Example format: adapt this based on actual API response
            results = data.get("results", [])
            
            if not results:
                return "🔍 Sorry, I couldn't find any relevant information online."
            
            # Format top results
            formatted = "🔍 Here are some additional suggestions I found online:\n"
            for idx, item in enumerate(results, start=1):
                title = item.get("title", "No title available")
                link = item.get("url", "#")
                formatted += f"{idx}. [{title}]({link})\n"
            
            return formatted
        else:
            return f"⚠️ Search failed with status code {response.status_code}. Please try again later."

    except requests.exceptions.Timeout:
        return "⚠️ The request timed out. Please check your internet connection and try again."
    except requests.exceptions.RequestException as e:
        return f"⚠️ An error occurred while searching: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"
