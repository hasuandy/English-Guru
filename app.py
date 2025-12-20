import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('vocal_warrior_v36.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER, streak INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE (Gaming Core) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'enemy_hp' not in st.session_state: st.session_state.enemy_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# --- 3. ULTRA DYNAMIC CSS ---
st.set_page_config(page_title="Vocal Warrior 36", page_icon="⚔️", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=JetBrains+Mono:wght@700&display=swap');
    
    .stApp {
        background: #050505;
        background-image: radial-gradient(#1b2735 0%, #090a0f 100%);
        color: #00f2ff;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Neon Pulse Animation */
    @keyframes pulse {
        0% { box-shadow: 0 0 5px #ff00ff; }
        50% { box-shadow: 0 0 25px #ff00ff; }
        100% { box-shadow: 0 0 5px #ff00ff; }
    }

    .game-card {
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
    }
    .game-card:hover {
        border-color: #ff00ff;
        transform: translateY(-5px);
    }

    .stButton>button {
        background: linear-gradient(45deg, #ff00ff, #00f2ff) !important;
        color: white !important;
        border: none !important;
        font-family: 'Bungee', cursive !important;
        font-size: 1.2rem !important;
        padding: 10px 20px !important;
        animation: pulse 2s infinite;
    }

    /* HP Bar Styling */
    .hp-container {
        width: 100%;
        background-color: #333;
        border-radius: 20px;
        margin: 10px 0;
    }
    .hp-bar-fill {
        height: 20px;
        border-radius: 20px;
        transition: width 0.5s ease-in-out;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. GAME CONTENT ---
VOCAB_BATTLE = [
    {"q": "Meaning of 'Vivid'?", "o": ["Dull", "Bright", "Small", "Slow"], "a": "Bright"},
    {"q": "Antonym of 'Gigantic'?", "o": ["Huge", "Tiny", "Strong", "Fast"], "a": "Tiny"},
    {"q": "Correct spelling?", "o": ["Comittee", "Committee", "Comite", "Commitee"], "a": "Committee"},
    {"q": "She ____ to the market every day.", "o": ["Go", "Goes", "Going", "Gone"], "a": "Goes"}
]

# --- 5. LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; font-size:4rem; color:#ff00ff;'>VOCAL WARRIOR</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)
        mode = st.tabs(["🔑 LOGIN", "🛡️ SIGNUP"])
        with mode[0]:
            e = st.text_input("EMAIL")
            p = st.text_input("PASSWORD", type='password')
            if st.button("START MISSION"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username, xp FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with mode[1]:
            ne, nu, np = st.text_input("NEW EMAIL"), st.text_input("CODENAME"), st.text_input("NEW PASSWORD", type='password')
            if st.button("RECRUIT ME"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0,0)', (ne, nu, h))
                conn.commit(); st.success("Welcome, Warrior!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- SIDEBAR: RANK SYSTEM ---
    with st.sidebar:
        c.execute("SELECT xp FROM users WHERE email=?", (st.session_state.email,))
        current_xp = c.fetchone()[0] or 0
        rank = "SOLDIER"
        if current_xp > 500: rank = "COMMANDER"
        if current_xp > 1000: rank = "WARLORD"
        
        st.markdown(f"## 🎖️ {st.session_state.user}\n**Rank:** {rank}")
        st.write(f"**XP:** {current_xp}")
        menu = st.radio("SELECT ARENA", ["🏠 Base", "⚔️ Combat Zone", "🏆 Leaderboard"])
        if st.button("EXIT GAME"): st.session_state.logged_in = False; st.rerun()

    # --- COMBAT ZONE (The "Majedar" Part) ---
    if menu == "⚔️ Combat Zone":
        st.markdown("<h1 style='text-align:center; font-family:Bungee;'>ARENA BATTLE</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🛡️ {st.session_state.user} (HP: {st.session_state.player_hp}%)")
            st.markdown(f'<div class="hp-container"><div class="hp-bar-fill" style="width:{st.session_state.player_hp}%; background:lime;"></div></div>', unsafe_allow_html=True)
        with col2:
            st.write(f"👹 MONSTER (HP: {st.session_state.enemy_hp}%)")
            st.markdown(f'<div class="hp-container"><div class="hp-bar-fill" style="width:{st.session_state.enemy_hp}%; background:red;"></div></div>', unsafe_allow_html=True)

        if st.session_state.enemy_hp <= 0:
            st.balloons()
            st.success("VICTORY! YOU GAINED 50 XP")
            c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
            conn.commit(); st.session_state.enemy_hp = 100; st.session_state.player_hp = 100
            if st.button("NEXT ENEMY"): st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("DEFEATED! Game Over.")
            if st.button("RESPAWN"): st.session_state.player_hp = 100; st.session_state.enemy_hp = 100; st.rerun()
        else:
            q = random.choice(VOCAB_BATTLE)
            st.markdown(f"<div class='game-card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
            ans = st.radio("Choose your weapon:", q['o'], horizontal=True)
            
            if st.button("💥 STRIKE"):
                if ans == q['a']:
                    st.session_state.enemy_hp -= 25
                    st.toast("Clean Hit! -25 HP to Enemy", icon='🔥')
                else:
                    st.session_state.player_hp -= 20
                    st.toast("Countered! -20 HP to You", icon='💀')
                st.rerun()

    elif menu == "🏠 Base":
        st.title("Welcome Back, Warrior!")
        st.markdown("""
        ### Daily Missions:
        1. Solve 5 Vocab questions (0/5)
        2. Defeat 1 Boss (0/1)
        3. Maintain 3-day streak
        """)
        st.info("Train in the Combat Zone to increase your rank!")

    elif menu == "🏆 Leaderboard":
        st.title("Hall of Fame")
        data = c.execute("SELECT username, xp FROM users ORDER BY xp DESC LIMIT 5").fetchall()
        for i, row in enumerate(data):
            st.markdown(f"<div class='game-card' style='margin:10px;'>#{i+1} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)
