import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DB & AUTO-REPAIR ENGINE ---
conn = sqlite3.connect('english_guru_v27.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER DEFAULT 0, hp INTEGER DEFAULT 100, goal INTEGER DEFAULT 100)')
c.execute('CREATE TABLE IF NOT EXISTS vault (email TEXT, word TEXT, meaning TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)')
conn.commit()

# --- 2. SESSION & BATTLE STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "🏰 Home Base"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500

def set_page(): st.session_state.user_page = st.session_state.nav_key

# --- 3. RPG NEON STYLING ---
st.set_page_config(page_title="English Guru V27", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .brand-title { font-family: 'Bungee'; font-size: 4.5rem; text-align: center; color: #ff0055; text-shadow: 0 0 20px #ff0055; margin-top: -50px; }
    .battle-card { background: rgba(20,0,0,0.6); border: 2px solid #ff0055; border-radius: 15px; padding: 20px; box-shadow: 0 0 15px #ff0055; }
    .stat-card { background: rgba(0,20,20,0.6); border: 2px solid #00f2ff; border-radius: 15px; padding: 15px; text-align: center; }
    .stButton>button { background: linear-gradient(45deg, #ff0055, #00f2ff) !important; color: white !important; font-family: 'Bungee' !important; border-radius: 10px !important; width: 100%; border:none; height: 50px; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #ff0055, #00f2ff) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CORE ENGINE ---
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
        with t2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Warrior Name"), st.text_input("Set Passkey", type='password')
            if st.button("RECRUIT ME"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users (email, username, password, xp, hp, goal) VALUES (?,?,?,0,100,100)', (ne, nu, h))
                conn.commit(); st.balloons(); st.rerun()
else:
    # Navigation
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff0055; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault", "🏆 Leaderboard", "⚙️ Settings"], key="nav_key", on_change=set_page)
        if st.button("ABORT MISSION"): st.session_state.logged_in = False; st.rerun()

    c.execute("SELECT xp, hp, goal FROM users WHERE email=?", (st.session_state.email,))
    u_xp, u_hp, u_goal = c.fetchone()
    page = st.session_state.user_page

    # --- HOME BASE (Growth Chart) ---
    if page == "🏰 Home Base":
        st.markdown("<h1 class='brand-title'>HOME BASE</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='stat-card'><h3>XP</h3><h1>{u_xp}</h1></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-card'><h3>STAMINA</h3><h1>{u_hp}%</h1></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-card'><h3>DAILY GOAL</h3><h1>{u_goal}</h1></div>", unsafe_allow_html=True)
        
        # Pro Growth Chart
        st.write("### 📈 Evolutionary Growth (XP Chart)")
        chart_data = {"Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Today"], "XP": [10, 45, 30, 80, 60, u_xp]}
        st.area_chart(chart_data, x="Day", y="XP")

    # --- DAILY BOSS (The Battle System) ---
    elif page == "👹 Daily Boss":
        st.markdown("<h1 class='brand-title'>BOSS BATTLE</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='battle-card'><h3>👹 GRAMMAR TITAN</h3><p>HP: {st.session_state.boss_hp}/500</p>", unsafe_allow_html=True)
            st.progress(st.session_state.boss_hp/500)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='battle-card'><h3>🛡️ {st.session_state.user}</h3><p>STAMINA: {u_hp}/100</p>", unsafe_allow_html=True)
            st.progress(u_hp/100)
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("---")
        q = "Which sentence is correct?"
        opts = ["He don't like it.", "He doesn't likes it.", "He doesn't like it."]
        choice = st.radio(q, opts)
        
        if st.button("💥 LAUNCH ATTACK"):
            if choice == "He doesn't like it.":
                dmg = random.randint(40, 70)
                st.session_state.boss_hp -= dmg
                st.success(f"🔥 CRITICAL HIT! You dealt {dmg} damage!")
                c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
                conn.commit()
                if st.session_state.boss_hp <= 0:
                    st.balloons(); st.write("### 🏆 TITAN FALLEN! YOU WON 50 XP!"); st.session_state.boss_hp = 500
            else:
                u_dmg = random.randint(20, 40)
                new_hp = max(u_hp - u_dmg, 0)
                c.execute("UPDATE users SET hp = ? WHERE email=?", (new_hp, st.session_state.email))
                conn.commit()
                st.error(f"💀 MISS! Titan counter-attacked for {u_dmg} damage!")
            time.sleep(1); st.rerun()

    # --- WORD VAULT ---
    elif page == "📚 Word Vault":
        st.markdown("<h1 class='brand-title'>WORD VAULT</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            w = st.text_input("New Word")
            m = st.text_area("Meaning/Usage")
            if st.button("🔒 SEAL IN VAULT"):
                c.execute("INSERT INTO vault VALUES (?,?,?)", (st.session_state.email, w, m))
                conn.commit(); st.toast("Knowledge Saved!")
        with c2:
            st.write("### Your Dictionary")
            c.execute("SELECT word, meaning FROM vault WHERE email=?", (st.session_state.email,))
            for row in c.fetchall():
                with st.expander(f"📖 {row[0]}"): st.write(row[1])

    # --- LEADERBOARD ---
    elif page == "🏆 Leaderboard":
        st.markdown("<h1 class='brand-title'>HALL OF FAME</h1>", unsafe_allow_html=True)
        c.execute("SELECT username, xp FROM users ORDER BY xp DESC LIMIT 5")
        leaders = c.fetchall()
        for i, leader in enumerate(leaders):
            st.markdown(f"<div class='stat-card' style='margin-bottom:10px;'>#{i+1} 💠 {leader[0]} — {leader[1]} XP</div>", unsafe_allow_html=True)

    # --- SETTINGS ---
    elif page == "⚙️ Settings":
        st.markdown("<h2 style='text-align:center;'>RECONFIGURATION</h2>", unsafe_allow_html=True)
        new_g = st.slider("Daily XP Goal", 50, 500, u_goal)
        if st.button("💾 SAVE CONFIG"):
            c.execute("UPDATE users SET goal=? WHERE email=?", (new_g, st.session_state.email))
            conn.commit(); st.success("Settings Saved!")
