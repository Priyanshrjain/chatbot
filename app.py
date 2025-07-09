from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import psycopg2

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

# PostgreSQL database connection
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

# Create table if not exists
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS query_logs (
        id SERIAL PRIMARY KEY,
        user_input TEXT,
        bot_response TEXT
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Log each chat to the DB
def log_query(user_input, bot_response):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO query_logs (user_input, bot_response) VALUES (%s, %s);", (user_input, bot_response))
    conn.commit()
    cur.close()
    conn.close()

# Function to generate Gemini response
def my_output(query):
    response = model.generate_content(query)
    return response.text

# Call once to ensure table exists
create_table()

# Streamlit page setup
st.set_page_config(page_title="ChatBot", layout="centered")
st.title("🤖 ChatBot with PostgreSQL Logging")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("💬 Ask me anything...")

# Handle user input
if user_input:
    # Show and save user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    response = my_output(user_input)

    # Log to PostgreSQL
    log_query(user_input, response)

    # Show and save assistant response
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
