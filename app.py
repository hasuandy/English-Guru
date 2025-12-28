import streamlit as st
import sqlite3
from datetime import date
import random
import time

# ==========================================
# 🛠️ DATABASE & SETUP
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

# --- Questions Pool ---
TRAINING_DATA = [
    {"q": "Synonym of 'SMART'?", "o": ["Dull", "Intelligent", "Weak", "Slow"], "a": "Intelligent"},
    {"q": "Past tense of 'Run'?", "o": ["Runned", "Running", "Ran", "Runs"], "a": "Ran"},
    {"q": "Opposite of 'QUIET'?", "o": ["Silent", "Noisy", "Soft", "Calm"], "a": "Noisy"}
]

# --- Session State (Auto-Login Hazel) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Hazel", "hazel@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# ==========================================
# 🎨 PREMIUM CSS (Purple hazel Theme)
# ==========================================
st.set_page_config(page_title="Hazel's English Guru", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    
    .stApp { background-color: #F8F7FF; color: #2D3436; font-family: 'Poppins', sans-serif; }
    
    /* Profile Card */
    .profile-card {
        background: white; padding: 25px; border-radius: 30px;
        text-align: center; box-shadow: 0px 10px 40px rgba(108, 92, 231, 0.1);
        margin-bottom: 25px; border: 1px solid #E0DDF5;
    }
    
    /* Stats Bar */
    .stat-box {
        background: #F1F0FF; border-radius: 15px; padding: 10px;
        text-align: center; min-width: 80px;
    }
    .stat-label { color: #A0A0A0; font-size: 11px; font-weight: 600; }
    .stat-val { color: #6C5CE7; font-weight: bold; font-size: 16px; }

    /* Buttons */
    .stButton>button {
        background: #6C5CE7; color: white !important;
        border-radius: 18px; padding: 12px; border: none;
        width: 100%; font-weight: 600; transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(108, 92, 231, 0.3); }
    
    /* Purple Banner */
    .purple-banner {
        background: #6C5CE7; color: white; padding: 20px;
        border-radius: 25px; margin: 15px 0;
    }
    
    /* Custom Progress Bar Color */
    .stProgress > div > div > div > div { background-color: #6C5CE7 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🚀 CORE LOGIC
# ==========================================
txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)
xp_in_level = txp % 100

# Navigation
with st.sidebar:
    st.markdown("<h1 style='color:#6C5CE7;'>MENU</h1>", unsafe_allow_html=True)
    menu = st.radio("Missions", ["🏠 Dashboard", "🎓 Training", "⚔️ Battle", "🛒 Shop", "🏆 Hall of Fame"])

if menu == "🏠 Dashboard":
    # 1. Profile Header
    st.markdown(f"""
        <div class="profile-card">
            <h4 style="color:#A0A0A0; letter-spacing: 2px;">PROFILE</h4>
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user}" width="110" style="margin: 10px 0;">
            <h2 style="margin:0;">{st.session_state.user}</h2>
            <div style="display: flex; justify-content: center; gap: 20px; margin-top: 15px;">
                <div class="stat-box"><div class="stat-label">EXP</div><div class="stat-val">{txp}</div></div>
                <div class="stat-box"><div class="stat-label">LEVEL</div><div class="stat-val">{user_level}</div></div>
                <div class="stat-box"><div class="stat-label">STREAK</div><div class="stat-val">🔥 5</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Daily Gift Section
    today = str(date.today())
    c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
    is_claimed = c.fetchone()
    
    if not is_claimed:
        st.markdown("""<div class="purple-banner">🎁 <b>Daily Reward Ready!</b><br><small>Claim your 50 XP bonus today.</small></div>""", unsafe_allow_html=True)
        if st.button("CLAIM GIFT"):
            c.execute("INSERT INTO daily_tasks VALUES (?, ?, ?)", (st.session_state.email, today, 1))
            c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, today, 50))
            conn.commit(); st.balloons(); st.rerun()
    
    # 3. Progress
    st.write("#### NEXT LEVEL PROGRESS")
    st.progress(max(0.0, min(xp_in_level / 100.0, 1.0)))
    st.caption(f"{100 - xp_in_level} XP left for Level {user_level + 1}")

elif menu == "🎓 Training":
    st.markdown("<h2 style='color:#6C5CE7;'>🎯 Practice Mode</h2>", unsafe_allow_html=True)
    if 't_q' not in st.session_state: st.session_state.t_q = random.choice(TRAINING_DATA)
    q = st.session_state.t_q
    
    st.markdown(f"""<div style="background:white; padding:30px; border-radius:25px; border:2px solid #E0DDF5; text-align:center; margin-bottom:20px;">
        <h3>{q['q']}</h3></div>""", unsafe_allow_html=True)
    
    for opt in q['o']:
        if st.button(opt):
            if opt == q['a']:
                st.success("Correct Answer!")
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 10))
                conn.commit(); time.sleep(1); del st.session_state.t_q; st.rerun()
            else: st.error("Oops! Try again.")

elif menu == "⚔️ Battle":
    st.markdown("<h2 style='color:#FF7675;'>👹 MONSTER ARENA</h2>", unsafe_allow_html=True)
    boss_max = 100 + (user_level * 25)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("🛡️ HERO HP")
        st.progress(max(0.0, min(st.session_state.player_hp / 100.0, 1.0)))
    with col2:
        st.write("👾 BOSS HP")
        st.progress(max(0.0, min(st.session_state.boss_hp / boss_max, 1.0)))

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("BOSS DEFEATED!")
        if st.button("FIND NEW ENEMY"): st.session_state.boss_hp = 120; st.session_state.player_hp = 100; st.rerun()
    else:
        st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=180)
        if st.button("🔥 MAGIC ATTACK"):
            st.session_state.boss_hp -= 30; st.rerun()

elif menu == "🛒 Shop":
    st.markdown("<h2 style='color:#6C5CE7;'>🛒 ITEM SHOP</h2>", unsafe_allow_html=True)
    st.write(f"Credits: **{txp} XP**")
    
    shop_col1, shop_col2 = st.columns(2)
    with shop_col1:
        st.markdown("""<div class='profile-card'>🛡️<br><b>Shield</b><br>50 XP</div>""", unsafe_allow_html=True)
        if st.button("BUY SHIELD"):
            if txp >= 50:
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, today, -50))
                c.execute("INSERT INTO inventory VALUES (?, 'Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1", (st.session_state.email,))
                conn.commit(); st.success("Bought!"); st.rerun()
            else: st.error("No XP!")

elif menu == "🏆 Hall of Fame":
    st.markdown("<h2 style='color:#6C5CE7; text-align:center;'>🏆 TOP GURUS</h2>", unsafe_allow_html=True)
    data = c.execute("SELECT username, SUM(xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC LIMIT 5").fetchall()
    for i, row in enumerate(data, 1):
        st.markdown(f"""<div style="background:white; padding:15px; border-radius:20px; margin-bottom:10px; display:flex; justify-content:space-between; border-left: 5px solid #6C5CE7;">
            <span>#{i} <b>{row[0]}</b></span><span style="color:#6C5CE7;">{row[1]} XP</span></div>""", unsafe_allow_html=True)
