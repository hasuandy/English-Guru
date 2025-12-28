import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random

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

# --- session state ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

# DEV MODE AUTO-LOGIN
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"

# --- UI CONFIG ---
st.set_page_config(page_title="English Guru Dash", page_icon="🎮", layout="wide")

# CUSTOM CSS FOR DASHBOARD
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #0e1117; color: white; font-family: 'Rajdhani', sans-serif; }}
    
    /* Stats Cards */
    .stat-card {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid {st.session_state.theme};
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        text-align: center;
    }}
    .stat-value {{ font-family: 'Bungee'; font-size: 24px; color: {st.session_state.theme}; }}
    .stat-label {{ font-size: 14px; color: #888; text-transform: uppercase; }}
    
    /* Main Card */
    .main-card {{
        background: linear-gradient(145deg, #1e2130, #161922);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #333;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- UTILS ---
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

# ==========================================
# 🏠 MAIN APP
# ==========================================
if st.session_state.logged_in:
    txp = get_total_xp(st.session_state.email)
    user_level = 1 + (txp // 100)
    xp_in_level = txp % 100
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>GURU V37</h1>", unsafe_allow_html=True)
        st.info(f"👤 Hero: {st.session_state.user}")
        page = st.radio("Navigation", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # --- DASHBOARD PAGE ---
    if page == "🏠 Dashboard":
        st.markdown(f"<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        
        # Row 1: Quick Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>Current Level</div><div class='stat-value'>{user_level}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-card'><div class='stat-label'>Total XP</div><div class='stat-value'>{txp}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='stat-card' style='border-left-color:#ff4b4b;'><div class='stat-label'>Streak</div><div class='stat-value'>🔥 3 Days</div></div>", unsafe_allow_html=True)
        with col4:
            c.execute("SELECT COUNT(*) FROM dictionary WHERE email=?", (st.session_state.email,))
            words_count = c.fetchone()[0]
            st.markdown(f"<div class='stat-card' style='border-left-color:#7000ff;'><div class='stat-label'>Words Learnt</div><div class='stat-value'>{words_count}</div></div>", unsafe_allow_html=True)

        st.write("") # Spacer

        # Row 2: Progress & Daily Task
        row2_col1, row2_col2 = st.columns([2, 1])
        
        with row2_col1:
            st.markdown("<div class='main-card'>", unsafe_allow_html=True)
            st.subheader("🎯 Level Progress")
            st.write(f"XP to Level {user_level + 1}: **{100 - xp_in_level} XP needed**")
            st.progress(xp_in_level / 100)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("")
            st.subheader("📜 Recent Activity")
            history = c.execute("SELECT date, xp FROM progress WHERE email=? ORDER BY rowid DESC LIMIT 3", (st.session_state.email,)).fetchall()
            if history:
                for d, x in history:
                    st.write(f"✅ Received `{x} XP` on {d}")
            else:
                st.write("No activity yet. Start training!")

        with row2_col2:
            st.markdown("<div class='main-card' style='text-align:center;'>", unsafe_allow_html=True)
            st.subheader("Daily Gift")
            today = str(date.today())
            c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
            if not c.fetchone():
                st.write("You have a daily reward waiting!")
                if st.button("CLAIM 50 XP", use_container_width=True):
                    c.execute("INSERT INTO daily_tasks VALUES (?, ?, ?)", (st.session_state.email, today, 1))
                    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, today, 50))
                    conn.commit()
                    st.balloons()
                    st.rerun()
            else:
                st.success("Reward Claimed Today!")
            st.markdown("</div>", unsafe_allow_html=True)

    # --- TRAINING PAGE ---
    elif page == "🎓 Training":
        st.title("🎓 Training Zone")
        st.write("Complete MCQs to earn XP and build your Dictionary.")
        # [Tumhara purana training code yahan aayega]
        st.warning("Training modules active. Choose a task from the tabs.")

    # --- BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.title("⚔️ Monster Arena")
        # [Tumhara purana boss battle code yahan aayega]
        st.error("Level 5 required for the Dragon Boss!")

    # --- SHOP ---
    elif page == "🛒 Shop":
        st.title("🛒 Item Shop")
        # [Tumhara purana shop code yahan aayega]
        st.write("Buy shields and potions using XP.")

else:
    st.title("Login to English Guru")
    st.info("Dev Mode is ON: Auto-logging in...")
