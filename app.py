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
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"},
    {"q": "Synonym of 'HAPPY'?", "o": ["Sad", "Joyful", "Angry", "Bored"], "a": "Joyful"},
    {"q": "Past tense of 'GO'?", "o": ["Gone", "Went", "Goes", "Going"], "a": "Went"},
    {"q": "____ you like coffee?", "o": ["Do", "Does", "Is", "Are"], "a": "Do"},
    {"q": "Correct spelling?", "o": ["Recieve", "Receive", "Recive", "Receve"], "a": "Receive"},
    {"q": "Meaning of 'GIGANTIC'?", "o": ["Small", "Tiny", "Huge", "Thin"], "a": "Huge"}
]

# --- 4. ULTRA GAMING CSS ---
st.set_page_config(page_title="English Guru V28", page_icon="🎮", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Roboto:wght@400;700&display=swap');
    
    .stApp {{ 
        background: radial-gradient(circle, #1a1a2e, #020205);
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }}
    
    .gaming-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid {st.session_state.theme};
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 20px {st.session_state.theme}44;
        margin-bottom: 20px;
    }}
    
    .question-text {{
        font-family: 'Bungee', cursive;
        font-size: 24px;
        color: {st.session_state.theme};
        text-shadow: 0 0 10px {st.session_state.theme};
        margin-bottom: 20px;
    }}

    .stButton>button {{
        background: linear-gradient(45deg, {st.session_state.theme}, #7000ff);
        color: white !important;
        border: none;
        border-radius: 12px;
        font-family: 'Bungee', cursive;
        padding: 15px 30px;
        transition: 0.4s;
        width: 100%;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 30px {st.session_state.theme};
    }}

    .hp-bar {{ height: 25px; border-radius: 15px; background: #111; border: 2px solid #333; overflow: hidden; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; font-size:4rem; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>ARENA V28</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        tab1, tab2 = st.tabs(["🔥 LOGIN", "💎 SIGNUP"])
        with tab1:
            e = st.text_input("Email")
            p = st.text_input("Password", type='password')
            if st.button("START BATTLE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
        with tab2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Hero Name"), st.text_input("Set Key", type='password')
            if st.button("CREATE ACCOUNT"):
                if "@" in ne:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, ne
                        st.rerun()
                    except: st.error("User exists!")

# --- 6. MAIN CONTENT ---
else:
    with st.sidebar:
        st.markdown(f"<h2 style='color:{st.session_state.theme};'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🗂️ Word Vault", "🏆 Leaderboard"])
        if st.button("EXIT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- DASHBOARD (NO GRAPH) ---
    if page == "🏠 Base":
        st.markdown(f"<h1>COMMAND CENTER</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,))
        txp = c.fetchone()[0] or 0
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='gaming-card'>🏆 TOTAL XP<br><h2 style='color:{st.session_state.theme};'>{txp}</h2></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='gaming-card'>🎖️ RANK<br><h2 style='color:{st.session_state.theme};'>{'LEGEND' if txp > 500 else 'WARRIOR'}</h2></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='gaming-card'>⚡ LEVEL<br><h2 style='color:{st.session_state.theme};'>{1 + (txp // 100)}</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='gaming-card'><h3>CURRENT MISSION</h3><p>Complete Training or defeat the Boss to earn more XP!</p></div>", unsafe_allow_html=True)

    # --- MCQ TRAINING (UNLIMITED QUESTIONS) ---
    elif page == "🎓 Training":
        st.markdown("<h1>MCQ TRAINING ZONE</h1>", unsafe_allow_html=True)
        q = random.choice(MCQ_DATA)
        st.markdown(f"<div class='gaming-card'><div class='question-text'>{q['q']}</div></div>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            with cols[i%2]:
                if st.button(opt, key=f"q_{i}_{time.time()}"): # key fixed for unlimited questions
                    if opt == q['a']:
                        st.balloons()
                        c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today())))
                        conn.commit()
                        st.success("Correct! +10 XP")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Wrong Choice! Try again.")

    # --- BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; text-shadow: 0 0 20px #ff4b4b;'>⚔️ BOSS RECKONING</h1>", unsafe_allow_html=True)
        
        col_p, col_b = st.columns(2)
        with col_p:
            st.markdown(f"**HERO: {st.session_state.player_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"**BOSS: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS DEFEATED! +100 XP")
            c.execute("INSERT INTO progress VALUES (?, ?, 100)", (st.session_state.email, str(date.today()))); conn.commit()
            if st.button("SPAWN NEW BOSS"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("YOU DIED!"); if st.button("REVIVE"): st.session_state.player_hp = 100; st.session_state.boss_hp = 100; st.rerun()
        else:
            q = random.choice(MCQ_DATA)
            st.markdown(f"<div class='gaming-card'><h3>CHALLENGE: {q['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("ATTACK MOVE:", q['o'], horizontal=True)
            if st.button("💥 HIT BOSS"):
                if ans == q['a']:
                    st.session_state.combo += 1
                    dmg = 20 * st.session_state.combo
                    st.session_state.boss_hp -= dmg
                    st.session_state.battle_log = f"CRITICAL HIT! -{dmg} HP"
                else:
                    st.session_state.combo = 0
                    st.session_state.player_hp -= 20
                    st.session_state.battle_log = "BOSS HIT YOU! -20 HP"
                st.rerun()
        st.info(st.session_state.battle_log)

    elif page == "🗂️ Word Vault":
        st.title("🗂️ WORD VAULT")
        w, m = st.text_input("New Word"), st.text_input("Meaning")
        if st.button("SAVE"):
            if w and m:
                c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                conn.commit(); st.rerun()
        rows = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        for r in rows: st.markdown(f"<div class='gaming-card' style='padding:10px;'>{r[0]} : {r[1]}</div>", unsafe_allow_html=True)

    elif page == "🏆 Leaderboard":
        st.title("🏆 RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.markdown(f"<div class='gaming-card'>#{i+1} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)
