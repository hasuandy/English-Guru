import streamlit as st
import sqlite3
import hashlib
from datetime import date, timedelta
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v28_final.db', check_same_thread=False)
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

# --- 4. ULTRA ATTRACTIVE CSS ---
st.set_page_config(page_title="English Guru V28 Pro", page_icon="⚡", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    .stApp {{ 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://wallpaperaccess.com/full/2565415.jpg');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Orbitron', sans-serif;
    }}
    
    /* Neon Pulse Cards */
    .metric-card {{
        background: rgba(0, 0, 0, 0.6);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid {st.session_state.theme};
        text-align: center;
        box-shadow: 0 0 15px {st.session_state.theme}, inset 0 0 10px {st.session_state.theme}33;
        transition: 0.3s;
    }}
    .metric-card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 0 30px {st.session_state.theme};
    }}

    /* HP Bars Gaming Look */
    .hp-bar {{ height: 25px; border-radius: 15px; background: #222; border: 1px solid #444; overflow: hidden; }}
    .hp-fill {{ height: 100%; transition: width 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}

    /* Glassmorphism Login Box */
    [data-testid="stVerticalBlock"] > div:has(div.stTabs) {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 50px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #00dbde 0%, {st.session_state.theme} 100%);
        color: white !important;
        border-radius: 50px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: none;
        padding: 15px;
        box-shadow: 0 5px 15px {st.session_state.theme}66;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 25px {st.session_state.theme};
        transform: scale(1.05);
    }}

    h1, h2 {{ 
        color: {st.session_state.theme}; 
        text-shadow: 0 0 20px {st.session_state.theme};
        font-weight: 700;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='font-size: 4rem;'>🛡️ ARENA V28</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.8,1])
    with c2:
        tab1, tab2 = st.tabs(["⚡ ACCESS LOGIN", "📝 CREATE HERO"])
        with tab1:
            e = st.text_input("Email", placeholder="warrior@arena.com")
            p = st.text_input("Secret Key", type='password', placeholder="••••••••")
            if st.button("INITIALIZE MISSION"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
                else: st.error("Access Denied! Check Credentials.")
        with tab2:
            ne, nu, np = st.text_input("Email ID"), st.text_input("Hero Name"), st.text_input("Password", type='password')
            if st.button("REGISTER HERO"):
                if "@" in ne:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, ne
                        st.rerun()
                    except: st.error("Email already in database!")

# --- 6. MAIN ARENA ---
else:
    with st.sidebar:
        st.markdown(f"<h1 style='font-size: 1.5rem;'>⭐ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        page = st.radio("SELECT MISSION:", ["🏠 Command Center", "🎓 MCQ Training", "⚔️ Boss Battle", "🗂️ Word Vault", "🏆 Rankings", "⚙️ Setup"])
        if st.button("🚪 Leave Arena"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "🏠 Command Center":
        st.markdown("<h1>CORE DASHBOARD</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,))
        total_xp = c.fetchone()[0] or 0
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='metric-card'>🏆<br>TOTAL XP<h2 style='margin:0;'>{total_xp}</h2></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='metric-card'>🎖️<br>RANK<h2 style='margin:0;'>{'ELITE' if total_xp > 500 else 'NOVICE'}</h2></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='metric-card'>🔥<br>STREAK<h2 style='margin:0;'>V28 ON</h2></div>", unsafe_allow_html=True)

        st.write("### 📈 Battle Evolution")
        dates = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        xp_vals = [c.execute("SELECT SUM(xp) FROM progress WHERE email=? AND date=?", (st.session_state.email, d)).fetchone()[0] or 0 for d in dates]
        st.area_chart(pd.DataFrame({"XP": xp_vals}, index=[d[5:] for d in dates]), color=st.session_state.theme)

    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b;'>⚔️ BOSS RECKONING</h1>", unsafe_allow_html=True)
        # Boss Battle UI is much more attractive now
        col_p, col_b = st.columns(2)
        with col_p:
            st.markdown(f"**HERO HP: {st.session_state.player_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:linear-gradient(90deg, #00f260, #0575e6);'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"**BOSS HP: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:linear-gradient(90deg, #ff416c, #ff4b2b);'></div></div>", unsafe_allow_html=True)
        
        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS DESTROYED! +100 XP")
            c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 100)); conn.commit()
            if st.button("Spawn New Boss"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
        else:
            q = random.choice(MCQ_DATA)
            st.markdown(f"<div class='metric-card'><h3>MISSION: {q['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("Choose Attack Move:", q['o'], horizontal=True)
            if st.button("💥 INITIATE ATTACK"):
                if ans == q['a']:
                    st.session_state.combo += 1
                    dmg = 20 * st.session_state.combo
                    st.session_state.boss_hp -= dmg
                    st.session_state.battle_log = f"🔥 CRITICAL HIT! -{dmg} HP"
                else:
                    st.session_state.combo = 0
                    st.session_state.player_hp -= 20
                    st.session_state.battle_log = "⚠️ COUNTER ATTACK! -20 HP"
                st.rerun()
        st.warning(st.session_state.battle_log)

    elif page == "🗂️ Word Vault":
        st.title("🗂️ ANCIENT VAULT")
        w, m = st.text_input("New Word"), st.text_input("Definition")
        if st.button("🔒 ENCRYPT & SAVE"):
            if w and m:
                c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                conn.commit(); st.rerun()
        
        rows = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        for r in rows:
            st.markdown(f"<div class='metric-card' style='padding:10px; margin:5px;'><b>{r[0]}</b> : {r[1]}</div>", unsafe_allow_html=True)

    elif page == "🏆 Rankings":
        st.title("🏆 LEADERBOARD")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            rank_icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🎖️"
            st.markdown(f"<div class='metric-card'><h4>{rank_icon} {row[0]} — {row[1]} XP</h4></div>", unsafe_allow_html=True)

    elif page == "⚙️ Setup":
        st.title("⚙️ ARENA SETTINGS")
        st.session_state.theme = st.color_picker("Customize UI Glow", st.session_state.theme)
        st.info("The arena color will reflect your choice instantly.")
