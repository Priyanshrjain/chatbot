from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
# import psycopg2  # Uncomment when connecting database
# from psycopg2 import sql
# from datetime import datetime

# Load .env variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Uncomment if using PostgreSQL database
"""
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def create_table():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS query_logs (
                id SERIAL PRIMARY KEY,
                user_input TEXT,
                bot_response TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
            '''
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")
"""

# Styling
st.set_page_config(page_title="AskNova - AI Chatbot", layout="centered")

st.markdown("""
    <style>
        body, .stApp {
            background-color: #0e0e0e;
            color: white;
        }

        .title-container {
            text-align: center;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }

        .title-container h1 {
            font-size: 2.5rem;
            font-weight: 600;
            margin: 0;
        }

        .title-accent {
            color: #6F1C87;
        }

        .chat-bubble-user {
            background-color: #6F1C87;
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .chat-bubble-assistant {
            background-color: #333;
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }

        .stChatInputContainer {
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <div class="title-container">
        <h1>
            <span style="color: white;">Welcome to </span>
            <span class="title-accent">AskNova</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Top-right buttons
col1, col2 = st.columns([10, 1])
with col2:
    clear = st.button("🧹", help="Clear Chat")
    download = st.download_button("💾", str(st.session_state.messages), file_name="asknova_chat_log.txt", help="Download Chat")

if clear:
    st.session_state.messages = []
    st.rerun()

# Chat history
for msg in st.session_state.messages:
    bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
    st.markdown(f"""<div class="{bubble_class}">{msg["content"]}</div>""", unsafe_allow_html=True)

# Input
user_input = st.chat_input("Ask something...")

def get_response(prompt):
    try:
        res = model.generate_content(prompt)
        return res.text
    except:
        return "⚠️ Sorry, something went wrong."

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"""<div class="chat-bubble-user">{user_input}</div>""", unsafe_allow_html=True)

    with st.spinner("⏳ Fetching response..."):
        response = get_response(user_input)

    # Log to DB (uncomment if needed)
    # log_query(user_input, response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f"""<div class="chat-bubble-assistant">{response}</div>""", unsafe_allow_html=True)
