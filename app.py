import streamlit as st
import sqlite3
from datetime import date
import random
import time

# ==========================================
# 🛠️ DATABASE SETUP
# ==========================================
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

# --- Data Pool ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"}
]

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "STEVNATION", "player@guru.ai"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# ==========================================
# 🎨 GAMER UI DESIGN (CYAN & DARK)
# ==========================================
st.set_page_config(page_title="GURU AI - PRO", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    /* Main Background */
    .stApp { background-color: #0e1117; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    /* Neon Header */
    .neon-text { color: #00f2ff; font-family: 'Bungee'; text-shadow: 0 0 10px #00f2ff; }
    
    /* Gamer Cards */
    .gamer-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        border-top: 3px solid #00f2ff;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .stat-val { font-family: 'Bungee'; font-size: 28px; color: #00f2ff; }
    
    /* Progress Bars */
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00f2ff , #7000ff) !important; }
    
    /* Buttons */
    .stButton>button {
        background: transparent;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        border-radius: 10px;
        font-family: 'Bungee';
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover { background: #00f2ff !important; color: #0e1117 !important; box-shadow: 0 0 20px #00f2ff; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0a0c10; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🚀 CORE LOGIC
# ==========================================
txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)
xp_in_level = txp % 100

# Top Branding
st.markdown("<h1 class='neon-text'>GURU AI <span style='color:white;'>| ENGLISH GURU PRO</span> 🎮</h1>", unsafe_allow_html=True)

# Navigation
with st.sidebar:
    st.image(f"https://api.dicebear.com/7.x/pixel-art/svg?seed={st.session_state.user}", width=100)
    st.write(f"👾 **{st.session_state.user}**")
    menu = st.radio("MAIN MENU", ["📊 Dashboard", "🎯 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Hall of Fame"])
    st.divider()
    if st.button("LOGOUT"): st.session_state.logged_in = False; st.rerun()

if menu == "📊 Dashboard":
    st.write("### COMMAND CENTER")
    
    # Row 1: Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='gamer-card'><small>LEVEL</small><div class='stat-val'>{user_level}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='gamer-card'><small>TOTAL XP</small><div class='stat-val'>{txp}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='gamer-card'><small>STREAK</small><div class='stat-val'>🔥 5</div></div>", unsafe_allow_html=True)
    with col4:
        c.execute("SELECT COUNT(*) FROM dictionary WHERE email=?", (st.session_state.email,))
        st.markdown(f"<div class='gamer-card'><small>WORDS</small><div class='stat-val'>{c.fetchone()[0]}</div></div>", unsafe_allow_html=True)

    st.write("")
    
    # Row 2: Progress & Missions
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.markdown("<div class='gamer-card'>", unsafe_allow_html=True)
        st.subheader("⚡ Level Progress")
        st.progress(max(0.0, min(xp_in_level / 100.0, 1.0)))
        st.write(f"**{100 - xp_in_level} XP** needed for next rank")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.write("#### 📜 Recent Activity")
        history = c.execute("SELECT date, xp FROM progress WHERE email=? ORDER BY rowid DESC LIMIT 3", (st.session_state.email,)).fetchall()
        for d, x in history: st.caption(f"📅 {d} — Earned {x} XP")

    with c_right:
        st.markdown("<div class='gamer-card' style='border-top-color:#7000ff; text-align:center;'>", unsafe_allow_html=True)
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

elif menu == "🎯 Training":
    st.title("🎯 Training Zone")
    if 't_q' not in st.session_state: st.session_state.t_q = random.choice(TRAINING_DATA)
    q = st.session_state.t_q
    
    st.markdown(f"<div class='gamer-card' style='text-align:center;'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
    st.write("")
    
    cols = st.columns(2)
    for i, opt in enumerate(q['o']):
        with cols[i%2]:
            if st.button(opt):
                if opt == q['a']:
                    st.toast("CORRECT! +10 XP", icon="⚡")
                    c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 10))
                    conn.commit(); time.sleep(1); del st.session_state.t_q; st.rerun()
                else: st.error("MISSION FAILED!")

elif menu == "⚔️ Boss Battle":
    st.markdown("<h1 class='neon-text' style='text-align:center;'>👹 BOSS BATTLE</h1>", unsafe_allow_html=True)
    boss_max = 100 + (user_level * 25)
    
    col_p, col_b = st.columns(2)
    col_p.progress(max(0.0, min(st.session_state.player_hp / 100.0, 1.0)))
    col_p.write("🛡️ HERO HP")
    
    col_b.progress(max(0.0, min(st.session_state.boss_hp / boss_max, 1.0)))
    col_b.write("👾 BOSS HP")

    st.markdown("<div style='text-align:center;'><img src='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJmZzZ4eXN6ZzZ4eXN6ZzZ4eXN6ZzZ4eXN6ZzZ4eXN6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxxXLyKHzvW/giphy.gif' width='200'></div>", unsafe_allow_html=True)
    
    if st.button("🔥 UNLEASH ATTACK"):
        st.session_state.boss_hp -= 25; st.rerun()

elif menu == "🏆 Hall of Fame":
    st.title("🏆 Leaderboard")
    data = c.execute("SELECT username, SUM(xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC LIMIT 10").fetchall()
    for i, row in enumerate(data, 1):
        color = "#00f2ff" if i==1 else "white"
        st.markdown(f"<div class='gamer-card' style='margin-bottom:10px; color:{color};'>#{i} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)
