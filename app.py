import streamlit as st
import sqlite3
from gtts import gTTS
import speech_recognition as sr
import os

# Database Connection
conn = sqlite3.connect('english_learning.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (xp INTEGER)')
conn.commit()

# --- Functions ---
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp_audio.mp3")
    return "temp_audio.mp3"

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Bolna shuru karein...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return "Sorry, samajh nahi aaya."

# --- UI Setup ---
st.set_page_config(page_title="Guru English App", page_icon="📖")
st.title("📖 My English Learning App")

menu = ["Home", "Speaking Practice", "Vocabulary", "Progress"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("Welcome to your English Journey!")
    st.write("Yahan se aap apni learning shuru kar sakte hain.")
    

elif choice == "Speaking Practice":
    st.header("🗣️ Speaking Challenge")
    target_sentence = "I want to improve my English every day"
    st.info(f"Bolo: **{target_sentence}**")
    
    if st.button("🎤 Record & Check"):
        user_said = recognize_speech()
        st.write(f"Aapne bola: {user_said}")
        if user_said.lower() == target_sentence.lower():
            st.success("Bilkul Sahi! +10 XP")
        else:
            st.warning("Thoda aur practice karein.")

elif choice == "Vocabulary":
    st.header("📚 New Words")
    word = "Resilient"
    st.write(f"**Word:** {word} (Mazboot/Lachila)")
    if st.button("🔊 Pronunciation"):
        audio_file = text_to_speech(word)
        st.audio(audio_file)

elif choice == "Progress":
    st.header("📈 Your Performance")
    st.bar_chart([10, 20, 40, 30, 50]) # Mock data
