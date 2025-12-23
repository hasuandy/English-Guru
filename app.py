import streamlit as st
import sqlite3
import hashlib
from datetime import date, datetime
import random
import time

# --- 1. DATABASE & SESSION SETUP ---
conn = sqlite3.connect('english_guru_v32.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER, level TEXT, daily_goal INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'playback_speed' not in st.session_state: st.session_state.playback_speed = 1.0

# --- 2. THE ULTIMATE UI (GAMIFIED & CLEAN) ---
st.set_page_config(page_title="English Guru Academy", page_icon="📖", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Bungee&display=swap');
    
    .stApp { 
        background: #0e1117;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    
    .module-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #00f2ff;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .module-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.1); }

    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important; font-family: 'Bungee'; border: none; width: 100%;
    }
    
    .progress-text { font-size: 14px; color: #00f2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE LOGIC FUNCTIONS ---
def add_xp(amount, category):
    c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), amount, category))
    conn.commit()

# --- 4. APP STRUCTURE ---
if not st.session_state.logged_in:
    # --- LOGIN PAGE ---
    st.markdown("<h1 style='text-align:center; font-family:Bungee; color:#00f2ff;'>GURU ACADEMY</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        mode = st.tabs(["🔑 Login", "🛡️ Register"])
        with mode[0]:
            e = st.text_input("Email")
            p = st.text_input("Password", type='password')
            if st.button("ENTER"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with mode[1]:
            ne = st.text_input("New Email")
            nu = st.text_input("Name")
            np = st.text_input("Create Password", type='password')
            if st.button("CREATE ACCOUNT"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0,"Beginner",50)', (ne, nu, h))
                conn.commit(); st.success("Success!"); st.rerun()

else:
    # --- MAIN SIDEBAR ---
    with st.sidebar:
        st.markdown(f"## ⚡ {st.session_state.user}")
        page = st.radio("LEARNING HUB", ["📊 Dashboard", "📚 Vocabulary (SRS)", "✍️ Grammar", "🎧 Listening", "🗣️ Speaking Practice", "🎮 Daily Quest"])
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

    # --- 1. DASHBOARD (Progress Tracking & Goals) ---
    if page == "📊 Dashboard":
        st.title("Your Learning Path")
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        total_xp = c.fetchone()[0] or 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total XP", total_xp)
        col2.metric("Level", "Intermediate" if total_xp > 500 else "Beginner")
        col3.metric("Streak", "3 Days 🔥") # Logic can be added for dates
        
        st.markdown("### 🎯 Weekly Goal Status")
        goal_progress = (total_xp % 100) / 100
        st.progress(goal_progress)
        st.write(f"You are {int(goal_progress*100)}% close to your weekly goal!")

    # --- 2. VOCABULARY (SRS & Flashcards) ---
    elif page == "📚 Vocabulary (SRS)":
        st.title("Interactive Flashcards")
        words = [
            {"w": "Ephemeral", "m": "Lasting for a very short time.", "e": "Fame is ephemeral."},
            {"w": "Resilient", "m": "Able to recoil or spring back into shape.", "e": "She is a resilient girl."}
        ]
        word = random.choice(words)
        with st.container():
            st.markdown(f"<div class='module-card'><h1>{word['w']}</h1><p><i>Spaced Repetition Active</i></p></div>", unsafe_allow_html=True)
            if st.button("Show Meaning"):
                st.info(f"**Meaning:** {word['m']}\n\n**Example:** {word['e']}")
                add_xp(5, "Vocabulary")

    # --- 3. GRAMMAR (Structured Lessons) ---
    elif page == "✍️ Grammar":
        st.title("Grammar Modules")
        topic = st.selectbox("Choose Topic", ["Tenses", "Prepositions", "Articles"])
        st.markdown(f"<div class='module-card'><h3>Mastering {topic}</h3><p>Detailed explanation and practice exercises below.</p></div>", unsafe_allow_html=True)
        q = st.radio("Fill in the blank: 'I ___ to the gym yesterday.'", ["go", "gone", "went", "goes"])
        if st.button("Check Answer"):
            if q == "went":
                st.success("Correct! 'Went' is the past tense of 'go'."); add_xp(10, "Grammar")
            else: st.error("Wrong! Try again.")

    # --- 4. LISTENING (Adjustable Speed) ---
    elif page == "🎧 Listening":
        st.title("Listening Immersion")
        st.session_state.playback_speed = st.slider("Playback Speed", 0.5, 2.0, 1.0)
        st.info(f"Playing content at {st.session_state.playback_speed}x speed.")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder
        st.markdown("### Transcript\n'The quick brown fox jumps over the lazy dog...'")

    # --- 5. SPEAKING (Roleplay & Shadowing) ---
    elif page == "🗣️ Speaking Practice":
        st.title("Speaking Arena")
        st.markdown("<div class='module-card'><h4>Scenario: Ordering Coffee</h4><p>Repeat after the prompt to improve intonation.</p></div>", unsafe_allow_html=True)
        st.write("Prompt: 'I would like a large latte, please.'")
        if st.button("🎙️ Tap to Speak (Simulation)"):
            st.warning("Speech recognition simulation: Your pronunciation score is 85%")
            add_xp(20, "Speaking")

    # --- 6. DAILY QUEST (Gamification) ---
    elif page == "🎮 Daily Quest":
        st.title("Boss Battle: The Verb Monster")
        st.markdown("")
        st.write("Defeat the monster by answering 5 questions correctly!")
        # Reuse previous Boss Battle logic here
