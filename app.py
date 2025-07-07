from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit page setup
st.set_page_config(page_title="ChatBot", layout="centered")
st.title("🤖 ChatBot")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages (like a conversation)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box at bottom
user_input = st.chat_input("💬 Ask me anything...")

# Handle new input
if user_input:
    # Display and save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using Gemini
    response = model.generate_content(user_input).text

    # Display and save bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)