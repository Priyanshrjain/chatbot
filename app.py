from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
# import psycopg2
# from psycopg2 import sql

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Set Streamlit page config
st.set_page_config(page_title="AI ChatBot", page_icon="🤖", layout="centered")

# Custom CSS Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
            color: white;
        }
        .stChatMessage {
            font-size: 16px;
            line-height: 1.6;
        }
        .chat-message.user {
            background-color: #6F1C87;
            color: white;
            border-radius: 8px;
            padding: 8px;
        }
        .chat-message.assistant {
            background-color: #2e2e2e;
            color: white;
            border-radius: 8px;
            padding: 8px;
        }
        .top-buttons {
            position: fixed;
            top: 15px;
            right: 20px;
            z-index: 100;
        }
        .top-buttons button {
            background-color: #6F1C87;
            border: none;
            border-radius: 8px;
            padding: 8px 10px;
            color: white;
            cursor: pointer;
            margin-left: 5px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🤖 AI ChatBot with Gemini</h1>", unsafe_allow_html=True)

# Top-right floating buttons
st.markdown("""
    <div class="top-buttons">
        <form action="/" method="get" style="display:inline;">
            <button type="submit">🧹</button>
        </form>
        <a download="chat_log.txt" href="data:text/plain;charset=utf-8,{text}" target="_blank">
            <button>📂</button>
        </a>
    </div>
""".replace("{text}", str(st.session_state.get("messages", "")).replace("\n", "%0A")), unsafe_allow_html=True)

# Optional PostgreSQL functions (commented for now)
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
#         cur.close()
#         conn.close()
#     except Exception as e:
#         st.error(f"Database setup error: {e}")

# def log_query(user_input, bot_response):
#     try:
#         conn = connect_db()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO query_logs (user_input, bot_response) VALUES (%s, %s);", (user_input, bot_response))
#         conn.commit()
#         cur.close()
#         conn.close()
#     except Exception as e:
#         st.warning("Could not log to database.")

# def get_response

def get_response(query):
    try:
        with st.spinner("🤖 Gemini is thinking..."):
            response = model.generate_content(query)
            return response.text
    except Exception as e:
        return "⚠️ Gemini API error. Please try again later."

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask something...")
if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_response(user_input)
    # log_query(user_input, response)  # DB logging (optional)

    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
