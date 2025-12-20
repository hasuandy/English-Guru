import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_final.db', check_same_thread=False)
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

# --- 3. ULTRA ATTRACTIVE CSS ---
st.set_page_config(page_title="English Guru", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@500;900&family=Rajdhani:wght@600&display=swap');
    
    .stApp {
        background: #050505;
        background-image: linear-gradient(0deg, rgba(0,0,0,0.9) 0%, rgba(20,20,40,0.8) 100%), 
                          url('https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        color: #00f2ff;
        font-family: 'Rajdhani', sans-serif;
    }

    .brand-title {
        font-family: 'Bungee', cursive;
        font-size: 5rem;
        text-align: center;
        background: linear-gradient(90deg, #00f2ff, #ff00ff, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 3s ease-in-out infinite alternate;
        margin-top: -50px;
    }
    @keyframes glow { from { text-shadow: 0 0 10px #00f2ff; } to { text-shadow: 0 0 30px #ff00ff; } }

    .glass-card {
        background: rgba(10, 10, 30, 0.7);
        backdrop-filter: blur(15px);
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        margin-bottom: 25px;
        text-align: center;
    }

    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important;
        font-family: 'Bungee' !important;
        border-radius: 12px !important;
        height: 55px;
        width: 100%;
        border: none !important;
        transition: 0.4s;
        font-size: 1.2rem !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px #00f2ff;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(0,0,0,0.95) !important;
        border-right: 2px solid #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["⚡ LOGIN", "🛡️ NEW WARRIOR"])
        with tab1:
            e = st.text_input("Warrior Email")
            p = st.text_input("Access Key", type='password')
            if st.button("ENTER PORTAL"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with tab2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Hero Name"), st.text_input("Set Passkey", type='password')
            if st.button("CREATE PROFILE"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                conn.commit(); st.balloons(); st.success("Profile Activated!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff00ff; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("CHOOSE MISSION", ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab"], key="nav_key", on_change=set_page)
        st.write("---")
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    page = st.session_state.user_page
    
    if page == "📊 Dashboard":
        st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        xp_res = c.fetchone()
        xp = xp_res[0] if xp_res and xp_res[0] else 0
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='glass-card'><h3>🏆 XP</h3><h1 style='color:#00f2ff;'>{xp}</h1></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'><h3>🎖️ RANK</h3><h1 style='color:#ff00ff;'>{'ELITE' if xp > 100 else 'NOOB'}</h1></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'><h3>🔥 LEVEL</h3><h1 style='color:#00f2ff;'>{1+xp//100}</h1></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'><h3>PROGRESS TO NEXT LEVEL</h3>", unsafe_allow_html=True)
        st.progress(min((xp % 100)/100, 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "📚 Vocab Vault":
        st.markdown("<h1 style='text-align:center;'>VOCABULARY VAULT</h1>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'><h3>WORD OF THE DAY</h3><h1 style='font-size:4rem; color:#00f2ff;'>'RESILIENT'</h1><p>Meaning: Able to recover quickly from difficulties.</p></div>", unsafe_allow_html=True)
        if st.button("CLAIM 10 XP"):
            c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), 10, "Vocab"))
            conn.commit(); st.toast("XP SECURED!"); time.sleep(1); st.rerun()

    elif page == "✍️ Grammar Lab":
        st.markdown("<h1 style='text-align:center;'>GRAMMAR CORE</h1>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'><h3>COMPLETE THE STRIKE:</h3><p style='font-size:1.5rem;'>'He ____ (study) every single day.'</p></div>", unsafe_allow_html=True)
        ans = st.text_input("INPUT VERB:")
        if st.button("VALIDATE"):
            if ans.lower().strip() == "studies":
                st.balloons()
                c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), 20, "Grammar"))
                conn.commit(); st.success("PERFECT HIT! +20 XP"); time.sleep(1); st.rerun()
            else:
                st.error("MISSED! Try Again.")
