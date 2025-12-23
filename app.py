import streamlit as st
import sqlite3
from datetime import date
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai

# --- 1. AI SETUP ---
# Aapki Key maine yahan fix kar di hai
API_KEY = "AIzaSyBWcggAXS3KYXl4LPMi1bWQkYqZUQ3b3c4"

try:
    genai.configure(api_key=API_KEY)
    # 404 Error fix karne ke liye hum 'gemini-pro' use kar rahe hain
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    model = None

# --- 2. PAGE CONFIG & DESIGN ---
st.set_page_config(page_title="English Guru Pro", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #1E2630; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { 
        background-color: #4CAF50; 
        color: white; 
        border-radius: 10px; 
        border: none;
        padding: 10px;
        width: 100%;
    }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE SETUP ---
conn = sqlite3.connect('english_guru.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS progress (date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (word TEXT, meaning TEXT)''')
conn.commit()

# --- 4. FUNCTIONS ---
def add_xp(amount):
    today = str(date.today())
    c.execute("INSERT INTO progress VALUES (?, ?)", (today, amount))
    conn.commit()

def get_total_xp():
    c.execute("SELECT SUM(xp) FROM progress")
    res = c.fetchone()[0]
    return res if res else 0

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3892/3892258.png", width=80)
    st.title("English Guru")
    st.markdown(f"### ⭐ Total XP: {get_total_xp()}")
    st.divider()
    menu = st.radio("Menu", ["🏠 Home", "🎙️ Speaking", "✍️ Writing", "🤖 AI Tutor Chat", "🗂️ Dictionary"])

# --- 6. MAIN PAGES ---

# --- HOME PAGE ---
if menu == "🏠 Home":
    st.title("🎓 Welcome back, Learner!")
    st.subheader("Aapka Progress")
    xp = get_total_xp()
    st.progress(min(xp / 1000, 1.0))
    st.write(f"Goal: {xp}/1000 XP tak pahunchna hai!")
    st.info("💡 Tip: AI Tutor se rozana 5 naye sentence check karwayein.")

# --- SPEAKING PRACTICE ---
elif menu == "🎙️ Speaking":
    st.title("🎙️ Speaking Practice")
    target_text = "Practice makes a man perfect."
    st.info(f"Boliye: **'{target_text}'**")
    
    audio = mic_recorder(start_prompt="🎤 Start Recording", stop_prompt="🛑 Stop", key='recorder')
    
    if audio:
        if len(audio['bytes']) > 2000:
            st.audio(audio['bytes'])
            st.success("Awaaz record ho gayi! Match kijiye.")
            if st.button("Claim 10 XP"):
                add_xp(10)
                st.rerun()
        else:
            st.warning("Kuch sunaai nahi diya, fir se boliye.")

# --- WRITING PRACTICE ---
elif menu == "✍️ Writing":
    st.title("✍️ Writing Challenge")
    st.write("Topic: **'My Best Friend'** (Kam se kam 10 words likhiye)")
    user_text = st.text_area("Yahan likhiye:", height=150)
    
    if st.button("Submit Writing"):
        if len(user_text.split()) >= 10:
            st.balloons()
            st.success("Great job! +20 XP Earned.")
            add_xp(20)
        else:
            st.warning("Thoda aur likhiye points earn karne ke liye.")

# --- AI TUTOR CHAT ---
elif menu == "🤖 AI Tutor Chat":
    st.title("🤖 AI Grammar Tutor")
    st.write("Mujhse English mein baat kijiye, main aapki galtiyan sudharunga.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat history dikhana
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type here (e.g., 'I goes to market')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.spinner("Guru soch raha hai..."):
                if model:
                    ai_query = f"You are a helpful English teacher. If the student's sentence is wrong, correct it and explain why in 1-2 simple lines. If it's correct, reply normally. Student said: '{prompt}'"
                    response = model.generate_content(ai_query)
                    reply = response.text
                else:
                    reply = "Sorry, AI connects nahi ho pa raha. Key check karein."

                with st.chat_message("assistant"):
                    st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")

# --- DICTIONARY ---
elif menu == "🗂️ Dictionary":
    st.title("🗂️ My Word Bank")
    col1, col2 = st.columns(2)
    with col1:
        new_word = st.text_input("Naya Word:")
    with col2:
        meaning = st.text_input("Meaning (Hindi/English):")
    
    if st.button("Add to Dictionary"):
        if new_word and meaning:
            c.execute("INSERT INTO dictionary VALUES (?, ?)", (new_word, meaning))
            conn.commit()
            st.success(f"'{new_word}' save ho gaya!")
            st.rerun()

    st.write("---")
    words = c.execute("SELECT * FROM dictionary").fetchall()
    for w in words:
        st.write(f"🔹 **{w[0]}**: {w[1]}")

