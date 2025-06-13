import streamlit as st
import pyttsx3
import speech_recognition as sr
import nltk
import os
import threading

# Load training data
def load_training_data():
    responses = {}
    if os.path.exists("training_data.txt"):
        with open("training_data.txt", "r") as file:
            for line in file:
                if ":" in line:
                    question, answer = line.strip().split(":", 1)
                    responses[question.lower()] = answer
    return responses

def get_response(user_input, responses):
    user_input = user_input.lower()
    for question in responses:
        if question in user_input:
            return responses[question]
    return "Sorry, I don't understand that."

# Text-to-Speech with threading
def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# Speech-to-Text
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.markdown("🎤 **Listening... Speak now!**")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Sorry, network error."

# Streamlit UI
st.set_page_config(page_title="Voice & Text Chatbot", page_icon="🧠")
st.title("Smart Chatbot 🤖")

st.markdown("Type or speak your message below. This chatbot works **offline** and gives voice replies too!")

responses = load_training_data()

# Voice Input
if st.button("🎤 Speak"):
    user_query = recognize_speech()
    st.write(f"You said: {user_query}")
    bot_reply = get_response(user_query, responses)
    st.success(f"Bot: {bot_reply}")
    speak(bot_reply)

# Text Input
text_input = st.text_input("💬 Or type your message here:")
if st.button("Send") and text_input:
    bot_reply = get_response(text_input, responses)
    st.success(f"Bot: {bot_reply}")
    st.text(f"Saying: {bot_reply}")
    speak(bot_reply)
