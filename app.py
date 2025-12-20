import streamlit as st
import sqlite3
import hashlib
from datetime import date
import time

# --- 1. DATABASE SETUP & AUTO-REPAIR ---
conn = sqlite3.connect('english_guru_v99.db', check_same_thread=False)
c = conn.cursor()

# Tables create/update logic
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')

# Auto-add missing columns to avoid TypeErrors
try:
    c.execute("ALTER TABLE users ADD COLUMN goal INTEGER DEFAULT 50")
except:
    pass # Column already exists

conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "📊 Dashboard"

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. THE ULTIMATE ATTRACTIVE UI ---
st.set_page_config(page_title="English Guru Pro", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    .stApp {
        background: #050505;
        background-image: radial-gradient(circle at center, #1a1a3a 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }

    .brand-title {
        font-family: 'Bungee', cursive;
        font-size: 5rem;
        text-align: center;
        background: linear-gradient(90deg, #ffd700, #ff00ff, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(0, 242, 255, 0.4));
        margin-top: -60px;
    }

    .cyber-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.4);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.7);
        text-align: center;
        margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ffd700, #ff8c00) !important;
        color: black !important;
        font-family: 'Bungee' !important;
        border-radius: 50px !important;
        height: 50px; width: 100%;
        border: none !important;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 ACCESS", "🛡️ JOIN"])
        with t1:
            e = st.text_input("Warrior Email")
            p = st.text_input("Access Key", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
                else: st.error("Wrong Credentials!")
        with t2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Codename"), st.text_input("Set Key", type='password')
            if st.button("CREATE HERO"):
                h = hashlib.sha256(np.encode()).hexdigest()
                try:
                    c.execute('INSERT INTO users (email, username, password, xp, goal) VALUES (?,?,?,0,100)', (ne, nu, h))
                    conn.commit(); st.balloons(); st.success("Created!")
                except: st.error("Email already exists!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff00ff; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("CHOOSE MISSION", 
                     ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🎧 Audio Hub", "⚙️ Settings"], 
                     key="nav_key", on_change=set_page)
        st.write("---")
        if st.button("EXIT ARENA"): st.session_state.logged_in = False; st.rerun()

    # Data Fetch with Error Handling
    c.execute("SELECT xp, goal, username FROM users WHERE email=?", (st.session_state.email,))
    user_info = c.fetchone()
    
    # Safety Check for data
    current_xp = user_info[0] if user_info and user_info[0] is not None else 0
    current_goal = user_info[1] if user_info and user_info[1] is not None else 100
    current_name = user_info[2] if user_info else "Warrior"

    page = st.session_state.user_page
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

    if page == "📊 Dashboard":
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='cyber-card'><h3>🏆 XP</h3><h1 style='color:#ffd700;'>{current_xp}</h1></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='cyber-card'><h3>🎯 GOAL</h3><h1 style='color:#00f2ff;'>{current_goal}</h1></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='cyber-card'><h3>🎖️ RANK</h3><h1 style='color:#ff00ff;'>{'ELITE' if current_xp >= current_goal else 'TRAINEE'}</h1></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='cyber-card'><h3>DAILY PROGRESS</h3>", unsafe_allow_html=True)
        st.progress(min(current_xp/current_goal, 1.0) if current_goal > 0 else 0)
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "📚 Vocab Vault":
        st.markdown("<div class='cyber-card'><h2>Word: 'LUMINOUS'</h2><p>Guess the meaning!</p></div>", unsafe_allow_html=True)
        if st.checkbox("💡 Get Hint"):
            st.markdown("<div style='color:#ffd700; font-style:italic;'>Hint: Think of something that glows in the dark.</div>", unsafe_allow_html=True)
        ans = st.text_input("Answer:")
        if st.button("CLAIM XP"):
            if "bright" in ans.lower() or "glow" in ans.lower():
                c.execute("UPDATE users SET xp = xp + 10 WHERE email=?", (st.session_state.email,))
                conn.commit(); st.balloons(); st.rerun()

    elif page == "⚙️ Settings":
        st.markdown("<h2 style='text-align:center;'>CONTROL CENTER</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            new_name = st.text_input("Change Codename", value=current_name)
            new_goal = st.number_input("Set Daily XP Goal", value=current_goal, step=10)
            if st.button("💾 SAVE SETTINGS"):
                c.execute("UPDATE users SET username=?, goal=? WHERE email=?", (new_name, new_goal, st.session_state.email))
                conn.commit()
                st.session_state.user = new_name
                st.success("Settings Updated!"); time.sleep(1); st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
