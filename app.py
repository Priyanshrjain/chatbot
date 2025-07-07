from dotenv import load_dotenv 
load_dotenv() 

import streamlit as st 
import os 
import google.generativeai as genai 

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash") 

# Function to get response from Gemini
def my_output(query):
    response = model.generate_content(query) 
    return response.text 

# Streamlit UI
st.set_page_config(page_title="Chat_BOT", layout="centered")
st.header("Chat_BOT")

# Input field and submit button
user_input = st.text_input("💬 Ask me anything:", key="input", placeholder="Type here and press Enter or click the button...")
submit = st.button("🚀 Ask your query")

# If either Enter or Button is used
if user_input and (submit or True):  # 'or True' lets it work with Enter
    response = my_output(user_input)
    st.subheader("🧠 The Response is:")
    st.write(response)
