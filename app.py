import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit page config
st.set_page_config(page_title="AskNova", page_icon="🌌", layout="centered")

# Custom CSS styling
st.markdown("""
<style>
body {
    background-color: #0C0C1D;
}
.stApp {
    background: linear-gradient(to bottom right, #0C0C1D, #0F0F22);
    color: white;
}
h1 {
    font-size: 3em;
    font-weight: bold;
    text-align: center;
    padding-top: 2rem;
    background: linear-gradient(to right, #8F00FF, #6F1C87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stChatMessage {
    font-size: 16px;
    line-height: 1.6;
}
.stTextInput>div>div>input {
    border: 1px solid #8F00FF;
}
.css-1y4p8pa.edgvbvh3 {
    padding: 1.5rem;
}
header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>Welcome to <span style='color:#8F00FF;'>AskNova</span></h1>", unsafe_allow_html=True)

# -------------------------------
# Uncomment and use below for database support
# import psycopg2
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
#         cur.execute('''CREATE TABLE IF NOT EXISTS query_logs (
#             id SERIAL PRIMARY KEY,
#             user_input TEXT,
#             bot_response TEXT,
#             created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
#         );''')
#         conn.commit()
#         cur.close()
#         conn.close()
#     except Exception as e:
#         print(f"Database error: {e}")

# def log_query(user_input, bot_response):
#     try:
#         conn = connect_db()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO query_logs (user_input, bot_response) VALUES (%s, %s);",
#             (user_input, bot_response)
#         )
#         conn.commit()
#         cur.close()
#         conn.close()
#     except:
#         pass
# -------------------------------

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    st.chat_message(role).markdown(content)

# Chat input
user_input = st.chat_input("Ask something...")

if user_input:
    st.chat_message("user").markdown(f"**{user_input}**")
    st.session_state.messages.append({"role": "user", "content": f"**{user_input}**"})

    with st.spinner("🔮 AskNova is generating a thoughtful response..."):
        try:
            response = model.generate_content(user_input)
            reply = response.text
        except Exception:
            reply = "❌ Sorry, something went wrong while generating a response."

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # log_query(user_input, reply)  # Uncomment when database is connected
