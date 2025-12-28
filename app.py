import streamlit as st
import sqlite3
from datetime import date
import random
import time

# --- DB & Setup ---
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

# --- Training Data ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"}
]

# --- Session ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "STEVNATION", "player@guru.ai"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# ==========================================
# 🎨 ULTRA-GAMER CSS (FIXED)
# ==========================================
st.set_page_config(page_title="GURU AI PRO", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    .stApp { background-color: #0b0e14; color: white; font-family: 'Rajdhani', sans-serif; }
    
    /* Neon Header */
    .title-neon { color: #00f2ff; font-family: 'Bungee'; text-align: left; text-shadow: 0 0 15px #00f2ff; font-size: 40px; }
    
    /* Gamer Cards */
    .card {
        background: #161b22; border: 1px solid #30363d;
        border-radius: 12px; padding: 20px; text-align: center;
        border-top: 4px solid #00f2ff;
    }
    .stat-val { font-family: 'Bungee'; font-size: 32px; color: #00f2ff; margin-top: 10px; }
    .stat-label { color: #8b949e; font-size: 14px; text-transform: uppercase; }

    /* Battle Sword Icon */
    .sword-icon { font-size: 60px; color: #00f2ff; margin: 20px 0; text-shadow: 0 0 20px #00f2ff; }

    /* Buttons */
    .stButton>button {
        background: transparent !important; color: #00f2ff !important;
        border: 2px solid #00f2ff !important; border-radius: 8px !important;
        font-family: 'Bungee' !important; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background: #00f2ff !important; color: #0b0e14 !important; box-shadow: 0 0 20px #00f2ff; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- Data Fetch ---
txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)
xp_in_level = txp % 100

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2ff; font-family:Bungee;'>GURU AI</h2>", unsafe_allow_html=True)
    st.image(f"https://api.dicebear.com/7.x/pixel-art/svg?seed={st.session_state.user}", width=80)
    st.write(f"USER: **{st.session_state.user}**")
    st.divider()
    menu = st.radio("MENU", ["🖥️ Dashboard", "🎯 Training", "⚔️ Boss Battle", "🛒 Shop"])

# ==========================================
# 🏠 COMMAND CENTER (DASHBOARD)
# ==========================================
if menu == "🖥️ Dashboard":
    st.markdown("<h1 class='title-neon'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    
    # Stat Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='card'><div class='stat-label'>Level</div><div class='stat-val'>{user_level}</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card'><div class='stat-label'>Total XP</div><div class='stat-val'>{txp}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card' style='border-top-color:#ff4b4b;'><div class='stat-label'>Streak</div><div class='stat-val'>🔥 5</div></div>", unsafe_allow_html=True)
    with c4: 
        cnt = c.execute("SELECT COUNT(*) FROM dictionary WHERE email=?", (st.session_state.email,)).fetchone()[0]
        st.markdown(f"<div class='card' style='border-top-color:#7000ff;'><div class='stat-label'>Words</div><div class='stat-val'>{cnt}</div></div>", unsafe_allow_html=True)

    st.write("---")
    
    # Main Section
    col_main, col_daily = st.columns([2, 1])
    
    with col_main:
        st.markdown("<div class='card' style='text-align:left;'>", unsafe_allow_html=True)
        st.subheader("🛡️ Level Progress")
        st.progress(max(0.0, min(xp_in_level / 100.0, 1.0)))
        st.write(f"Progress: {xp_in_level}% | Next Level: {100-xp_in_level} XP left")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.write("### 📜 Recent Missions")
        history = c.execute("SELECT date, xp FROM progress WHERE email=? ORDER BY rowid DESC LIMIT 3", (st.session_state.email,)).fetchall()
        for d, x in history: st.info(f"✅ Mission Cleared: +{x} XP on {d}")

    with col_daily:
        st.markdown("<div class='card' style='border-top-color:#00f2ff;'>", unsafe_allow_html=True)
        st.subheader("🎁 Daily Gift")
        today = str(date.today())
        c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
        if not c.fetchone():
            if st.button("CLAIM 50 XP"):
                c.execute("INSERT INTO daily_tasks VALUES (?, ?, ?)", (st.session_state.email, today, 1))
                c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, today, 50))
                conn.commit(); st.balloons(); st.rerun()
        else: st.success("Gift Claimed!")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ⚔️ BATTLE MODE (FIXED IMAGE STYLE)
# ==========================================
elif menu == "⚔️ Boss Battle":
    st.markdown("<h1 class='title-neon' style='text-align:center;'>BOSS ARENA</h1>", unsafe_allow_html=True)
    
    col_p, col_mid, col_b = st.columns([2, 1, 2])
    
    with col_p:
        st.markdown(f"<div class='card'><b>HERO</b><div class='stat-val' style='color:#ff4b4b;'>{st.session_state.player_hp}%</div></div>", unsafe_allow_html=True)
    with col_mid:
        st.markdown("<div style='text-align:center;' class='sword-icon'>⚔️</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<div class='card'><b>BOSS</b><div class='stat-val'>{st.session_state.boss_hp}%</div></div>", unsafe_allow_html=True)

    st.write("---")
    if st.button("🔥 UNLEASH COMBO ATTACK"):
        st.session_state.boss_hp -= 20
        st.toast("CRITICAL HIT!")
        st.rerun()

elif menu == "🎯 Training":
    st.title("🎯 MCQ TRAINING")
    # Training code... (same logic as before)
