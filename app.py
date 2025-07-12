from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
# import psycopg2  # 👉 Uncomment when DB is ready
# from psycopg2 import sql
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit page config
st.set_page_config(page_title="Gemini ChatBot 🤖", page_icon="💬", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        body { background-color: #f8f9fa; }
        .stApp { background-color: #ffffff; }
        .stChatMessage { font-size: 16px; line-height: 1.6; }
        .chat-input { background-color: #f1f1f1; padding: 1rem; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI ChatBot with Gemini")

# ========== Database Functions (Commented Out) ==========
# def connect_db():
#     return psycopg2.connect(
#         host=os.getenv("DB_HOST"),
#         database=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         port=os.getenv("DB_PORT")
#     )

# def create_table():
#     try:
#         conn = connect_db()
#         cur = conn.cursor()
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS query_logs (
#                 id SERIAL PRIMARY KEY,
#                 user_input TEXT,
#                 bot_response TEXT,
#                 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
#             );
#         """)
#         conn.commit()
#     except Exception as e:
#         st.error(f"❌ Database setup failed: {e}")
#     finally:
#         cur.close()
#         conn.close()

# def log_query(user_input, bot_response):
#     try:
#         conn = connect_db()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO query_logs (user_input, bot_response) VALUES (%s, %s);",
#             (user_input, bot_response)
#         )
#         conn.commit()
#     except Exception as e:
#         st.warning("⚠️ Could not log to database.")
#     finally:
#         cur.close()
#         conn.close()

# create_table()  # 👉 Only needed when DB is active

# ========== Gemini Chat ==========
def get_response(query):
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return "⚠️ Gemini API error. Please try again later."

# Session state to maintain messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Option to clear chat
if st.button("🧹 Clear Chat History"):
    st.session_state.messages = []
    st.rerun()


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Input field
user_input = st.chat_input("💬 Ask me anything...")

if user_input:
    st.chat_message("user", avatar="🧑").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🤖 Thinking..."):
        response = get_response(user_input)

    # log_query(user_input, response)  # 👉 Uncomment when DB is ready

    st.chat_message("assistant", avatar="🤖").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Optional: download chat
if st.download_button("📥 Download Chat Log", str(st.session_state.messages), file_name="chat_log.txt"):
    pass
