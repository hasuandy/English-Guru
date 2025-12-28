import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# ==========================================
# 🛠️ SETTINGS & DATABASE
# ==========================================
DEV_MODE = True 
DB_NAME = 'english_guru_pro_v37.db'

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
    c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
    conn.commit()

init_db()

# --- Data Pools ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
    {"q": "I ____ a student.", "o": ["is", "am", "are", "be"], "a": "am"}
]

BOSS_POOL = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"}
]

# --- Session State ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"
    # Ensure user exists in DB for leaderboard
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

# --- UI CONFIG ---
st.set_page_config(page_title="English Guru Pro", page_icon="🎓", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #0e1117; color: white; font-family: 'Rajdhani', sans-serif; }}
    .stat-card {{ background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border-left: 5px solid {st.session_state.theme}; text-align: center; }}
    .stat-value {{ font-family: 'Bungee'; font-size: 24px; color: {st.session_state.theme}; }}
    .main-card {{ background: linear-gradient(145deg, #1e2130, #161922); padding: 25px; border-radius: 20px; border: 1px solid #333; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border: none; border-radius: 10px; transition: 0.3s; }}
    .stButton>button:hover {{ transform: scale(1.05); box-shadow: 0 0 15px {st.session_state.theme}; }}
    </style>
    """, unsafe_allow_html=True)

# --- Helper Functions ---
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def check_training_answer(user_choice, correct_answer):
    if user_choice.replace("✨ ", "") == correct_answer:
        st.session_state.combo += 1
        gain = 10 if st.session_state.combo < 3 else 20
        c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), gain))
        conn.commit()
        st.toast(f"✅ Correct! +{gain} XP", icon="🔥")
    else:
        st.session_state.combo = 0
        st.toast(f"❌ Wrong! Correct: {correct_answer}", icon="💀")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# ==========================================
# 🚀 MAIN APP LOGIC
# ==========================================
if st.session_state.logged_in:
    txp = get_total_xp(st.session_state.email)
    user_level = 1 + (txp // 100)
    xp_in_level = txp % 100
    
    with st.sidebar:
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>GURU V37</h1>", unsafe_allow_html=True)
        st.write(f"🎖️ Level: {user_level} | 🔥 Combo: {st.session_state.combo}")
        page = st.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Hall of Fame"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- 🏠 DASHBOARD ---
    if page == "🏠 Dashboard":
        st.markdown(f"<h1 style='font-family:Bungee;'>HERO COMMAND CENTER</h1>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f"<div class='stat-card'><small>LEVEL</small><div class='stat-value'>{user_level}</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-card'><small>TOTAL XP</small><div class='stat-value'>{txp}</div></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='stat-card' style='border-left-color:#ff4b4b;'><small>STREAK</small><div class='stat-value'>🔥 5 DAYS</div></div>", unsafe_allow_html=True)
        with col4: 
            c.execute("SELECT COUNT(*) FROM dictionary WHERE email=?", (st.session_state.email,))
            st.markdown(f"<div class='stat-card' style='border-left-color:#7000ff;'><small>WORDS</small><div class='stat-value'>{c.fetchone()[0]}</div></div>", unsafe_allow_html=True)

        st.write("### 🎯 Level Progress")
        st.progress(xp_in_level / 100)
        
        st.write("")
        c_left, c_right = st.columns([2, 1])
        with c_left:
            st.subheader("📜 Recent Missions")
            history = c.execute("SELECT date, xp FROM progress WHERE email=? ORDER BY rowid DESC LIMIT 3", (st.session_state.email,)).fetchall()
            for d, x in history: st.info(f"📅 {d}: Earned {x} XP")
        with c_right:
            st.subheader("🎁 Daily Gift")
            today = str(date.today())
            c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
            if not c.fetchone():
                if st.button("CLAIM 50 XP"):
                    c.execute("INSERT INTO daily_tasks VALUES (?, ?, ?)", (st.session_state.email, today, 1))
                    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, today, 50))
                    conn.commit(); st.balloons(); st.rerun()
            else: st.success("Gift Claimed!")

    # --- 🎓 TRAINING ---
    elif page == "🎓 Training":
        st.markdown(f"<h1 style='font-family:Bungee;'>🎓 TRAINING ZONE</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🎯 MCQs", "📖 DICTIONARY"])
        with t1:
            if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAINING_DATA)
            tq = st.session_state.current_tq
            st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:30px; border-radius:20px; border:2px solid {st.session_state.theme}; text-align:center;'><h2>{tq['q']}</h2></div>", unsafe_allow_html=True)
            st.write("")
            cols = st.columns(2)
            for i, opt in enumerate(tq['o']):
                with cols[i%2]: 
                    if st.button(f"✨ {opt}", key=f"opt_{i}", use_container_width=True):
                        check_training_answer(opt, tq['a']); st.rerun()
        with t2:
            st.subheader("Add New Word")
            w = st.text_input("Word")
            m = st.text_input("Meaning")
            if st.button("SAVE WORD"):
                if w and m:
                    c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                    conn.commit(); st.success("Added!")

    # --- ⚔️ BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee; text-align:center;'>👹 MONSTER ARENA</h1>", unsafe_allow_html=True)
        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"HERO: {st.session_state.player_hp}%")
            st.progress(st.session_state.player_hp / 100)
        with col_b:
            boss_max = 100 + (user_level * 25)
            st.write(f"BOSS: {int((st.session_state.boss_hp/boss_max)*100)}%")
            st.progress(st.session_state.boss_hp / boss_max)
        
        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("Victory!"); st.button("SPAWN NEXT", on_click=lambda: setattr(st.session_state, 'boss_hp', 150))
        elif st.session_state.player_hp <= 0:
            st.error("Defeated!"); st.button("REVIVE", on_click=lambda: setattr(st.session_state, 'player_hp', 100))
        else:
            if 'bq' not in st.session_state: st.session_state.bq = random.choice(BOSS_POOL)
            st.markdown(f"<div class='main-card' style='text-align:center;'><h3>{st.session_state.bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("Select Answer:", st.session_state.bq['o'], horizontal=True)
            if st.button("🔥 ATTACK"):
                if ans == st.session_state.bq['a']:
                    st.session_state.boss_hp -= 40; st.toast("Hit!")
                else:
                    st.session_state.player_hp -= 20; st.toast("Ouch!")
                del st.session_state.bq; st.rerun()

    # --- 🏆 HALL OF FAME ---
    elif page == "🏆 Hall of Fame":
        st.markdown("<h1 style='font-family:Bungee; text-align:center;'>🏆 HALL OF FAME</h1>", unsafe_allow_html=True)
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        if data:
            cols = st.columns(3)
            with cols[1]: # Rank 1
                st.markdown(f"<div style='text-align:center; padding:20px; border:2px solid gold; border-radius:15px;'>👑<br><b>{data[0][0]}</b><br>{data[0][1]} XP</div>", unsafe_allow_html=True)
            st.write("---")
            for i, row in enumerate(data[1:], 2):
                st.write(f"#{i} {row[0]} — {row[1]} XP")

    # --- 🛒 SHOP ---
    elif page == "🛒 Shop":
        st.markdown("<h1 style='font-family:Bungee;'>🛒 ITEM SHOP</h1>", unsafe_allow_html=True)
        st.write(f"Your Balance: **{txp} XP**")
        if st.button("Buy Shield (50 XP)"):
            if txp >= 50:
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), -50))
                c.execute("INSERT INTO inventory VALUES (?, '🛡️ Mystic Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1", (st.session_state.email,))
                conn.commit(); st.success("Purchased!"); st.rerun()
