import streamlit as st
import sqlite3
import hashlib
from datetime import date, timedelta
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_final_v28.db', check_same_thread=False)
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

# --- 3. MCQ DATA ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"}
]

# --- 4. CSS (PREMIUM DARK LOOK) ---
st.set_page_config(page_title="English Guru Pro", page_icon="⚡", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
    .stApp {{ 
        background: radial-gradient(circle at center, #1a1a2e 0%, #0d0d14 100%);
        background-attachment: fixed;
        font-family: 'Rajdhani', sans-serif;
        color: #e0e0e0;
    }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.03);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid {st.session_state.theme};
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
        transition: 0.3s;
    }}
    .hp-bar {{ height: 15px; border-radius: 10px; background: #222; overflow: hidden; margin-bottom: 5px; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    .stButton>button {{
        background: transparent;
        color: {st.session_state.theme} !important;
        border: 2px solid {st.session_state.theme} !important;
        border-radius: 8px; font-weight: bold; padding: 10px 20px; width: 100%;
    }}
    .stButton>button:hover {{ background: {st.session_state.theme} !important; color: #000 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-size: 3.5rem;'>⚡ ENGLISH GURU ARENA</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:  # <-- FIXED LINE HERE
        t1, t2 = st.tabs(["🔑 ACCESS PORTAL", "📝 NEW REGISTRATION"])
        with t1:
            e = st.text_input("Email")
            p = st.text_input("Password", type='password')
            if st.button("ENTER PORTAL"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
                else: st.error("Invalid credentials.")
        with t2:
            ne, nu, np = st.text_input("User Email"), st.text_input("Warrior Name"), st.text_input("Create Password", type='password')
            if st.button("CREATE HERO"):
                if "@" in ne:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, ne
                        st.rerun()
                    except: st.error("Email already registered.")

# --- 6. MAIN CONTENT ---
else:
    with st.sidebar:
        st.markdown(f"<h3>⚔️ {st.session_state.user}</h3>", unsafe_allow_html=True)
        page = st.radio("SELECT MISSION", ["🏠 Dashboard", "🎯 MCQ Training", "⚔️ Boss Battle", "🗂️ Word Vault", "🏆 Leaderboard", "⚙️ Settings"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "🏠 Dashboard":
        st.markdown(f"<h1>Welcome, Warrior {st.session_state.user}</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,))
        txp = c.fetchone()[0] or 0
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='metric-card'>🏆 XP<h3>{txp}</h3></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='metric-card'>🎖️ RANK<h3>{'ELITE' if txp > 500 else 'NOVICE'}</h3></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='metric-card'>🔥 DAYS<h3>1</h3></div>", unsafe_allow_html=True)
        st.write("### 📈 Recent Activity")
        dates = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        xp_vals = [c.execute("SELECT SUM(xp) FROM progress WHERE email=? AND date=?", (st.session_state.email, d)).fetchone()[0] or 0 for d in dates]
        st.area_chart(pd.DataFrame({"XP": xp_vals}, index=[d[5:] for d in dates]), color=st.session_state.theme)

    elif page == "🎯 MCQ Training":
        st.title("🎯 MCQ TRAINING")
        q = random.choice(MCQ_DATA)
        st.markdown(f"<div class='metric-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            with cols[i%2]:
                if st.button(opt, key=f"q_{i}"):
                    if opt == q['a']:
                        st.balloons(); st.success("Correct! +10 XP")
                        c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today())))
                        conn.commit(); time.sleep(1); st.rerun()
                    else: st.error("Try again!")

    elif page == "⚔️ Boss Battle":
        st.title("⚔️ DARK BOSS CHALLENGE")
        cp, cb = st.columns(2)
        with cp:
            st.write(f"Hero: {st.session_state.player_hp}%")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        with cb:
            st.write(f"Boss: {st.session_state.boss_hp}%")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)
        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS DEFEATED! +100 XP")
            c.execute("INSERT INTO progress VALUES (?, ?, 100)", (st.session_state.email, str(date.today()))); conn.commit()
            if st.button("New Battle"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
        else:
            q = random.choice(MCQ_DATA)
            st.markdown(f"<div class='metric-card'><h4>{q['q']}</h4></div>", unsafe_allow_html=True)
            ans = st.radio("Options", q['o'], horizontal=True)
            if st.button("💥 ATTACK"):
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

    elif page == "🗂️ Word Vault":
        st.title("🗂️ WORD VAULT")
        w, m = st.text_input("New Word"), st.text_input("Definition")
        if st.button("Save Word"):
            if w and m:
                c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                conn.commit(); st.rerun()
        rows = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        for r in rows: st.markdown(f"<div class='metric-card' style='padding:10px; margin-bottom:5px;'>{r[0]} : {r[1]}</div>", unsafe_allow_html=True)

    elif page == "🏆 Leaderboard":
        st.title("🏆 TOP WARRIORS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.markdown(f"<div class='metric-card'>#{i+1} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)

    elif page == "⚙️ Settings":
        st.title("⚙️ SETTINGS")
        st.session_state.theme = st.color_picker("Glow Color", st.session_state.theme)
