import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Configure Gemini API
load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Caelus - Chatbot", page_icon="🤖")
st.title("Caelus AI")
st.caption("Your AI assistant powered by Satyam Raj")

if "history" not in st.session_state:
    st.session_state.history = []

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

user_input = st.chat_input("Type your message...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.history.append(("user", user_input))

    with st.chat_message("assistant"):
        with st.spinner("Caelus is typing..."):
            try:
                response = model.generate_content(user_input)
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"⚠️ Error: {str(e)}"
            
            st.markdown(bot_reply)
            st.session_state.history.append(("assistant", bot_reply))
