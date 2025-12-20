import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v40.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE (Gaming Core) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'enemy_hp' not in st.session_state: st.session_state.enemy_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# --- 3. ULTRA GAMER UI (CSS) ---
st.set_page_config(page_title="ENGLISH GURU", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    .stApp { 
        background: #0d1117;
        background-image: radial-gradient(#1f2937 1px, transparent 1px);
        background-size: 20px 20px;
        color: #e6edf3;
        font-family: 'Rajdhani', sans-serif;
    }

    /* English Guru Branding */
    .brand-title {
        font-family: 'Bungee', cursive;
        color: #00f2ff;
        font-size: 4rem;
        text-align: center;
        text-shadow: 0 0 15px #00f2ff, 0 0 30px #7000ff;
        margin-top: -50px;
    }

    .glass-card {
        background: rgba(22, 27, 34, 0.8);
        border: 2px solid #30363d;
        border-radius: 15px; padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        transition: 0.4s;
    }
    .glass-card:hover { border-color: #ff00ff; box-shadow: 0 0 20px rgba(255, 0, 255, 0.3); }

    /* Neon Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #7000ff) !important;
        color: white !important; font-family: 'Bungee' !important;
        border: none !important; border-radius: 8px !important;
        height: 50px; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0, 242, 255, 0.4); }

    /* HP Mechanics */
    .hp-bg { height: 30px; background: #21262d; border-radius: 5px; border: 1px solid #30363d; margin: 10px 0; }
    .hp-player { height: 100%; background: #238636; box-shadow: 0 0 10px #238636; transition: 0.6s; }
    .hp-boss { height: 100%; background: #da3633; box-shadow: 0 0 10px #da3633; transition: 0.6s; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DATA ---
COMBAT_DB = [
    {"q": "Meaning of 'EUPHORIA'?", "o": ["Sadness", "Extreme Happiness", "Anger", "Confusion"], "a": "Extreme Happiness"},
    {"q": "Correct sentence?", "o": ["He don't like it", "He doesn't likes it", "He doesn't like it", "He no like it"], "a": "He doesn't like it"},
    {"q": "Synonym of 'OBSOLETE'?", "o": ["Modern", "Outdated", "Expensive", "Fast"], "a": "Outdated"}
]

# --- 5. APP FLOW ---
if not st.session_state.logged_in:
    st.markdown("<p class='brand-title'>ENGLISH GURU</p>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        tab = st.tabs(["🚀 ACCESS", "🛡️ NEW HERO"])
        with tab[0]:
            e = st.text_input("Warrior Email")
            p = st.text_input("Key", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
                else: st.error("Access Denied!")
        with tab[1]:
            ne, nu, np = st.text_input("Email"), st.text_input("Codename"), st.text_input("Passkey", type='password')
            if st.button("CREATE PROFILE"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                conn.commit(); st.balloons(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Fetch Data
    c.execute("SELECT xp FROM users WHERE email=?", (st.session_state.email,))
    user_data = c.fetchone()
    current_xp = user_data[0] if user_data else 0

    # Sidebar
    with st.sidebar:
        st.markdown(f"<h1 style='color:#00f2ff; font-family:Bungee;'>{st.session_state.user}</h1>", unsafe_allow_html=True)
        st.write(f"📊 **LEVEL:** {1 + current_xp//100}")
        st.write(f"✨ **TOTAL XP:** {current_xp}")
        menu = st.radio("MISSION SELECT", ["🏠 DASHBOARD", "⚔️ COMBAT ARENA"])
        if st.button("ABORT MISSION"): st.session_state.logged_in = False; st.rerun()

    if menu == "🏠 DASHBOARD":
        st.markdown("<p class='brand-title'>ENGLISH GURU</p>", unsafe_allow_html=True)
        cols = st.columns(3)
        cols[0].markdown(f"<div class='glass-card'><h3>🏆 XP</h3><h2>{current_xp}</h2></div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='glass-card'><h3>🎖️ RANK</h3><h2>{'ELITE' if current_xp > 500 else 'SCOUT'}</h2></div>", unsafe_allow_html=True)
        cols[2].markdown(f"<div class='glass-card'><h3>🔥 STREAK</h3><h2>5 DAYS</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<br><div class='glass-card'><h3>Level Progression</h3>", unsafe_allow_html=True)
        st.progress(min((current_xp % 100)/100, 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "⚔️ COMBAT ARENA":
        st.markdown("<h2 style='text-align:center; font-family:Bungee;'>BATTLE ZONE</h2>", unsafe_allow_html=True)
        
        ca, cb = st.columns(2)
        with ca:
            st.write(f"🛡️ HERO HP: {st.session_state.player_hp}%")
            st.markdown(f"<div class='hp-bg'><div class='hp-player' style='width:{st.session_state.player_hp}%;'></div></div>", unsafe_allow_html=True)
        with cb:
            st.write(f"👾 MONSTER HP: {st.session_state.enemy_hp}%")
            st.markdown(f"<div class='hp-bg'><div class='hp-boss' style='width:{st.session_state.enemy_hp}%;'></div></div>", unsafe_allow_html=True)

        if st.session_state.enemy_hp <= 0:
            st.balloons(); st.success("ENEMY DESTROYED! +50 XP")
            c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
            conn.commit(); st.session_state.enemy_hp, st.session_state.player_hp = 100, 100
            st.button("Search Next Enemy")
        elif st.session_state.player_hp <= 0:
            st.error("Wasted! Respawning...")
            if st.button("RESPAWN"): st.session_state.enemy_hp, st.session_state.player_hp = 100, 100; st.rerun()
        else:
            q = random.choice(COMBAT_DB)
            st.markdown(f"<div class='glass-card'><h3>MISSION: {q['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("Choose Move:", q['o'], horizontal=True)
            if st.button("💥 STRIKE"):
                if ans == q['a']:
                    st.session_state.enemy_hp -= 34
                    st.toast("CRITICAL HIT!", icon="🔥")
                else:
                    st.session_state.player_hp -= 25
                    st.toast("SYSTEM ERROR! -25 HP", icon="💀")
                st.rerun()
