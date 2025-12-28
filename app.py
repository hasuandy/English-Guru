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
    c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
    conn.commit()

init_db()

# --- Assets & Data ---
CORRECT_SND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WRONG_SND = "https://www.soundjay.com/buttons/sounds/button-10.mp3"
BOSS_GIF = "https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif"

TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "I ____ a student.", "o": ["is", "am", "are", "be"], "a": "am"}
]

# --- Functions ---
def trigger_effects(effect_type):
    if effect_type == "correct":
        st.markdown(f'<audio src="{CORRECT_SND}" autoplay></audio>', unsafe_allow_html=True)
    elif effect_type == "wrong":
        st.markdown(f'<audio src="{WRONG_SND}" autoplay></audio>', unsafe_allow_html=True)
        st.markdown("<script>window.parent.document.querySelector('.stApp').animate([{transform:'translate(2px,2px)'},{transform:'translate(-2px,-2px)'}],{duration:100,iterations:3});</script>", unsafe_allow_html=True)

# --- Session State ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Hero_Player", "player@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# --- User Stats ---
txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)

# --- UI Layout ---
st.set_page_config(page_title="English Guru Pro v37", page_icon="🎓", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp {{ background: #0e1117; color: white; }}
    .main-card {{ background: #1e2130; padding: 25px; border-radius: 20px; border: 1px solid #333; }}
    .boss-box {{ background: rgba(255,0,0,0.1); padding: 20px; border-radius: 20px; border: 2px solid red; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🚀 APP NAVIGATION
# ==========================================
page = st.sidebar.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🏆 Leaderboard"])

if page == "🏠 Dashboard":
    st.markdown("<h1 style='font-family:Bungee;'>🛡️ COMMAND CENTER</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("CURRENT LEVEL", user_level)
    c2.metric("TOTAL XP", txp)
    st.info("📢 Pro Tip: Awaaz ke liye pehle screen par kahin click karein! 🔊")

elif page == "🎓 Training":
    st.title("🎓 Daily Practice")
    if 't_q' not in st.session_state: st.session_state.t_q = random.choice(TRAINING_DATA)
    q = st.session_state.t_q
    
    st.markdown(f"<div class='main-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
    for opt in q['o']:
        if st.button(opt, use_container_width=True):
            if opt == q['a']:
                trigger_effects("correct"); st.success("Sahi Jawab! +10 XP")
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 10))
                conn.commit()
            else:
                trigger_effects("wrong"); st.error("Galat Jawab!")
            del st.session_state.t_q; time.sleep(1); st.rerun()

elif page == "⚔️ Boss Battle":
    st.markdown("<h1 style='color:red; font-family:Bungee; text-align:center;'>👹 BOSS FIGHT</h1>", unsafe_allow_html=True)
    
    # Boss Config
    boss_max_hp = 100 + (user_level * 25)
    
    # Safe Progress Bar Calculation (Error Fix)
    p_val = max(0.0, min(st.session_state.player_hp / 100.0, 1.0))
    b_val = max(0.0, min(st.session_state.boss_hp / boss_max_hp, 1.0))
    
    col_hp1, col_hp2 = st.columns(2)
    col_hp1.write(f"🛡️ HERO: {int(p_val*100)}%")
    col_hp1.progress(p_val)
    col_hp2.write(f"👾 BOSS: {int(b_val*100)}%")
    col_hp2.progress(b_val)

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("VICTORY! Boss tabah ho gaya!")
        if st.button("Agla Boss Bulao ⚔️"):
            st.session_state.boss_hp = boss_max_hp + 50
            st.session_state.player_hp = 100
            st.rerun()
    elif st.session_state.player_hp <= 0:
        st.error("Khatam... Tata... Bye Bye... (You Died)")
        if st.button("Zinda Ho Jao (Revive)"):
            st.session_state.player_hp = 100; st.rerun()
    else:
        st.image(BOSS_GIF, width=250)
        st.markdown("<div class='boss-box'><h3>Sahi jawab do attack karne ke liye!</h3></div>", unsafe_allow_html=True)
        
        # Battle Question
        q = TRAINING_DATA[0] # Training data se hi utha raha hoon simple rakhne ke liye
        ans = st.radio("Choose Answer:", q['o'], horizontal=True)
        
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("🗡️ Normal Attack"):
                if ans == q['a']:
                    st.session_state.boss_hp -= 25; trigger_effects("correct")
                else:
                    st.session_state.player_hp -= 15; trigger_effects("wrong")
                st.rerun()
        with btn2:
            if user_level >= 2:
                if st.button("🔥 Super Attack"):
                    if ans == q['a']:
                        st.session_state.boss_hp -= 50; trigger_effects("correct")
                    else:
                        st.session_state.player_hp -= 30; trigger_effects("wrong")
                    st.rerun()
            else:
                st.button("🔒 Lvl 2 Required", disabled=True)

elif page == "🏆 Leaderboard":
    st.markdown("<h1 style='font-family:Bungee;'>🏆 TOP HEROES</h1>", unsafe_allow_html=True)
    data = c.execute("SELECT username, SUM(xp) as s FROM progress p JOIN users u ON p.email=u.email GROUP BY u.email ORDER BY s DESC").fetchall()
    for i, row in enumerate(data, 1):
        av = f"https://api.dicebear.com/7.x/avataaars/svg?seed={row[0]}"
        st.markdown(f"**#{i}** <img src='{av}' width='30'> {row[0]} — {row[1]} XP", unsafe_allow_html=True)
