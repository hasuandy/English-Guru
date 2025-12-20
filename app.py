import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP & AUTO-FIX ---
# Naye DB name se start kar rahe hain taaki purane errors clash na karein
conn = sqlite3.connect('english_guru_v28_final.db', check_same_thread=False)
c = conn.cursor()

# Tables create/update logic
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, 
              xp INTEGER DEFAULT 0, hp INTEGER DEFAULT 100, goal INTEGER DEFAULT 100)''')
c.execute('''CREATE TABLE IF NOT EXISTS vault 
             (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "🏰 Home Base"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. RPG NEON STYLING ---
st.set_page_config(page_title="English Guru V27 Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .brand-title { font-family: 'Bungee'; font-size: 4rem; text-align: center; color: #ff0055; text-shadow: 0 0 20px #ff0055; margin-top: -50px; }
    .stat-card { background: rgba(0,20,20,0.6); border: 2px solid #00f2ff; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 10px; }
    .battle-card { background: rgba(20,0,0,0.6); border: 2px solid #ff0055; border-radius: 15px; padding: 20px; box-shadow: 0 0 15px #ff0055; }
    .stButton>button { background: linear-gradient(45deg, #ff0055, #00f2ff) !important; color: white !important; font-family: 'Bungee' !important; border-radius: 10px !important; width: 100%; border:none; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.2,1])
    with col:
        t1, t2 = st.tabs(["⚡ LOGIN", "⚔️ SIGNUP"])
        with t1:
            e = st.text_input("Email")
            p = st.text_input("Passkey", type='password')
            if st.button("ENTER ARENA"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
                else: st.error("Access Denied!")
        with t2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Warrior Name"), st.text_input("Set Passkey", type='password')
            if st.button("RECRUIT ME"):
                h = hashlib.sha256(np.encode()).hexdigest()
                try:
                    c.execute('INSERT INTO users (email, username, password, xp, hp, goal) VALUES (?,?,?,0,100,100)', (ne, nu, h))
                    conn.commit(); st.balloons(); st.success("Profile Created!"); st.rerun()
                except: st.error("Email already exists!")

else:
    # --- DATA FETCH WITH SAFETY ---
    c.execute("SELECT xp, hp, goal FROM users WHERE email=?", (st.session_state.email,))
    user_data = c.fetchone()
    
    # Error Handling Fix: Agar data nahi mila toh default values set hongi
    if user_data:
        u_xp, u_hp, u_goal = user_data
    else:
        u_xp, u_hp, u_goal = 0, 100, 100

    # Navigation
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff0055; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault", "🏆 Leaderboard"], 
                     key="nav_key", on_change=set_page)
        st.write("---")
        if st.button("ABORT MISSION"): st.session_state.logged_in = False; st.rerun()

    page = st.session_state.user_page
    st.markdown(f"<h1 class='brand-title'>{page.split(' ')[1].upper()}</h1>", unsafe_allow_html=True)

    # --- HOME BASE ---
    if page == "🏰 Home Base":
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='stat-card'><h3>XP</h3><h1>{u_xp}</h1></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-card'><h3>STAMINA</h3><h1>{u_hp}%</h1></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-card'><h3>GOAL</h3><h1>{u_goal}</h1></div>", unsafe_allow_html=True)
        
        st.write("### 📈 Your Growth Radar")
        st.area_chart({"XP": [10, 25, u_xp, u_xp+10]})

    # --- DAILY BOSS (The Battle) ---
    elif page == "👹 Daily Boss":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='battle-card'><h3>👹 BOSS: GRAMMAR TITAN</h3><p>HP: {st.session_state.boss_hp}/500</p>", unsafe_allow_html=True)
            st.progress(st.session_state.boss_hp/500)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='battle-card'><h3>🛡️ {st.session_state.user}</h3><p>STAMINA: {u_hp}/100</p>", unsafe_allow_html=True)
            st.progress(u_hp/100)
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("---")
        q = "Battle Question: 'She _____ her homework every day.'"
        choice = st.radio(q, ["do", "does", "doing"])
        
        if st.button("💥 LAUNCH STRIKE"):
            if choice == "does":
                dmg = random.randint(50, 80)
                st.session_state.boss_hp -= dmg
                c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
                conn.commit()
                st.success(f"CRITICAL HIT! Dealt {dmg} damage! +50 XP Secured.")
                if st.session_state.boss_hp <= 0:
                    st.balloons(); st.session_state.boss_hp = 500
            else:
                st.error("MISS! The Boss strikes back!")
                new_hp = max(u_hp - 20, 0)
                c.execute("UPDATE users SET hp = ? WHERE email=?", (new_hp, st.session_state.email))
                conn.commit()
            time.sleep(1); st.rerun()

    # --- WORD VAULT ---
    elif page == "📚 Word Vault":
        word = st.text_input("New Intel (Word)")
        mean = st.text_area("Data (Meaning)")
        if st.button("🔒 SEAL IN VAULT"):
            c.execute("INSERT INTO vault VALUES (?,?,?)", (st.session_state.email, word, mean))
            conn.commit(); st.success("Knowledge Stored!")

    # --- LEADERBOARD ---
    elif page == "🏆 Leaderboard":
        c.execute("SELECT username, xp FROM users ORDER BY xp DESC LIMIT 5")
        for i, user in enumerate(c.fetchall()):
            st.markdown(f"<div class='stat-card'>#{i+1} {user[0]} - {user[1]} XP</div>", unsafe_allow_html=True)
