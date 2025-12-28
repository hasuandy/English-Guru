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

# --- Data Pool ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"}
]

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Hazel", "hazel@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# ==========================================
# 🎨 DESIGN (CSS) - IMAGE THEME BASED
# ==========================================
st.set_page_config(page_title="English Guru Pro", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    
    /* Main Background */
    .stApp { background-color: #F3F1FB; font-family: 'Poppins', sans-serif; }
    
    /* Profile Card */
    .profile-card {
        background: white; padding: 30px; border-radius: 30px;
        text-align: center; box-shadow: 0px 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Stats Bar */
    .stat-row { display: flex; justify-content: space-around; margin: 20px 0; }
    .stat-item { color: #8E8E8E; font-size: 14px; }
    .stat-val { color: #6C5CE7; font-weight: bold; font-size: 18px; }

    /* Buttons */
    .stButton>button {
        background: #6C5CE7; color: white !important;
        border-radius: 20px; padding: 10px 25px; border: none;
        width: 100%; font-weight: 600;
    }
    
    /* Certificate Card */
    .cert-card {
        background: #6C5CE7; color: white; padding: 20px;
        border-radius: 25px; display: flex; align-items: center;
    }
    
    /* Question Box */
    .q-box {
        background: white; padding: 25px; border-radius: 25px;
        border: 2px solid #E0E0E0; text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🚀 APP LOGIC
# ==========================================
txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)

# Navigation
menu = st.sidebar.selectbox("Go to", ["Profile", "Training", "Battle", "Hall of Fame"])

if menu == "Profile":
    # User Profile Section (Design ki tarah)
    st.markdown(f"""
        <div class="profile-card">
            <h2 style="color:#2D3436; margin-bottom:5px;">PROFILE</h2>
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user}" width="120" style="margin: 15px 0;">
            <h3 style="color:#2D3436;">{st.session_state.user}</h3>
            <div class="stat-row">
                <div class="stat-item">EXP<br><span class="stat-val">{txp}</span></div>
                <div class="stat-item">LEVEL<br><span class="stat-val">{user_level}</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### MY BADGES")
    cols = st.columns(4)
    badges = ["📚", "🏆", "❔", "❔"]
    for i, b in enumerate(badges):
        cols[i].markdown(f"<div style='background:white; padding:15px; border-radius:15px; text-align:center; font-size:24px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);'>{b}</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown(f"""
        <div class="cert-card">
            <div style="font-size:40px; margin-right:20px;">📜</div>
            <div>
                <b style="font-size:18px;">Lingo Star</b><br>
                <small>{txp}/500 XP to next certificate</small>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif menu == "Training":
    st.markdown("<h2 style='text-align:center; color:#6C5CE7;'>🎓 TRAINING</h2>", unsafe_allow_html=True)
    if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAINING_DATA)
    tq = st.session_state.current_tq
    
    st.markdown(f"<div class='q-box'><h3>{tq['q']}</h3></div>", unsafe_allow_html=True)
    
    for opt in tq['o']:
        if st.button(opt):
            if opt == tq['a']:
                st.success("Correct!")
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 10))
                conn.commit()
                time.sleep(1); del st.session_state.current_tq; st.rerun()
            else:
                st.error("Try Again!")

elif menu == "Battle":
    st.markdown("<h2 style='text-align:center; color:#FF7675;'>⚔️ BOSS BATTLE</h2>", unsafe_allow_html=True)
    # Safe progress calc
    boss_max = 100 + (user_level * 25)
    p_val = max(0.0, min(st.session_state.player_hp / 100.0, 1.0))
    b_val = max(0.0, min(st.session_state.boss_hp / boss_max, 1.0))
    
    st.write("Hero HP")
    st.progress(p_val)
    st.write("Boss HP")
    st.progress(b_val)
    
    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("VICTORY!")
        if st.button("New Boss"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
    else:
        st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=200)
        if st.button("Attack! (-20 Boss HP)"):
            st.session_state.boss_hp -= 20; st.rerun()

elif menu == "Hall of Fame":
    st.markdown("<h2 style='text-align:center; color:#6C5CE7;'>🏆 TOP GURUS</h2>", unsafe_allow_html=True)
    data = c.execute("SELECT username, SUM(xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC LIMIT 5").fetchall()
    for row in data:
        st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:20px; margin-bottom:10px; display:flex; justify-content:space-between;">
                <b>{row[0]}</b>
                <span style="color:#6C5CE7; font-weight:bold;">{row[1]} XP</span>
            </div>
        """, unsafe_allow_html=True)
