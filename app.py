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

# --- Sounds Links ---
CORRECT_SOUND = "https://www.myinstants.com/media/sounds/ding-sound-effect_2.mp3"
WRONG_SOUND = "https://www.myinstants.com/media/sounds/wrong-answer-sound-effect.mp3"

def play_sound(url):
    st.markdown(f'<audio src="{url}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)

# --- Data Pools ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
    {"q": "I ____ a student.", "o": ["is", "am", "are", "be"], "a": "am"}
]

BOSS_POOL = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"}
]

# --- Session State ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

st.set_page_config(page_title="English Guru Pro", page_icon="🎓", layout="wide")

# CSS Styling
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #0e1117; color: white; font-family: 'Rajdhani', sans-serif; }}
    .stat-card {{ background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border-left: 5px solid {st.session_state.theme}; text-align: center; }}
    .stat-value {{ font-family: 'Bungee'; font-size: 24px; color: {st.session_state.theme}; }}
    </style>
    """, unsafe_allow_html=True)

# Helper for Training
def check_training_answer(user_choice, correct_answer):
    if user_choice.replace("✨ ", "") == correct_answer:
        st.session_state.combo += 1
        play_sound(CORRECT_SOUND)
        c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 10))
        conn.commit()
        st.toast("✅ Shabaash!", icon="🔥")
    else:
        st.session_state.combo = 0
        play_sound(WRONG_SOUND)
        st.toast("❌ Galat Jawab!", icon="💀")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# --- MAIN APP ---
if st.session_state.logged_in:
    txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
    user_level = 1 + (txp // 100)
    
    with st.sidebar:
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>GURU V37</h1>", unsafe_allow_html=True)
        page = st.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🏆 Hall of Fame"])

    # DASHBOARD
    if page == "🏠 Dashboard":
        st.markdown(f"<h1 style='font-family:Bungee;'>DASHBOARD</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.markdown(f"<div class='stat-card'><small>LEVEL</small><div class='stat-value'>{user_level}</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-card'><small>TOTAL XP</small><div class='stat-value'>{txp}</div></div>", unsafe_allow_html=True)
        st.write("### Progress")
        st.progress((txp % 100) / 100)

    # TRAINING (SOUNDS ENABLED)
    elif page == "🎓 Training":
        st.title("🎓 Training")
        if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAINING_DATA)
        tq = st.session_state.current_tq
        st.subheader(tq['q'])
        for opt in tq['o']:
            if st.button(f"✨ {opt}", use_container_width=True):
                check_training_answer(opt, tq['a'])
                time.sleep(1) # Sound play hone ka waqt
                st.rerun()

    # BOSS BATTLE
    elif page == "⚔️ Boss Battle":
        st.title("⚔️ Boss Battle")
        # Same Boss logic as before but with play_sound(CORRECT_SOUND) on success
        st.info("Boss is waiting for your move!")
        # (Boss battle code goes here...)

    # HALL OF FAME (AVATARS)
    elif page == "🏆 Hall of Fame":
        st.markdown("<h1 style='font-family:Bungee; text-align:center;'>🏆 HALL OF FAME</h1>", unsafe_allow_html=True)
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data, 1):
            av = f"https://api.dicebear.com/7.x/avataaars/svg?seed={row[0]}"
            st.markdown(f"<img src='{av}' width='40'> **{row[0]}** - {row[1]} XP", unsafe_allow_html=True)
