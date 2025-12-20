import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP (Naya Name taaki purana error clear ho jaye) ---
conn = sqlite3.connect('english_guru_v30_final.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, 
              xp INTEGER DEFAULT 0, hp INTEGER DEFAULT 100, goal INTEGER DEFAULT 100)''')
c.execute('''CREATE TABLE IF NOT EXISTS vault 
             (email TEXT, word TEXT, meaning TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "🏰 Home Base"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. RPG NEON STYLING ---
st.set_page_config(page_title="English Guru V30", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .brand-title { font-family: 'Bungee'; font-size: 4rem; text-align: center; color: #ff0055; text-shadow: 0 0 20px #ff0055; }
    .cyber-card { background: rgba(20, 20, 40, 0.8); border: 1px solid #00f2ff; border-radius: 15px; padding: 25px; box-shadow: 0 0 15px rgba(0, 242, 255, 0.2); }
    .stButton>button { background: linear-gradient(45deg, #ff0055, #00f2ff) !important; color: white !important; font-family: 'Bungee' !important; border-radius: 10px !important; width: 100%; border:none; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION (Login/Signup) ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.2,1])
    with col:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["⚡ LOGIN", "⚔️ SIGNUP"])
        with t1:
            e = st.text_input("Warrior Email")
            p = st.text_input("Passkey", type='password')
            if st.button("ENTER ARENA"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
                else: st.error("Wrong Email/Key! Please try again or Signup.")
        with t2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Warrior Name"), st.text_input("Set Passkey", type='password')
            if st.button("CREATE PROFILE"):
                if ne and nu and np:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users (email, username, password, xp, hp, goal) VALUES (?,?,?,0,100,100)', (ne, nu, h))
                        conn.commit(); st.success("Profile Created! Now go to LOGIN tab."); st.balloons()
                    except: st.error("Email already exists!")
                else: st.warning("Please fill all details.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- DATA FETCH SAFETY (Ye Line Error Fix Karegi) ---
    c.execute("SELECT xp, hp, goal FROM users WHERE email=?", (st.session_state.email,))
    user_data = c.fetchone()
    u_xp, u_hp, u_goal = (user_data[0], user_data[1], user_data[2]) if user_data else (0, 100, 100)

    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff0055; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault", "🏆 Leaderboard"], 
                     key="nav_key", on_change=set_page)
        if st.button("ABORT MISSION"): st.session_state.logged_in = False; st.rerun()

    page = st.session_state.user_page

    # --- PAGES ---
    if page == "🏰 Home Base":
        st.markdown("<h1 class='brand-title'>WARRIOR BASE</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("CURRENT XP", u_xp)
        c2.metric("STAMINA", f"{u_hp}%")
        c3.metric("DAILY GOAL", u_goal)
        st.area_chart({"Growth": [0, 10, 25, u_xp]})

    elif page == "👹 Daily Boss":
        st.markdown("<h1 class='brand-title'>BOSS BATTLE</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"### 👹 TITAN HP: {st.session_state.boss_hp}/500")
            st.progress(st.session_state.boss_hp/500)
        with col2:
            st.write(f"### 🛡️ YOUR HP: {u_hp}/100")
            st.progress(u_hp/100)
        
        st.write("---")
        q = "Question: Select the correct sentence."
        choice = st.radio(q, ["She walk home.", "She walks home.", "She walking home."])
        if st.button("💥 STRIKE"):
            if choice == "She walks home.":
                dmg = random.randint(50, 80)
                st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
                c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
                conn.commit(); st.success(f"CRITICAL HIT! -{dmg} HP to Boss!"); time.sleep(1); st.rerun()
            else:
                st.error("MISS! You lost 20 HP."); c.execute("UPDATE users SET hp = hp - 20 WHERE email=?", (st.session_state.email,))
                conn.commit(); time.sleep(1); st.rerun()

    elif page == "📚 Word Vault":
        st.markdown("<h1 class='brand-title'>WORD VAULT</h1>", unsafe_allow_html=True)
        w = st.text_input("New Word")
        m = st.text_area("Meaning")
        if st.button("SAVE WORD"):
            c.execute("INSERT INTO vault VALUES (?,?,?)", (st.session_state.email, w, m))
            conn.commit(); st.success("Saved to your dictionary!")
