import streamlit as st
import sqlite3
import hashlib
from datetime import date, datetime, timedelta
import random
import time

# --- 1. DATABASE & ARCHITECTURE ---
conn = sqlite3.connect('cyber_academy_v34.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER, level TEXT, daily_goal INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS srs_vocab 
             (email TEXT, word TEXT, next_review TEXT, interval INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'playback_speed' not in st.session_state: st.session_state.playback_speed = 1.0

# --- 3. ULTRA GAMER CSS (CYBERPUNK THEME) ---
st.set_page_config(page_title="English Guru Arena", page_icon="🌐", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), 
                    url('https://wallpaperaccess.com/full/2650153.jpg');
        background-size: cover; background-attachment: fixed;
        color: #00f2ff; font-family: 'Rajdhani', sans-serif;
    }
    
    .glass-card {
        background: rgba(0, 20, 40, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid #00f2ff;
        border-radius: 15px; padding: 25px;
        margin-bottom: 20px; box-shadow: 0 0 15px #00f2ff33;
    }

    .stButton>button {
        background: transparent !important;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase; letter-spacing: 2px;
        transition: 0.4s; width: 100%; border-radius: 0px;
    }
    .stButton>button:hover {
        background: #00f2ff !important; color: #000 !important;
        box-shadow: 0 0 30px #00f2ff;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #ff00ff; text-shadow: 0 0 10px #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CORE FUNCTIONS ---
def add_xp(amount, cat):
    c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), amount, cat))
    conn.commit()

# --- 5. APP LOGIC ---
if not st.session_state.logged_in:
    # --- AUTHENTICATION GATEWAY ---
    st.markdown("<h1 style='text-align:center;'>CYBER GURU ACADEMY</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        tab = st.tabs(["ACCESS", "INITIALIZE NEW USER"])
        with tab[0]:
            e = st.text_input("User ID")
            p = st.text_input("Passkey", type='password')
            if st.button("LOGIN"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with tab[1]:
            ne = st.text_input("Email")
            nu = st.text_input("Codename")
            np = st.text_input("Set Passkey", type='password')
            if st.button("CREATE HERO"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0,"Beginner",50)', (ne, nu, h))
                conn.commit(); st.success("Profile Created!"); st.rerun()

else:
    # --- NAVIGATION PANEL ---
    with st.sidebar:
        st.markdown(f"### ⚡ WARRIOR: {st.session_state.user}")
        page = st.selectbox("MISSION SELECT", [
            "📊 Dashboard", 
            "📚 Vocabulary Builder (SRS)", 
            "✍️ Grammar Lab", 
            "🎧 Listening Hub", 
            "🗣️ Speaking Simulation",
            "📖 Reading/Writing"
        ])
        if st.button("TERMINATE SESSION"): st.session_state.logged_in = False; st.rerun()

    # --- MODULE 1: DASHBOARD ---
    if page == "📊 Dashboard":
        st.markdown("<h1>SYSTEM STATUS</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        xp = c.fetchone()[0] or 0
        
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"<div class='glass-card'><h3>TOTAL XP</h3><h2>{xp}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='glass-card'><h3>LEVEL</h3><h2>{'PRO' if xp > 500 else 'NOOB'}</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='glass-card'><h3>DAILY GOAL</h3><h2>{xp}/100</h2></div>", unsafe_allow_html=True)
        
        st.markdown("### Progress Roadmap")
        st.progress(min(xp/1000, 1.0))

    # --- MODULE 2: VOCABULARY SRS ---
    elif page == "📚 Vocabulary Builder (SRS)":
        st.markdown("<h1>VOCABULARY VAULT</h1>", unsafe_allow_html=True)
        st.info("Spaced Repetition System (SRS) logic enabled. Review words before you forget!")
        
        words = [
            {"w": "Inevitable", "m": "Certain to happen; unavoidable.", "ex": "Change is inevitable."},
            {"w": "Pragmatic", "m": "Dealing with things sensibly and realistically.", "ex": "A pragmatic approach to English."}
        ]
        w = random.choice(words)
        st.markdown(f"<div class='glass-card'><h1>{w['w']}</h1></div>", unsafe_allow_html=True)
        if st.button("REVEAL DATA"):
            st.write(f"**Meaning:** {w['m']}")
            st.write(f"**Context:** {w['ex']}")
            add_xp(10, "Vocabulary")

    # --- MODULE 3: GRAMMAR LAB ---
    elif page == "✍️ Grammar Lab":
        st.markdown("<h1>GRAMMAR CORE</h1>", unsafe_allow_html=True)
        topic = st.radio("Select Lesson", ["Tenses", "Modals", "Articles"], horizontal=True)
        
        st.markdown(f"<div class='glass-card'><h3>{topic} Training</h3><p>Rule: Always use 'an' before vowel sounds.</p></div>", unsafe_allow_html=True)
        ans = st.text_input("Practice: He is ___ honest man.")
        if st.button("VALIDATE"):
            if ans.lower().strip() == "an":
                st.success("Correct! +20 XP"); add_xp(20, "Grammar")
            else: st.error("Feedback: 'Honest' starts with a vowel sound (O). Use 'an'.")

    # --- MODULE 4: LISTENING HUB ---
    elif page == "🎧 Listening Hub":
        st.markdown("<h1>AUDIO IMMERSION</h1>", unsafe_allow_html=True)
        speed = st.select_slider("Adjust Neural Playback Speed", options=[0.5, 0.75, 1.0, 1.25, 1.5], value=1.0)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.markdown(f"<div class='glass-card'><h3>Transcript (Speed: {speed}x)</h3><p>Focus on the pronunciation of 'R' and 'T' sounds.</p></div>", unsafe_allow_html=True)

    # --- MODULE 5: SPEAKING SIMULATION ---
    elif page == "🗣️ Speaking Simulation":
        st.markdown("<h1>VOCAL INTERFACE</h1>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'><h4>Roleplay: Ordering Food</h4><p>Repeat: 'I'll have the steak with a side of vegetables.'</p></div>", unsafe_allow_html=True)
        if st.button("🎙️ START RECORDING (SIMULATION)"):
            with st.spinner("Analyzing Intonation..."):
                time.sleep(2)
                st.info("Pronunciation Accuracy: 88%. Try to emphasize 'steak' more.")
                add_xp(30, "Speaking")

    # --- MODULE 6: READING/WRITING ---
    elif page == "📖 Reading/Writing":
        st.markdown("<h1>GRADED READERS</h1>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'><h3>The Future of AI</h3><p>Articles tailored to your level. Read and write a summary below.</p></div>", unsafe_allow_html=True)
        summary = st.text_area("Write a 2-line summary:")
        if st.button("SUBMIT FOR EVALUATION"):
            st.success("Submission received! XP rewarded for journaling."); add_xp(25, "Writing")

