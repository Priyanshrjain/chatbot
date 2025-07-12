from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
# import psycopg2  # Uncomment when DB is ready
# from psycopg2 import sql

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# Streamlit page config
st.set_page_config(page_title="Gemini ChatBot 🤖", page_icon="🤖", layout="centered")

# Custom CSS for better UI
st.markdown("""
    <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
        }
        .chat-box {
            background-color: #f1f3f6;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .user-msg { background-color: #d0e6ff; }
        .bot-msg { background-color: #ffffff; }
        .btn-row {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

st.title("🤖 AI ChatBot with Gemini")

# === Database functions (commented out) ===
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

# Function to generate Gemini response
def get_response(query):
    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return "⚠️ Gemini API error. Please try again later."

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    role_class = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f"<div class='chat-box {role_class}'><b>{msg['role'].capitalize()}:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# Input area
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # log_query(user_input, response)  # Uncomment when DB is ready

# Buttons aligned bottom right
st.markdown("<div class='btn-row'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.download_button("📥 Download Chat", str(st.session_state.messages), file_name="chat_log.txt")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
