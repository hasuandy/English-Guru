import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('vocal_warrior_v38.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'enemy_hp' not in st.session_state: st.session_state.enemy_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# --- 3. HIGH-ENERGY CYBER CSS ---
st.set_page_config(page_title="Vocal Arena: Neon Overdrive", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=JetBrains+Mono:wght@500&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.wallpapersden.com/image/download/cyberpunk-city-street-neon-lights_bGhpZmqUmZqaraWkpJRmbmdlrWZnZ2U.jpg');
        background-size: cover; background-attachment: fixed;
        color: #00f2ff; font-family: 'JetBrains Mono', monospace;
    }
    
    .cyber-card {
        background: rgba(10, 10, 20, 0.8);
        backdrop-filter: blur(15px);
        border: 2px solid #ff00ff;
        border-radius: 20px; padding: 25px;
        box-shadow: 0 0 25px #ff00ff44, inset 0 0 10px #ff00ff22;
        text-align: center; margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important; font-family: 'Bungee', cursive !important;
        border: none !important; border-radius: 10px;
        padding: 15px; font-size: 1.2rem; transition: 0.3s;
        box-shadow: 0 5px 15px rgba(0, 242, 255, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 0 40px #00f2ff; transform: scale(1.05);
    }

    .hp-bar { height: 25px; border-radius: 5px; background: #111; border: 1px solid #555; overflow: hidden; }
    .hp-fill { height: 100%; transition: width 0.8s ease; }
    
    .stat-text { font-family: 'Bungee'; color: #ff00ff; text-shadow: 0 0 5px #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. GAME CONTENT ---
QUESTIONS = [
    {"q": "Choose the correct spelling:", "o": ["Necessary", "Necesary", "Necasery", "Neccesary"], "a": "Necessary"},
    {"q": "Synonym of 'GENEROUS'?", "o": ["Kind", "Cruel", "Small", "Greedy"], "a": "Kind"},
    {"q": "One who knows everything?", "o": ["Omniscient", "Omnipotent", "Omnipresent", "Smart"], "a": "Omniscient"}
]

# --- 5. APP STRUCTURE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#ff00ff; font-family:Bungee; font-size:4rem; text-shadow:0 0 20px #ff00ff;'>VOCAL ARENA</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        mode = st.radio("SYSTEM ACCESS", ["LOGIN", "NEW WARRIOR"], horizontal=True)
        e = st.text_input("WARRIOR EMAIL")
        p = st.text_input("SECURITY KEY", type='password')
        if st.button("INITIALIZE"):
            h = hashlib.sha256(p.encode()).hexdigest()
            if mode == "LOGIN":
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
            else:
                nu = st.text_input("CODENAME")
                if nu:
                    c.execute('INSERT INTO users VALUES (?,?,?,0)', (e, nu, h))
                    conn.commit(); st.success("Created!"); time.sleep(1); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar
    c.execute("SELECT xp FROM users WHERE email=?", (st.session_state.email,))
    row = c.fetchone()
    current_xp = row[0] if row else 0

    with st.sidebar:
        st.markdown(f"<h2 class='stat-text'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
        st.write(f"**XP:** `{current_xp}`")
        st.write(f"**RANK:** `{'Elite' if current_xp > 500 else 'Scout'}`")
        menu = st.radio("MISSION", ["⚔️ COMBAT", "🏆 RANKS"])
        if st.button("TERMINATE"): st.session_state.logged_in = False; st.rerun()

    if menu == "⚔️ COMBAT":
        st.markdown("<h1 class='stat-text' style='text-align:center;'>BATTLE ZONE</h1>", unsafe_allow_html=True)
        
        # HP Interface
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"YOU: {st.session_state.player_hp}%")
            st.markdown(f'<div class="hp-bar"><div class="hp-fill" style="width:{st.session_state.player_hp}%; background:#00f2ff; box-shadow: 0 0 15px #00f2ff;"></div></div>', unsafe_allow_html=True)
        with col2:
            st.write(f"BOSS: {st.session_state.enemy_hp}%")
            st.markdown(f'<div class="hp-bar"><div class="hp-fill" style="width:{st.session_state.enemy_hp}%; background:#ff0000; box-shadow: 0 0 15px #ff0000;"></div></div>', unsafe_allow_html=True)

        if st.session_state.enemy_hp <= 0:
            st.balloons(); st.markdown("<div class='cyber-card'><h2>VICTORY! +50 XP Gained</h2></div>", unsafe_allow_html=True)
            c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
            conn.commit(); st.session_state.enemy_hp = 100; st.session_state.player_hp = 100
            st.button("Next Enemy")
        elif st.session_state.player_hp <= 0:
            st.error("Wasted! Try again."); 
            if st.button("Respawn"): st.session_state.player_hp = 100; st.session_state.enemy_hp = 100; st.rerun()
        else:
            q = random.choice(QUESTIONS)
            st.markdown(f"<div class='cyber-card'><h3>MISSION: {q['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("Choose Weapon:", q['o'], horizontal=True)
            if st.button("🔥 EXECUTE STRIKE"):
                if ans == q['a']:
                    st.session_state.enemy_hp -= 34
                    st.toast("CRITICAL HIT!", icon="🔥")
                else:
                    st.session_state.player_hp -= 25
                    st.toast("SYSTEM FAILURE!", icon="💀")
                st.rerun()
