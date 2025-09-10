import streamlit as st
from config.config import GOOGLE_GEMINI_API_KEY, APIFY_API_KEY
from models.llm import get_gemini_model
from utils.web_search import web_search
from utils.helpers import format_response, needs_fallback
#from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def get_chat_response(chat_model, messages, system_prompt):
    """Get response from the chat model including filter context."""
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]

        filters = st.session_state.filters
        filter_text = (
            f"Filters:\n"
            f"- Categories: {', '.join(filters['categories'] + ([filters['other_category']] if filters['other_category'] else []))}\n"
            f"- Location: {filters['location']}\n"
            f"- Minimum Rating: {filters['min_rating']}\n"
            f"- Price Range: {filters['price']}\n"
            f"- Open Now: {'Yes' if filters['open_now'] else 'No'}\n"
            f"- Popular: {'Yes' if filters['popular'] else 'No'}\n"
            f"- Response Mode: {filters['response_mode']}"
        )
        formatted_messages.append(SystemMessage(content=filter_text))

        # Add conversation history
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))

        # Get response from model
        response = chat_model.invoke(formatted_messages)
        return response.content

    except Exception as e:
        return f"Error getting response: {str(e)}"

def instructions_page():
    st.title("The Chatbot Blueprint - Review & Recommendation Bot")
    st.markdown("This chatbot helps you find the best places to eat, shop, or explore based on reviews and ratings.")
    st.markdown("""
    ##  API Keys Setup
    - Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and set it in `config/config.py`.
    - Get your Apify API key from [Apify](https://apify.com/) and set it in `config/config.py`.
    
    ##  Filters
    Choose from categories, location, ratings, price range, and more to get personalized recommendations.

    ##  Response Modes
    Toggle between concise summaries or detailed descriptions.

    ##  Notes
    - Data is stored only for your current session and resets when you refresh.
    """)

def chat_page():
    st.title("🛍️ Review & Recommendation Bot")
    st.markdown("Find top-rated restaurants, electronics stores, malls, and more with expert reviews!")

    system_prompt = (
        "You are a friendly and energetic assistant that helps users find the best places to eat or shop. "
        "Use the provided filters and respond in the chosen style."
    )

    chat_model = get_gemini_model()

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")
        categories = st.multiselect("Select categories", ["Restaurants", "Electronics Stores", "Shopping Malls", "Grocery", "Apparel", "Others"])
        other_category = ""
        if "Others" in categories:
            other_category = st.text_input("Specify other category")

        location = st.text_input("Enter city or pin code")
        min_rating = st.slider("Minimum rating", 1.0, 5.0, 3.0, 0.1)
        price = st.selectbox("Select price range", ["$", "$$", "$$$", "$$$$"])
        open_now = st.checkbox("Open now")
        popular = st.checkbox("Popular places")
        response_mode = st.radio("Response style", ["Concise", "Detailed"])

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "categories": categories,
            "other_category": other_category,
            "location": location,
            "min_rating": min_rating,
            "price": price,
            "open_now": open_now,
            "popular": popular,
            "response_mode": response_mode
        }

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_query = st.chat_input("Ask for recommendations!")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Finding the best recommendations..."):
                try:
                    response = get_chat_response(chat_model, st.session_state.messages, system_prompt)
                    # Check if fallback is needed
                    if needs_fallback(response):
                        fallback = web_search(user_query)
                        response += "\n\n" + fallback
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_message = f"Oops! Something went wrong: {str(e)}"
                    st.markdown(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
def main():
    st.set_page_config(page_title="Review & Recommendation Bot", page_icon="🛍️", layout="wide")

    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to:", ["Chat", "Instructions"], index=0)
        if page == "Chat":
            st.divider()
            if st.button("🗑️ Clear Chat History"):
                st.session_state.messages = []
                st.rerun()

    if page == "Instructions":
        instructions_page()
    else:
        chat_page()

if __name__ == "__main__":
    main()

