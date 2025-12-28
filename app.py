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
    c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
    conn.commit()
init_db()

# ==========================================
# 📚 QUESTION BANK (50+ QUESTIONS)
# ==========================================
BIG_QUESTION_POOL = [
    {"q": "Meaning of 'ABANDON'?", "o": ["To start", "To leave", "To keep", "To find"], "a": "To leave"},
    {"q": "Meaning of 'GENEROUS'?", "o": ["Selfish", "Kind", "Poor", "Angry"], "a": "Kind"},
    {"q": "Meaning of 'PRECISE'?", "o": ["Vague", "Exact", "Wrong", "Long"], "a": "Exact"},
    {"q": "Meaning of 'RELUCTANT'?", "o": ["Willing", "Unwilling", "Happy", "Eager"], "a": "Unwilling"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Steady", "Heavy"], "a": "Quick"},
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Classic", "Stone"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eated", "Ate", "Eating", "Eats"], "a": "Ate"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"},
    {"q": "Correct spelling?", "o": ["Receive", "Recieve", "Receve", "Riceive"], "a": "Receive"},
    {"q": "I ____ to school every day.", "o": ["go", "goes", "going", "gone"], "a": "go"},
    {"q": "Antonym of 'STRONG'?", "o": ["Hard", "Weak", "Tough", "Brave"], "a": "Weak"},
    {"q": "Past tense of 'GO'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"}
]

# ==========================================
# 🎨 GAMER CSS
# ==========================================
st.set_page_config(page_title="GURU AI PRO", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background-color: #0b0e14; color: white; font-family: 'Rajdhani', sans-serif; }
    .neon-text { color: #00f2ff; font-family: 'Bungee'; text-shadow: 0 0 15px #00f2ff; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; border-top: 4px solid #00f2ff; text-align: center; margin-bottom: 10px; }
    .stat-val { font-family: 'Bungee'; font-size: 30px; color: #00f2ff; }
    .stButton>button { background: transparent !important; color: #00f2ff !important; border: 2px solid #00f2ff !important; border-radius: 8px !important; font-family: 'Bungee' !important; width: 100%; }
    .stButton>button:hover { background: #00f2ff !important; color: #0b0e14 !important; box-shadow: 0 0 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "STEVNATION", "player@guru.ai"

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)

with st.sidebar:
    st.markdown("<h2 class='neon-text'>GURU AI</h2>", unsafe_allow_html=True)
    st.image(f"https://api.dicebear.com/7.x/pixel-art/svg?seed={st.session_state.user}", width=80)
    menu = st.radio("MENU", ["🖥️ Dashboard", "🎯 Training", "⚔️ Boss Battle"])

# ==========================================
# 🖥️ DASHBOARD & 🎯 TRAINING (Same as before)
# ==========================================
if menu == "🖥️ Dashboard":
    st.markdown("<h1 class='neon-text'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><small>TOTAL XP</small><div class='stat-val'>{txp}</div></div>", unsafe_allow_html=True)
    st.progress((txp % 100) / 100)

elif menu == "🎯 Training":
    st.markdown("<h1 class='neon-text'>TRAINING ZONE</h1>", unsafe_allow_html=True)
    if 'current_q' not in st.session_state: st.session_state.current_q = random.choice(BIG_QUESTION_POOL)
    q = st.session_state.current_q
    st.markdown(f"<div class='card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, opt in enumerate(q['o']):
        with cols[i%2]:
            if st.button(opt, key=f"t_{i}"):
                if opt == q['a']:
                    st.toast("CORRECT!"); c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 10))
                    conn.commit(); time.sleep(0.5); del st.session_state.current_q; st.rerun()

# ==========================================
# ⚔️ BOSS BATTLE (FIXED WITH IMAGE)
# ==========================================
elif menu == "⚔️ Boss Battle":
    st.markdown("<h1 class='neon-text' style='text-align:center;'>BOSS ARENA</h1>", unsafe_allow_html=True)
    
    # HP Bars
    col_p, col_mid, col_b = st.columns([2, 1, 2])
    col_p.markdown(f"<div class='card' style='border-top-color:#ff4b4b;'><b>HERO</b><div class='stat-val'>{st.session_state.player_hp}%</div></div>", unsafe_allow_html=True)
    col_mid.markdown("<h1 style='text-align:center; font-size:60px;'>⚔️</h1>", unsafe_allow_html=True)
    col_b.markdown(f"<div class='card'><b>BOSS</b><div class='stat-val'>{st.session_state.boss_hp}%</div></div>", unsafe_allow_html=True)

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("VICTORY!"); st.button("NEXT BOSS", on_click=lambda: setattr(st.session_state, 'boss_hp', 100))
    elif st.session_state.player_hp <= 0:
        st.error("YOU DIED!"); st.button("RESPAWN", on_click=lambda: setattr(st.session_state, 'player_hp', 100))
    else:
        # --- YE RAHA IMAGE WALA PART ---
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        # Aap yahan koi bhi GIF ya Image link dal sakte hain
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJmZzZ4eXN6ZzZ4eXN6ZzZ4eXN6ZzZ4eXN6ZzZ4eXN6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxxXLyKHzvW/giphy.gif", width=300)
        st.markdown("</div>", unsafe_allow_html=True)

        # Question below image
        if 'bq' not in st.session_state: st.session_state.bq = random.choice(BIG_QUESTION_POOL)
        bq = st.session_state.bq
        
        st.markdown(f"<div class='card'><h3>{bq['q']}</h3></div>", unsafe_allow_html=True)
        
        ans = st.radio("CHOOSE YOUR ATTACK:", bq['o'], horizontal=True)
        if st.button("🔥 CAST SPELL"):
            if ans == bq['a']:
                st.session_state.boss_hp -= 25
                st.toast("HIT! -25 HP", icon="💥")
            else:
                st.session_state.player_hp -= 20
                st.toast("MISSED! BOSS ATTACKED YOU", icon="🛑")
            del st.session_state.bq
            st.rerun()
