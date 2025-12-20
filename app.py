import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v43.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

# --- 2. SESSION STATE (Important Fix) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_page' not in st.session_state: st.session_state.current_page = "📊 Dashboard"

# --- 3. THE "AMAZING" UI ---
st.set_page_config(page_title="English Guru", page_icon="🎓", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    .stApp { background: #050505; color: #00f2ff; font-family: 'Rajdhani', sans-serif; }
    
    .brand-title {
        font-family: 'Bungee', cursive;
        color: #ff00ff; font-size: 4rem; text-align: center;
        text-shadow: 0 0 15px #ff00ff, 0 0 30px #00f2ff;
        margin-bottom: 20px;
    }

    .cyber-card {
        background: rgba(20, 20, 35, 0.8);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 20px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important; font-family: 'Bungee' !important;
        border: none !important; border-radius: 10px !important;
        width: 100%; transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNCTIONS ---
def change_page(page_name):
    st.session_state.current_page = page_name

# --- 5. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        tab = st.tabs(["⚡ LOGIN", "🛠️ SIGNUP"])
        with tab[0]:
            e = st.text_input("Email")
            p = st.text_input("Passkey", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with tab[1]:
            ne, nu, np = st.text_input("New Email"), st.text_input("Codename"), st.text_input("New Passkey", type='password')
            if st.button("CREATE HERO"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                conn.commit(); st.success("Created!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Navigation Sidebar with Session State
    with st.sidebar:
        st.markdown(f"<h2 style='color:#ff00ff; font-family:Bungee;'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
        # Selectbox ko session_state se connect kiya
        st.session_state.current_page = st.selectbox(
            "MISSION SELECT", 
            ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🎧 Listening Hub"],
            index=["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🎧 Listening Hub"].index(st.session_state.current_page)
        )
        if st.button("ABORT MISSION"): st.session_state.logged_in = False; st.rerun()

    # --- PAGES ---
    if st.session_state.current_page == "📊 Dashboard":
        st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        xp_res = c.fetchone()
        xp = xp_res[0] if xp_res and xp_res[0] else 0
        
        col1, col2 = st.columns(2)
        col1.markdown(f"<div class='cyber-card'><h3>🏆 XP POINTS</h3><h2>{xp}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='cyber-card'><h3>🎖️ RANK</h3><h2>{'ELITE' if xp > 100 else 'NOOB'}</h2></div>", unsafe_allow_html=True)

    elif st.session_state.current_page == "📚 Vocab Vault":
        st.markdown("<h1>VOCABULARY VAULT</h1>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h2>Word: 'Eloquent'</h2><p>Meaning: Fluent or persuasive in speaking or writing.</p></div>", unsafe_allow_html=True)
        if st.button("CLAIM 10 XP"):
            c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), 10, "Vocab"))
            conn.commit(); st.toast("XP Added!"); st.rerun()

    elif st.session_state.current_page == "✍️ Grammar Lab":
        st.markdown("<h1>GRAMMAR CORE</h1>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h3>Mission: Identify the Error</h3><p>'She go to the park everyday.'</p></div>", unsafe_allow_html=True)
        ans = st.text_input("Correct the verb:")
        if st.button("STRIKE"):
            if ans.lower() == "goes":
                st.success("Correct! +20 XP")
                c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), 20, "Grammar"))
                conn.commit()
            else: st.error("Wrong!")

    elif st.session_state.current_page == "🎧 Listening Hub":
        st.markdown("<h1>AUDIO ROOM</h1>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.info("Listen and take notes to improve your score.")
