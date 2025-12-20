import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro_v28.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"
if 'combo' not in st.session_state: st.session_state.combo = 0

# --- 3. UNLIMITED QUESTIONS POOL ---
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

# --- 4. CYBERPUNK CSS ---
st.set_page_config(page_title="English Guru: Cyber Arena", page_icon="🌃", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@400;700&display=swap');
    
    .stApp {{ 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1605810230434-7631ac76ec81?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=1080');
        background-size: cover;
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
    }}
    
    /* Glassmorphism Card Effect */
    .gaming-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin-bottom: 25px;
    }}
    
    .question-text {{
        font-family: 'Bungee', cursive;
        font-size: 28px;
        color: #ff00ff; /* Neon Pink Question */
        text-shadow: 0 0 15px #ff00ff;
    }}

    .stButton>button {{
        background: rgba(0, 242, 255, 0.1);
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        border-radius: 15px;
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        padding: 20px;
        transition: 0.5s;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    .stButton>button:hover {{
        background: #00f2ff !important;
        color: #000 !important;
        box-shadow: 0 0 30px #00f2ff;
        transform: translateY(-5px);
    }}

    .hp-bar {{ height: 25px; border-radius: 20px; background: #111; border: 1px solid #444; overflow: hidden; box-shadow: inset 0 0 10px #000; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    
    /* Dashboard Stats Style */
    .stat-val {{ font-size: 40px; font-weight: bold; color: {st.session_state.theme}; text-shadow: 0 0 10px {st.session_state.theme}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIN/SIGNUP (GLASS BOX) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; font-size:5rem; color:#00f2ff; text-shadow: 0 0 30px #00f2ff;'>CYBER ARENA</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.8,1])
    with c2:
        tab1, tab2 = st.tabs(["⚡ ACCESS LOGIN", "🛡️ REGISTER HERO"])
        with tab1:
            e = st.text_input("User ID")
            p = st.text_input("Access Key", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
        with tab2:
            ne, nu, np = st.text_input("New ID"), st.text_input("Hero Name"), st.text_input("Set Key", type='password')
            if st.button("CREATE PROFILE"):
                if "@" in ne:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, ne
                        st.rerun()
                    except: st.error("Profile Exists!")

# --- 6. ARENA MAIN ---
else:
    with st.sidebar:
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>🎮 {st.session_state.user}</h2>", unsafe_allow_html=True)
        page = st.radio("SELECT MISSION", ["🏠 Base Hub", "🎓 Grind Zone", "⚔️ Boss Fight", "🏆 Leaderboard"])
        if st.button("EXIT MISSION"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "🏠 Base Hub":
        st.markdown("<h1 style='font-family:Bungee;'>DASHBOARD</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,))
        txp = c.fetchone()[0] or 0
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='gaming-card'>🏆 TOTAL XP<br><div class='stat-val'>{txp}</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='gaming-card'>🎖️ RANK<br><div class='stat-val'>{'PRO' if txp > 300 else 'NOOB'}</div></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='gaming-card'>🔥 LVL<br><div class='stat-val'>{1 + (txp // 100)}</div></div>", unsafe_allow_html=True)

    elif page == "🎓 Grind Zone":
        st.markdown("<h1 style='font-family:Bungee;'>UNLIMITED TRAINING</h1>", unsafe_allow_html=True)
        q = random.choice(MCQ_DATA)
        st.markdown(f"<div class='gaming-card'><div class='question-text'>{q['q']}</div></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            with cols[i%2]:
                if st.button(opt, key=f"t_{i}_{time.time()}"):
                    if opt == q['a']:
                        st.balloons(); st.success("BULLSEYE! +10 XP")
                        c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today())))
                        conn.commit(); time.sleep(0.7); st.rerun()
                    else: st.error("MISSED!")

    elif page == "⚔️ Boss Fight":
        st.markdown("<h1 style='color:#ff0055; font-family:Bungee; text-shadow: 0 0 20px #ff0055;'>NEON OVERLORD</h1>", unsafe_allow_html=True)
        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"YOU: {st.session_state.player_hp}%")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.write(f"BOSS: {st.session_state.boss_hp}%")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff0055;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS TERMINATED! +100 XP")
            c.execute("INSERT INTO progress VALUES (?, ?, 100)", (st.session_state.email, str(date.today()))); conn.commit()
            if st.button("NEXT BOSS"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("SYSTEM OVERLOAD: YOU DIED!")
            if st.button("REBOOT"): st.session_state.player_hp = 100; st.session_state.boss_hp = 100; st.rerun()
        else:
            q = random.choice(MCQ_DATA)
            st.markdown(f"<div class='gaming-card'><p>{q['q']}</p></div>", unsafe_allow_html=True)
            ans = st.radio("SELECT WEAPON:", q['o'], horizontal=True)
            if st.button("💥 FIRE"):
                if ans == q['a']:
                    st.session_state.combo += 1
                    dmg = 20 * st.session_state.combo
                    st.session_state.boss_hp -= dmg
                    st.session_state.battle_log = f"CRITICAL HIT! -{dmg} HP"
                else:
                    st.session_state.combo = 0
                    st.session_state.player_hp -= 20
                    st.session_state.battle_log = "BOSS COUNTERED! -20 HP"
                st.rerun()
        st.info(st.session_state.battle_log)

    elif page == "🏆 Leaderboard":
        st.title("🏆 RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.markdown(f"<div class='gaming-card' style='text-align:left;'>#{i+1} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)
