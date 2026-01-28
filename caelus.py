import streamlit as st
import google.generativeai as genai
import os

# REMOVED: from dotenv import load_dotenv
# REMOVED: load_dotenv()

st.set_page_config(page_title="Caelus - Chatbot", page_icon="🤖")
st.title("Caelus AI")
st.caption("Your AI assistant powered by Satyam Raj")

# CORRECTED: Get the key from Streamlit Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    st.error("Secrets not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

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
