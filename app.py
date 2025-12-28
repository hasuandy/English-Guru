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

# --- Assets ---
CORRECT_SND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WRONG_SND = "https://www.soundjay.com/buttons/sounds/button-10.mp3"
BOSS_GIF = "https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif"

# --- Functions ---
def trigger_effects(effect_type):
    if effect_type == "correct":
        st.markdown(f'<audio src="{CORRECT_SND}" autoplay></audio>', unsafe_allow_html=True)
    elif effect_type == "wrong":
        st.markdown(f'<audio src="{WRONG_SND}" autoplay></audio>', unsafe_allow_html=True)
        # Screen Shake Animation
        st.markdown("<script>window.parent.document.querySelector('.stApp').animate([{transform:'translate(2px,2px)'},{transform:'translate(-2px,-2px)'}],{duration:100,iterations:3});</script>", unsafe_allow_html=True)

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Hero_Player", "player@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# --- UI Config ---
st.set_page_config(page_title="English Guru Pro", page_icon="⚔️", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp { background: #0e1117; color: white; }
    .boss-box { background: rgba(255,0,0,0.1); padding: 20px; border-radius: 20px; border: 2px solid red; text-align: center; }
    .stat-card { background: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🚀 MAIN APP
# ==========================================
page = st.sidebar.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🏆 Hall of Fame"])

if page == "🏠 Dashboard":
    st.markdown("<h1 style='font-family:Bungee;'>🛡️ COMMAND CENTER</h1>", unsafe_allow_html=True)
    txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,)).fetchone()[0] or 0)
    col1, col2 = st.columns(2)
    with col1: st.markdown(f"<div class='stat-card'><h3>XP: {txp}</h3></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='stat-card'><h3>LEVEL: {1+(txp//100)}</h3></div>", unsafe_allow_html=True)
    st.info("📢 Click anywhere on the screen first to enable sounds! 🔊")

elif page == "🎓 Training":
    st.title("🎓 Practice Mode")
    q = {"q": "Opposite of 'FAST'?", "o": ["Quick", "Slow", "High", "Happy"], "a": "Slow"}
    st.subheader(q['q'])
    for opt in q['o']:
        if st.button(f"✨ {opt}", use_container_width=True):
            if opt == q['a']:
                trigger_effects("correct"); st.success("Sahi Jawab!")
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 10))
                conn.commit()
            else:
                trigger_effects("wrong"); st.error("Galat Jawab!")
            time.sleep(1); st.rerun()

elif page == "⚔️ Boss Battle":
    st.markdown("<h1 style='color:red; font-family:Bungee; text-align:center;'>👹 MONSTER ARENA</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2: st.image(BOSS_GIF, use_container_width=True)
    
    hp1, hp2 = st.columns(2)
    hp1.metric("YOUR HP", f"{st.session_state.player_hp}%")
    hp2.metric("BOSS HP", f"{st.session_state.boss_hp}%")

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("VICTORY!"); st.button("Spawn New Boss", on_click=lambda: setattr(st.session_state, 'boss_hp', 100))
    elif st.session_state.player_hp <= 0:
        st.error("DEFEATED!"); st.button("Revive", on_click=lambda: setattr(st.session_state, 'player_hp', 100))
    else:
        st.markdown("<div class='boss-box'><h3>Synonym of 'SMART'?</h3></div>", unsafe_allow_html=True)
        ans = st.radio("Weapon:", ["Dull", "Intelligent", "Lazy", "Angry"], horizontal=True)
        if st.button("🔥 ATTACK"):
            if ans == "Intelligent":
                st.session_state.boss_hp -= 25; trigger_effects("correct")
            else:
                st.session_state.player_hp -= 20; trigger_effects("wrong")
            time.sleep(1); st.rerun()

elif page == "🏆 Hall of Fame":
    st.title("🏆 Leaderboard")
    data = c.execute("SELECT username, SUM(xp) as s FROM progress p JOIN users u ON p.email=u.email GROUP BY u.email ORDER BY s DESC").fetchall()
    for row in data:
        av = f"https://api.dicebear.com/7.x/avataaars/svg?seed={row[0]}"
        st.markdown(f"<img src='{av}' width='40'> **{row[0]}** — {row[1]} XP", unsafe_allow_html=True)
        
