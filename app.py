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
    {"q": "Meaning of 'VIBRANT'?", "o": ["Dull", "Energetic", "Slow", "Pale"], "a": "Energetic"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Steady", "Heavy"], "a": "Quick"},
    {"q": "Synonym of 'LARGE'?", "o": ["Tiny", "Huge", "Soft", "Thin"], "a": "Huge"},
    {"q": "Synonym of 'BRAVE'?", "o": ["Afraid", "Fearless", "Quiet", "Weak"], "a": "Fearless"},
    {"q": "Synonym of 'HAPPY'?", "o": ["Sad", "Joyful", "Angry", "Bored"], "a": "Joyful"},
    {"q": "Synonym of 'SMART'?", "o": ["Dull", "Intelligent", "Stupid", "Lazy"], "a": "Intelligent"},
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Classic", "Stone"], "a": "Modern"},
    {"q": "Antonym of 'BRIGHT'?", "o": ["Shining", "Dim", "Light", "Clear"], "a": "Dim"},
    {"q": "Antonym of 'VICTORY'?", "o": ["Win", "Defeat", "Success", "Gain"], "a": "Defeat"},
    {"q": "Past tense of 'EAT'?", "o": ["Eated", "Ate", "Eating", "Eats"], "a": "Ate"},
    {"q": "Past tense of 'BUY'?", "o": ["Buyed", "Bought", "Buying", "Brought"], "a": "Bought"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"},
    {"q": "Plural of 'MOUSE'?", "o": ["Mouses", "Mice", "Micey", "Mices"], "a": "Mice"},
    {"q": "Correct spelling?", "o": ["Receive", "Recieve", "Receve", "Riceive"], "a": "Receive"},
    {"q": "Correct spelling?", "o": ["Bussiness", "Business", "Busyness", "Bisness"], "a": "Business"},
    {"q": "I ____ to school every day.", "o": ["go", "goes", "going", "gone"], "a": "go"},
    {"q": "She ____ a beautiful song.", "o": ["sing", "sings", "singing", "sung"], "a": "sings"},
    {"q": "'Piece of cake' means?", "o": ["Very easy", "Very sweet", "Hard work", "Small slice"], "a": "Very easy"},
    {"q": "Antonym of 'STRONG'?", "o": ["Hard", "Weak", "Tough", "Brave"], "a": "Weak"},
    {"q": "Synonym of 'BEAUTIFUL'?", "o": ["Ugly", "Pretty", "Plain", "Rough"], "a": "Pretty"},
    {"q": "Past tense of 'GO'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"}
    # ... (Aap isi format mein aur add kar sakte hain)
]

# ==========================================
# 🎨 GAMER CSS (CYAN NEON THEME)
# ==========================================
st.set_page_config(page_title="GURU AI PRO", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background-color: #0b0e14; color: white; font-family: 'Rajdhani', sans-serif; }
    .neon-text { color: #00f2ff; font-family: 'Bungee'; text-shadow: 0 0 15px #00f2ff; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; border-top: 4px solid #00f2ff; text-align: center; }
    .stat-val { font-family: 'Bungee'; font-size: 30px; color: #00f2ff; }
    .stButton>button { background: transparent !important; color: #00f2ff !important; border: 2px solid #00f2ff !important; border-radius: 8px !important; font-family: 'Bungee' !important; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background: #00f2ff !important; color: #0b0e14 !important; box-shadow: 0 0 20px #00f2ff; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- Session Management ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "STEVNATION", "player@guru.ai"

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)
xp_in_level = txp % 100

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 class='neon-text'>GURU AI</h2>", unsafe_allow_html=True)
    st.image(f"https://api.dicebear.com/7.x/pixel-art/svg?seed={st.session_state.user}", width=80)
    st.write(f"USER: **{st.session_state.user}**")
    st.write(f"LEVEL: **{user_level}**")
    st.divider()
    menu = st.radio("MENU", ["🖥️ Dashboard", "🎯 Training", "⚔️ Boss Battle"])

# ==========================================
# 🖥️ DASHBOARD
# ==========================================
if menu == "🖥️ Dashboard":
    st.markdown("<h1 class='neon-text'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='card'><small>LEVEL</small><div class='stat-val'>{user_level}</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card'><small>TOTAL XP</small><div class='stat-val'>{txp}</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='card' style='border-top-color:#ff4b4b;'><small>STREAK</small><div class='stat-val'>🔥 5</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='card' style='border-top-color:#7000ff;'><small>RANK</small><div class='stat-val'>PRO</div></div>", unsafe_allow_html=True)

    st.write("### ⚡ Current Progress")
    st.progress(xp_in_level / 100)
    
    col_gift, col_empty = st.columns([1, 2])
    with col_gift:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("🎁 **Daily Gift**")
        if st.button("CLAIM 50 XP"):
            c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 50))
            conn.commit(); st.balloons(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🎯 TRAINING (RANDOM QUESTIONS)
# ==========================================
elif menu == "🎯 Training":
    st.markdown("<h1 class='neon-text'>TRAINING ZONE</h1>", unsafe_allow_html=True)
    if 'current_q' not in st.session_state:
        st.session_state.current_q = random.choice(BIG_QUESTION_POOL)
    
    q = st.session_state.current_q
    st.markdown(f"<div class='card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
    
    st.write("")
    cols = st.columns(2)
    for i, opt in enumerate(q['o']):
        with cols[i%2]:
            if st.button(opt, key=f"t_{i}"):
                if opt == q['a']:
                    st.toast("CORRECT! +10 XP", icon="✅")
                    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 10))
                    conn.commit(); time.sleep(0.5); del st.session_state.current_q; st.rerun()
                else:
                    st.error("WRONG! TRY AGAIN")

# ==========================================
# ⚔️ BOSS BATTLE
# ==========================================
elif menu == "⚔️ Boss Battle":
    st.markdown("<h1 class='neon-text' style='text-align:center;'>BOSS ARENA</h1>", unsafe_allow_html=True)
    
    col_p, col_mid, col_b = st.columns([2, 1, 2])
    col_p.markdown(f"<div class='card' style='border-top-color:#ff4b4b;'><b>HERO</b><div class='stat-val'>{st.session_state.player_hp}%</div></div>", unsafe_allow_html=True)
    col_mid.markdown("<h1 style='text-align:center; font-size:60px;'>⚔️</h1>", unsafe_allow_html=True)
    col_b.markdown(f"<div class='card'><b>BOSS</b><div class='stat-val'>{st.session_state.boss_hp}%</div></div>", unsafe_allow_html=True)

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("BOSS DEFEATED!"); st.button("SPAWN NEXT BOSS", on_click=lambda: setattr(st.session_state, 'boss_hp', 100))
    else:
        if 'bq' not in st.session_state: st.session_state.bq = random.choice(BIG_QUESTION_POOL)
        bq = st.session_state.bq
        st.markdown(f"<div class='card'><h3>{bq['q']}</h3></div>", unsafe_allow_html=True)
        
        ans = st.radio("Select Attack:", bq['o'], horizontal=True)
        if st.button("🔥 EXECUTE ATTACK"):
            if ans == bq['a']:
                st.session_state.boss_hp -= 25; st.toast("DIRECT HIT!")
            else:
                st.session_state.player_hp -= 20; st.toast("BOSS COUNTERED!")
            del st.session_state.bq; st.rerun()
