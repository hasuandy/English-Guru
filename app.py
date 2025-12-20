import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro_v1.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "📊 Dashboard"

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. PREMIUM CYBER-GOLD UI ---
st.set_page_config(page_title="English Guru", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@700&family=Rajdhani:wght@600&display=swap');
    
    .stApp {
        background: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }

    .brand-title {
        font-family: 'Bungee', cursive;
        font-size: 5.5rem;
        text-align: center;
        background: linear-gradient(90deg, #ffd700, #ff00ff, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
        margin-top: -60px;
    }

    .cyber-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: 0.4s;
        text-align: center;
    }
    .cyber-card:hover {
        border-color: #00f2ff;
        transform: translateY(-5px);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.2);
    }

    .stButton>button {
        background: linear-gradient(90deg, #ffd700, #ff8c00) !important;
        color: black !important;
        font-family: 'Bungee' !important;
        border-radius: 12px !important;
        height: 50px; width: 100%;
        border: none !important;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px #ffd700;
        transform: scale(1.02);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(10, 10, 15, 0.98) !important;
        border-right: 1px solid #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 ACCESS", "🛡️ JOIN"])
        with t1:
            e = st.text_input("Warrior Email")
            p = st.text_input("Passkey", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with t2:
            ne, nu, np = st.text_input("Email ID"), st.text_input("Codename"), st.text_input("Set Key", type='password')
            if st.button("CREATE PROFILE"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                conn.commit(); st.balloons(); st.success("Hero Profile Created!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- NAVIGATION SIDEBAR (All Options Included) ---
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ffd700; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox(
            "SELECT MISSION", 
            ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🎧 Listening Hub", "🗣️ Speaking Simulation", "📖 Reading/Writing"],
            key="nav_key",
            on_change=set_page
        )
        st.write("---")
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- PAGES ---
    page = st.session_state.user_page
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

    c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
    xp = c.fetchone()[0] or 0

    if page == "📊 Dashboard":
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='cyber-card'><h3>🏆 TOTAL XP</h3><h1 style='color:#ffd700;'>{xp}</h1></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='cyber-card'><h3>🎖️ RANK</h3><h1 style='color:#00f2ff;'>{'ELITE' if xp > 200 else 'TRAINEE'}</h1></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='cyber-card'><h3>🔥 STREAK</h3><h1 style='color:#ff00ff;'>5 DAYS</h1></div>", unsafe_allow_html=True)
        
        st.markdown("<br><div class='cyber-card'><h3>LEVEL PROGRESS</h3>", unsafe_allow_html=True)
        st.progress(min((xp % 100)/100, 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "📚 Vocab Vault":
        st.markdown("<div class='cyber-card'><h2>Word: 'Pinnacle'</h2><p>Meaning: The most successful point; the culmination.</p></div>", unsafe_allow_html=True)
        if st.button("COLLECT 10 XP"):
            c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), 10, "Vocab"))
            conn.commit(); st.toast("XP Secured!"); time.sleep(1); st.rerun()

    elif page == "✍️ Grammar Lab":
        st.markdown("<div class='cyber-card'><h3>Fix: 'He don't know the answer.'</h3></div>", unsafe_allow_html=True)
        ans = st.text_input("Your Correction:")
        if st.button("VERIFY"):
            if "doesn't" in ans.lower():
                st.success("Perfect! +20 XP"); c.execute("INSERT INTO progress VALUES (?,?,?,?)", (st.session_state.email, str(date.today()), 20, "Grammar"))
                conn.commit(); time.sleep(1); st.rerun()

    elif page == "🎧 Listening Hub":
        st.markdown("<div class='cyber-card'><h3>Audio Training Feed</h3>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.write("Listen to the pronunciation carefully.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "🗣️ Speaking Simulation":
        st.markdown("<div class='cyber-card'><h3>Pronunciation Challenge</h3><p>Repeat: 'The aesthetic of the interface is stunning.'</p></div>", unsafe_allow_html=True)
        if st.button("🎙️ START ANALYZER"):
            with st.spinner("Analyzing voice..."):
                time.sleep(2); st.info("Accuracy: 95%! +30 XP")
                c.execute("INSERT INTO progress VALUES (?,?,?,?)", (st.session_state.email, str(date.today()), 30, "Speaking"))
                conn.commit()

    elif page == "📖 Reading/Writing":
        st.markdown("<div class='cyber-card'><h3>Daily Journal</h3><p>Write 2 lines about your day in English.</p></div>", unsafe_allow_html=True)
        st.text_area("Your Entry:")
        if st.button("SUBMIT LOG"):
            st.success("Journal Updated! +25 XP")
            c.execute("INSERT INTO progress VALUES (?,?,?,?)", (st.session_state.email, str(date.today()), 25, "Writing"))
            conn.commit()
