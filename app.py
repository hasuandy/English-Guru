import streamlit as st
import sqlite3
from datetime import date
import random
import time

# ==========================================
# 🛠️ DATABASE SETUP (FIXED)
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
# 📚 MEGA QUESTION BANK (READY TO USE)
# ==========================================
if 'questions' not in st.session_state:
    st.session_state.questions = [
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
        {"q": "Past tense of 'GO'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
        {"q": "Meaning of 'ENORMOUS'?", "o": ["Tiny", "Huge", "Weak", "Soft"], "a": "Huge"},
        {"q": "Antonym of 'STRONG'?", "o": ["Hard", "Weak", "Tough", "Brave"], "a": "Weak"},
        {"q": "Synonym of 'BEAUTIFUL'?", "o": ["Ugly", "Pretty", "Plain", "Rough"], "a": "Pretty"},
        {"q": "A person who treats teeth?", "o": ["Doctor", "Dentist", "Teacher", "Engineer"], "a": "Dentist"},
        {"q": "Opposite of 'ALWAYS'?", "o": ["Never", "Sometimes", "Daily", "Often"], "a": "Never"},
        {"q": "Plural of 'FOOT'?", "o": ["Foots", "Feets", "Feet", "Footes"], "a": "Feet"},
        {"q": "She ____ a book now.", "o": ["read", "reads", "is reading", "reading"], "a": "is reading"},
        {"q": "Meaning of 'VALUABLE'?", "o": ["Cheap", "Priceless", "Useless", "Trash"], "a": "Priceless"},
        {"q": "Spelling check:", "o": ["Necessary", "Necesary", "Neccessary", "Nesesary"], "a": "Necessary"},
        {"q": "Synonym of 'ANGRY'?", "o": ["Happy", "Mad", "Sad", "Calm"], "a": "Mad"}
    ]

# ==========================================
# 🎨 GAMER CSS (NEON THEME)
# ==========================================
st.set_page_config(page_title="GURU AI PRO", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background-color: #0b0e14; color: white; font-family: 'Rajdhani', sans-serif; }
    .neon-text { color: #00f2ff; font-family: 'Bungee'; text-shadow: 0 0 15px #00f2ff; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 25px; border-top: 4px solid #00f2ff; text-align: center; margin-bottom: 15px; }
    .stat-val { font-family: 'Bungee'; font-size: 30px; color: #00f2ff; }
    .stButton>button { background: transparent !important; color: #00f2ff !important; border: 2px solid #00f2ff !important; border-radius: 8px; font-family: 'Bungee' !important; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background: #00f2ff !important; color: #0b0e14 !important; box-shadow: 0 0 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- Session Control ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "STEVNATION", "player@guru.ai"

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h2 class='neon-text'>GURU AI</h2>", unsafe_allow_html=True)
    menu = st.radio("MENU", ["🖥️ Dashboard", "🎯 Training", "⚔️ Boss Battle"])

# Fetch Data
txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)

# ==========================================
# 🎯 TRAINING (FIXED QUESTION ADDING)
# ==========================================
if menu == "🎯 Training":
    st.markdown("<h1 class='neon-text'>TRAINING ZONE</h1>", unsafe_allow_html=True)
    
    # Randomly pick a question if not already in session
    if 'curr_q' not in st.session_state:
        st.session_state.curr_q = random.choice(st.session_state.questions)
    
    q = st.session_state.curr_q
    st.markdown(f"<div class='card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, opt in enumerate(q['o']):
        with cols[i%2]:
            if st.button(opt, key=f"q_btn_{i}"):
                if opt == q['a']:
                    st.toast("⚡ CORRECT! +10 XP")
                    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 10))
                    conn.commit()
                    time.sleep(0.5)
                    # Force naya question
                    st.session_state.curr_q = random.choice(st.session_state.questions)
                    st.rerun()
                else:
                    st.error("MISSION FAILED! Try Again.")

elif menu == "🖥️ Dashboard":
    st.markdown("<h1 class='neon-text'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><small>TOTAL XP</small><div class='stat-val'>{txp}</div></div>", unsafe_allow_html=True)
    st.write("### ⚡ LEVEL PROGRESS")
    st.progress((txp % 100) / 100)

elif menu == "⚔️ Boss Battle":
    st.markdown("<h1 class='neon-text' style='text-align:center;'>BOSS ARENA</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h2>Answer questions to defeat the Dragon!</h2></div>", unsafe_allow_html=True)
    # Similar logic for Battle...
