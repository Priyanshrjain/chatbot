from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Function to get response (streaming or normal)
def my_output(query, stream=False):
    if stream:
        response = model.generate_content(query, stream=True)
        full_text = ""
        for chunk in response:
            if chunk.text:
                full_text += chunk.text
                yield chunk.text  # Stream partial result
        return
    else:
        response = model.generate_content(query)
        return response.text

# Streamlit App Setup
st.set_page_config(page_title="ChatBot", layout="centered")
st.title("🤖 ChatBot")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar with options
with st.sidebar:
    st.markdown("⚙️ **Settings**")
    use_streaming = st.checkbox("Stream Response (Typing Effect)", value=True)
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.experimental_rerun()

# Input and button
user_input = st.text_input("💬 Ask your question:", key="input", placeholder="Type here and press Enter or click the button...")
submit = st.button("🚀 Ask your query")

# Process user input
if user_input and (submit or True):
    st.session_state.chat_history.append(("You", user_input))

    if use_streaming:
        response_placeholder = st.empty()
        full_response = ""
        for chunk in my_output(user_input, stream=True):
            full_response += chunk
            response_placeholder.markdown(f"**🤖 Bot:** {full_response}")
        st.session_state.chat_history.append(("Bot", full_response))
    else:
        response = my_output(user_input)
        st.session_state.chat_history.append(("Bot", response))

# Show conversation
st.markdown("---")
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
