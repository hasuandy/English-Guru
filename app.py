import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('vocal_warrior_v37.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'enemy_hp' not in st.session_state: st.session_state.enemy_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# --- 3. CSS (Neon Style) ---
st.set_page_config(page_title="Vocal Warrior Pro", page_icon="⚔️", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0a0a0a; color: #00f2ff; font-family: 'Courier New', monospace; }
    .game-card {
        background: rgba(20, 20, 20, 0.8);
        border: 2px solid #ff00ff;
        border-radius: 15px; padding: 20px;
        text-align: center; box-shadow: 0 0 20px #ff00ff33;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important; font-weight: bold !important;
        border-radius: 10px; width: 100%; height: 50px;
    }
    .hp-bar { height: 20px; border-radius: 10px; background: #333; overflow: hidden; }
    .hp-fill { height: 100%; transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. QUESTIONS ---
QUESTIONS = [
    {"q": "Synonym of 'ABANDON'?", "o": ["Leave", "Keep", "Hold", "Adopt"], "a": "Leave"},
    {"q": "Antonym of 'FRAGILE'?", "o": ["Weak", "Strong", "Delicate", "Thin"], "a": "Strong"},
    {"q": "Correct spelling?", "o": ["Occurrence", "Occurence", "Ocurrence", "Occurrance"], "a": "Occurrence"}
]

# --- 5. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#ff00ff;'>⚔️ VOCAL WARRIOR ⚔️</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        mode = st.tabs(["LOGIN", "SIGNUP"])
        with mode[0]:
            e = st.text_input("Email")
            p = st.text_input("Password", type='password')
            if st.button("ENTER ARENA"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
                else: st.error("Wrong Credentials")
        with mode[1]:
            ne, nu, np = st.text_input("New Email"), st.text_input("Warrior Name"), st.text_input("New Password", type='password')
            if st.button("RECRUIT"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                conn.commit(); st.success("Warrior Created!"); st.rerun()

else:
    # --- FETCH USER DATA (Error-proof) ---
    c.execute("SELECT xp FROM users WHERE email=?", (st.session_state.email,))
    row = c.fetchone()
    current_xp = row[0] if row else 0 # Yahan humne error fix kar diya hai!

    # --- WEAPON & RANK SYSTEM ---
    weapon = "👊 Bare Fists"
    if current_xp >= 100: weapon = "🗡️ Iron Dagger"
    if current_xp >= 300: weapon = "⚔️ Plasma Sword"
    if current_xp >= 600: weapon = "🔥 Dragon Slayer"

    with st.sidebar:
        st.markdown(f"### 🛡️ {st.session_state.user}")
        st.markdown(f"**XP:** `{current_xp}`")
        st.markdown(f"**Weapon:** `{weapon}`")
        menu = st.radio("MENU", ["Combat Zone", "Leaderboard"])
        if st.button("Logout"): st.session_state.logged_in = False; st.rerun()

    if menu == "Combat Zone":
        st.markdown(f"<h2 style='text-align:center;'>BATTLE FIELD</h2>", unsafe_allow_html=True)
        
        # UI: HP BARS
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"YOU ({st.session_state.player_hp}%)")
            st.markdown(f'<div class="hp-bar"><div class="hp-fill" style="width:{st.session_state.player_hp}%; background:lime;"></div></div>', unsafe_allow_html=True)
        with col2:
            st.write(f"ENEMY ({st.session_state.enemy_hp}%)")
            st.markdown(f'<div class="hp-bar"><div class="hp-fill" style="width:{st.session_state.enemy_hp}%; background:red;"></div></div>', unsafe_allow_html=True)

        if st.session_state.enemy_hp <= 0:
            st.balloons(); st.success("VICTORY! +50 XP")
            c.execute("UPDATE users SET xp = xp + 50 WHERE email=?", (st.session_state.email,))
            conn.commit(); st.session_state.enemy_hp = 100; st.session_state.player_hp = 100
            st.button("Search Next Enemy")
        elif st.session_state.player_hp <= 0:
            st.error("YOU DIED!"); 
            if st.button("Respawn"): st.session_state.player_hp = 100; st.session_state.enemy_hp = 100; st.rerun()
        else:
            q = random.choice(QUESTIONS)
            st.markdown(f"<div class='game-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("Choose Move:", q['o'], horizontal=True)
            if st.button(f"USE {weapon.split(' ')[1].upper()}"):
                if ans == q['a']:
                    st.session_state.enemy_hp -= 34
                    st.toast("CRITICAL HIT!", icon="🔥")
                else:
                    st.session_state.player_hp -= 25
                    st.toast("YOU GOT HIT!", icon="💀")
                st.rerun()
                
    elif menu == "Leaderboard":
        st.title("Hall of Fame")
        data = c.execute("SELECT username, xp FROM users ORDER BY xp DESC LIMIT 10").fetchall()
        for i, r in enumerate(data):
            st.markdown(f"<div class='game-card' style='margin-bottom:10px;'>#{i+1} {r[0]} - {r[1]} XP</div>", unsafe_allow_html=True)
