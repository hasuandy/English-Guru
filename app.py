import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP (Nayi File Name taaki fresh start ho) ---
conn = sqlite3.connect('english_guru_v50_fix.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, 
              xp INTEGER DEFAULT 0, hp INTEGER DEFAULT 100, goal INTEGER DEFAULT 100)''')
c.execute('''CREATE TABLE IF NOT EXISTS vault 
             (email TEXT, word TEXT, meaning TEXT)''')
conn.commit()

# --- 2. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = ""
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'user_page' not in st.session_state:
    st.session_state.user_page = "🏰 Home Base"
if 'boss_hp' not in st.session_state:
    st.session_state.boss_hp = 500

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. RPG STYLING (NEON & DARK) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .brand-title { font-family: 'Bungee'; font-size: 4rem; text-align: center; color: #ff0055; text-shadow: 0 0 15px #ff0055; }
    .cyber-card { background: rgba(30, 30, 60, 0.4); border: 1px solid #00f2ff; border-radius: 15px; padding: 25px; box-shadow: 0 0 20px rgba(0, 242, 255, 0.1); }
    .stButton>button { background: linear-gradient(45deg, #ff0055, #00f2ff) !important; color: white !important; font-family: 'Bungee' !important; border-radius: 12px !important; border:none; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN / SIGNUP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["⚡ LOGIN", "⚔️ SIGNUP"])
        
        with tab1:
            email_in = st.text_input("Warrior Email", key="login_email")
            pass_in = st.text_input("Passkey", type='password', key="login_pass")
            if st.button("ENTER ARENA"):
                hashed_pw = hashlib.sha256(pass_in.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (email_in, hashed_pw))
                result = c.fetchone()
                if result:
                    st.session_state.logged_in = True
                    st.session_state.user = result[0]
                    st.session_state.email = email_in
                    st.rerun()
                else:
                    st.error("Invalid Credentials! Please Signup first.")
        
        with tab2:
            new_email = st.text_input("New Email", key="reg_email")
            new_user = st.text_input("Warrior Name", key="reg_user")
            new_pass = st.text_input("Set Passkey", type='password', key="reg_pass")
            if st.button("CREATE HERO"):
                if new_email and new_user and new_pass:
                    hashed_pw = hashlib.sha256(new_pass.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users (email, username, password, xp, hp, goal) VALUES (?,?,?,0,100,100)', (new_email, new_user, hashed_pw))
                        conn.commit()
                        st.success("Account Created! Go to Login Tab.")
                        st.balloons()
                    except:
                        st.error("This email is already registered.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- SAFE DATA FETCHING ---
    try:
        c.execute("SELECT xp, hp, goal FROM users WHERE email=?", (st.session_state.email,))
        data = c.fetchone()
        if data:
            u_xp, u_hp, u_goal = data
        else:
            u_xp, u_hp, u_goal = 0, 100, 100
    except:
        u_xp, u_hp, u_goal = 0, 100, 100

    # Sidebar
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff0055; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault", "🏆 Leaderboard"], 
                     key="nav_key", on_change=set_page)
        st.write("---")
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- PAGES ---
    page = st.session_state.user_page
    
    if page == "🏰 Home Base":
        st.markdown("<h1 class='brand-title'>WARRIOR BASE</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='cyber-card'><h3>XP</h3><h1>{u_xp}</h1></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='cyber-card'><h3>STAMINA</h3><h1>{u_hp}%</h1></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='cyber-card'><h3>GOAL</h3><h1>{u_goal}</h1></div>", unsafe_allow_html=True)
        
    elif page == "👹 Daily Boss":
        st.markdown("<h1 class='brand-title'>BOSS BATTLE</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp}/500")
            st.progress(st.session_state.boss_hp/500)
        with col2:
            st.write(f"### 🛡️ YOUR HP: {u_hp}/100")
            st.progress(u_hp/100)
        
        st.write("---")
        ans = st.radio("Choose the correct word: 'I ____ English every day.'", ["studies", "study", "studying"])
        if st.button("💥 ATTACK"):
            if ans == "study":
                dmg = random.randint(50, 100)
                st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
                c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
                conn.commit()
                st.success(f"CRITICAL HIT! -{dmg} HP")
            else:
                st.error("WRONG! Boss counter-attacked!")
            time.sleep(1)
            st.rerun()

    elif page == "📚 Word Vault":
        st.markdown("<h1 class='brand-title'>VAULT</h1>", unsafe_allow_html=True)
        w = st.text_input("Word")
        m = st.text_input("Meaning")
        if st.button("SAVE"):
            c.execute("INSERT INTO vault VALUES (?,?,?)", (st.session_state.email, w, m))
            conn.commit()
            st.success("Saved!")
