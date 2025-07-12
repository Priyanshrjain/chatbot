from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
# import psycopg2
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Streamlit Page Config ---
st.set_page_config(page_title="AI ChatBot with Gemini", page_icon="🤖", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
        .stApp {
            background-color: black;
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            text-align: center;
            color: #6F1C87;
        }
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        .message {
            background-color: #222;
            border-radius: 12px;
            padding: 12px;
            margin-top: 10px;
            color: white;
        }
        .user { background-color: #6F1C87; color: white; }
        .assistant { background-color: #333; color: white; }

        .utility-buttons {
            position: fixed;
            top: 10px;
            right: 10px;
            display: flex;
            gap: 10px;
            z-index: 1000;
        }

        .utility-buttons button {
            background-color: #6F1C87;
            color: white;
            border: none;
            padding: 6px 10px;
            border-radius: 8px;
            cursor: pointer;
        }

        .utility-buttons button:hover {
            background-color: #55106b;
        }

        .stChatInputContainer {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="utility-buttons">
        <form><button type="submit" name="clear" formmethod="post">🧹</button></form>
        <form><button type="submit" name="download" formmethod="post">💾</button></form>
    </div>
""", unsafe_allow_html=True)

st.title("🤖 AI ChatBot with Gemini")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Clear button ---
if st.session_state.get("clear"):
    st.session_state.messages = []

# --- Display chat history ---
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f"<div class='message {role_class}'><strong>{msg['role'].capitalize()}:</strong><br>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Input box ---
user_input = st.chat_input("Ask something...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # --- Gemini response ---
    try:
        response = model.generate_content(user_input)
        reply = response.text
    except Exception as e:
        reply = "⚠️ Gemini API error."

    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- Download chat history ---
if st.session_state.get("download"):
    st.download_button("Download Chat Log", str(st.session_state.messages), file_name="chat_log.txt")
