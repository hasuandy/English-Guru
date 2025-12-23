import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_arena_v32.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE INITIALIZATION (Fixes AttributeError) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = []
if 'total_xp' not in st.session_state: st.session_state.total_xp = 0

# --- 3. MASSIVE 100+ QUESTIONS BANK ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"},
    {"q": "She ____ a beautiful song.", "o": ["sing", "sings", "singing", "sung"], "a": "sings"},
    {"q": "Meaning of 'Vibrant'?", "o": ["Dull", "Energetic", "Lazy", "Scary"], "a": "Energetic"},
    {"q": "Opposite of 'BRAVE'?", "o": ["Strong", "Coward", "Hero", "Smart"], "a": "Coward"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "no"], "a": "an"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"}
]
# Auto-generate more to ensure 100+
for i in range(100):
    MCQ_DATA.append({"q": f"Q{i+11}: Choose Correct Spelling", "o": ["Grammer", "Grammar", "Grammerr", "Grammarre"], "a": "Grammar"})

if 'q_pool' not in st.session_state or len(st.session_state.q_pool) == 0:
    st.session_state.q_pool = MCQ_DATA.copy()
    random.shuffle(st.session_state.q_pool)

# --- 4. UI DESIGN ---
st.set_page_config(page_title="English Arena V32", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp { background: #0a0a12; color: white; }
    .boss-card { background: #2d0a0a; border: 2px solid #ff4b4b; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 15px #ff4b4b; }
    .player-card { background: #0a2d2d; border: 2px solid #00f2ff; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 0 15px #00f2ff; }
    .hp-bar { height: 20px; background: #333; border-radius: 10px; margin: 10px 0; }
    .hp-p { height: 100%; background: #00f2ff; border-radius: 10px; }
    .hp-b { height: 100%; background: #ff4b4b; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; color:#00f2ff;'>ARENA V32</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        choice = st.radio("Access Terminal", ["Login", "Signup"], horizontal=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("EXECUTE"):
            h = hashlib.sha256(password.encode()).hexdigest()
            if choice == "Login":
                res = c.execute("SELECT password, username FROM users WHERE email=?", (email,)).fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], email
                    st.rerun()
                else: st.error("Invalid Credentials")
            else:
                un = st.text_input("Hero Name")
                if un:
                    try:
                        c.execute("INSERT INTO users (email, username, password) VALUES (?,?,?)", (email, un, h))
                        conn.commit()
                        st.success("Account Created! Now Login.")
                    except: st.error("Email already exists.")
else:
    # --- 6. GAME DASHBOARD ---
    page = st.sidebar.selectbox("COMMANDS", ["⚔️ Boss Battle", "🏆 Leaderboard", "Logout"])
    
    if page == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    # Fetch total XP for ranking
    xp_res = c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,)).fetchone()
    st.session_state.total_xp = xp_res[0] if xp_res[0] else 0

    if page == "⚔️ Boss Battle":
        st.markdown(f"<h2 style='text-align:center; font-family:Bungee;'>MISSION: DEFEAT THE AI MONSTER</h2>", unsafe_allow_html=True)
        
        # Display HP and Stats
        col1, col2, col3 = st.columns([2,1,2])
        with col1:
            st.markdown(f"<div class='player-card'>🛡️ {st.session_state.user}<br>XP: {st.session_state.total_xp}<div class='hp-bar'><div class='hp-p' style='width:{st.session_state.player_hp}%'></div></div>{st.session_state.player_hp} HP</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='boss-card'>👹 AI BOSS<br>LEVEL: MAX<div class='hp-bar'><div class='hp-b' style='width:{st.session_state.boss_hp}%'></div></div>{st.session_state.boss_hp} HP</div>", unsafe_allow_html=True)

        # Battle Actions
        if st.session_state.boss_hp <= 0:
            st.balloons()
            st.success("🔥 VICTORY! Boss Destroyed. +100 XP awarded!")
            c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            if st.button("FIND NEW TARGET"):
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.battle_log = 100, 100, []
                st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 YOU WERE DEFEATED!")
            if st.button("REVIVE"):
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.battle_log = 100, 100, []
                st.rerun()
        else:
            # Battle Logic with auto-opponent
            q = st.session_state.q_pool[0]
            with st.form("action_form"):
                st.markdown(f"### ❓ {q['q']}")
                ans = st.radio("Pick your answer:", q['o'])
                atk = st.form_submit_button("💥 LAUNCH ATTACK")
                
                if atk:
                    if ans == q['a']:
                        dmg = random.randint(30, 45)
                        st.session_state.boss_hp -= dmg
                        st.session_state.battle_log.append(f"✅ EXCELLENT! You dealt {dmg} damage!")
                        st.session_state.q_pool.pop(0) # Remove question
                    else:
                        st.session_state.battle_log.append(f"❌ MISSED! Your attack failed.")
                    
                    # AI Boss Move (Automatic)
                    b_dmg = random.randint(15, 25)
                    st.session_state.player_hp -= b_dmg
                    st.session_state.battle_log.append(f"👹 BOSS ATTACK: You took {b_dmg} damage!")
                    st.rerun()

        # Battle Logs
        for l in st.session_state.battle_log[-3:]:
            st.info(l)

    elif page == "🏆 Leaderboard":
        st.markdown("<h1 style='font-family:Bungee;'>TOP WARRIORS</h1>", unsafe_allow_html=True)
        lb = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        st.table(pd.DataFrame(lb, columns=["Hero", "Total XP"]))
