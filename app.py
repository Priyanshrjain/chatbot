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

.custom-button-container {
    position: absolute;
    top: 10px;
    right: 15px;
    display: flex;
    gap: 0.5rem;
}
.icon-button {
    background-color: #8F00FF;
    border: none;
    color: white;
    border-radius: 5px;
    padding: 0.4rem 0.5rem;
    cursor: pointer;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>Welcome to <span style='color:#8F00FF;'>AskNova</span></h1>", unsafe_allow_html=True)

# Clear Chat Button (top right)
with st.container():
    st.markdown("""
    <div class="custom-button-container">
        <form action="" method="post">
            <button class="icon-button" name="clear" type="submit">🪄</button>
        </form>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get("clear"):
        st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    st.chat_message(role).markdown(content)

# Input field
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
