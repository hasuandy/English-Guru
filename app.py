import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP (Cloud Friendly) ---
def get_db_connection():
    # Streamlit cloud ke liye connection function
    conn = sqlite3.connect('english_guru_v37.db', check_same_thread=False)
    return conn

conn = get_db_connection()
c = conn.cursor()

# Tables create karna
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user' not in st.session_state: st.session_state.user = "Tester_Hero"
if 'email' not in st.session_state: st.session_state.email = "test@guru.com"
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

# Auto-Login for Testing
st.session_state.logged_in = True 

# --- 3. DATA POOLS ---
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

# --- 4. CSS ---
st.set_page_config(page_title="English Guru V37", layout="wide")
st.markdown(f"""
    <style>
    .stApp {{ background: #0e1117; color: white; }}
    .gaming-card {{ 
        background: rgba(255,255,255,0.05); 
        border: 2px solid {st.session_state.theme}; 
        border-radius: 15px; padding: 20px; text-align: center; 
    }}
    .stButton>button {{ background: {st.session_state.theme}; color: black !important; font-weight: bold; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# HELPER FUNCTIONS
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def check_training_answer(user_choice, correct_answer):
    if user_choice == correct_answer:
        st.session_state.combo += 1
        gain = 10 if st.session_state.combo < 3 else 20
        c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), gain))
        conn.commit()
        st.toast(f"✅ Correct! +{gain} XP")
    else:
        st.session_state.combo = 0
        st.toast(f"❌ Wrong! Answer: {correct_answer}")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# --- 5. MAIN APP ---
txp = get_total_xp(st.session_state.email)
user_level = 1 + (txp // 100)

with st.sidebar:
    st.title("🎓 English Guru")
    st.write(f"👤 **{st.session_state.user}**")
    st.write(f"🎖️ Level: {user_level} | XP: {txp}")
    page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Leaderboard"])

if page == "🏠 Base":
    st.header("🏠 Command Center")
    col1, col2 = st.columns(2)
    col1.metric("Current XP", txp)
    col2.metric("Level", user_level)
    
    # Daily Task Logic
    today = str(date.today())
    c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
    if not c.fetchone():
        if st.button("🎁 CLAIM DAILY 50 XP"):
            c.execute("INSERT INTO daily_tasks (email, task_date, completed) VALUES (?, ?, ?)", (st.session_state.email, today, 1))
            c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, today, 50))
            conn.commit()
            st.rerun()

elif page == "🎓 Training":
    st.header("🎓 Training Zone")
    t_tab1, t_tab2 = st.tabs(["🎮 MCQ Practice", "📖 Word Vault"])
    
    with t_tab1:
        if 'current_tq' not in st.session_state:
            st.session_state.current_tq = random.choice(TRAINING_DATA)
        
        tq = st.session_state.current_tq
        st.markdown(f"<div class='gaming-card'><h3>{tq['q']}</h3></div>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i, opt in enumerate(tq['o']):
            with cols[i % 2]:
                st.button(opt, key=f"btn_{i}", on_click=check_training_answer, args=(opt, tq['a']), use_container_width=True)

    with t_tab2:
        w = st.text_input("New Word")
        m = st.text_input("Meaning")
        if st.button("Save Word"):
            c.execute("INSERT INTO dictionary (email, word, meaning) VALUES (?, ?, ?)", (st.session_state.email, w, m))
            conn.commit(); st.success("Added to Vault!")

elif page == "⚔️ Boss Battle":
    st.header("⚔️ Boss Arena")
    # Simple Boss Logic
    st.progress(st.session_state.boss_hp / 100)
    st.write(f"Boss HP: {st.session_state.boss_hp}%")
    
    if st.button("🔥 SUPER ATTACK"):
        st.session_state.boss_hp -= 20
        if st.session_state.boss_hp <= 0:
            st.success("Boss Defeated! +100 XP")
            c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            st.session_state.boss_hp = 100
        st.rerun()

elif page == "🏆 Leaderboard":
    st.header("🏆 Top Warriors")
    # Dummy data agar user login setup na ho
    st.write("1. Tester_Hero - 500 XP")
    st.write(f"2. You - {txp} XP")
