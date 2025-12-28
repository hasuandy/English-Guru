import streamlit as st
import sqlite3
from datetime import date
import random
import time

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

# --- Sound URLs ---
CORRECT_SND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WRONG_SND = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

# --- Animation & Sound Logic ---
def trigger_effects(effect_type):
    if effect_type == "correct":
        st.markdown(f'<audio src="{CORRECT_SND}" autoplay></audio>', unsafe_allow_html=True)
    elif effect_type == "wrong":
        st.markdown(f'<audio src="{WRONG_SND}" autoplay></audio>', unsafe_allow_html=True)
        # Screen Shake CSS
        st.markdown("""
            <script>
            window.parent.document.querySelector('.stApp').animate([
                { transform: 'translate(1px, 1px) rotate(0deg)' },
                { transform: 'translate(-1px, -2px) rotate(-1deg)' },
                { transform: 'translate(-3px, 0px) rotate(1deg)' },
                { transform: 'translate(3px, 2px) rotate(0deg)' },
                { transform: 'translate(1px, -1px) rotate(1deg)' },
                { transform: 'translate(-1px, 2px) rotate(-1deg)' },
                { transform: 'translate(-3px, 1px) rotate(0deg)' }
            ], { duration: 100 });
            </script>
            """, unsafe_allow_html=True)

# --- Data ---
TRAINING_DATA = [{"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"}]
BOSS_POOL = [{"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"}]

# --- Session State ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

# --- UI CONFIG ---
st.set_page_config(page_title="English Guru Pro", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp { background: #0e1117; color: white; }
    .boss-card { background: linear-gradient(45deg, #4b0082, #000000); padding: 20px; border-radius: 15px; border: 2px solid red; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- APP PAGES ---
if st.session_state.logged_in:
    page = st.sidebar.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle"])

    if page == "🏠 Dashboard":
        st.title("Welcome Hero!")
        st.write("Click anywhere to enable sounds for this session! 🔊")

    elif page == "🎓 Training":
        st.title("Quick Practice")
        tq = TRAINING_DATA[0]
        st.subheader(tq['q'])
        for opt in tq['o']:
            if st.button(opt):
                if opt == tq['a']:
                    trigger_effects("correct")
                    st.success("Correct!")
                else:
                    trigger_effects("wrong")
                    st.error("Wrong!")
                time.sleep(1)
                st.rerun()

    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:red; font-family:Bungee;'>⚔️ BOSS FIGHT</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.metric("HERO HP", f"{st.session_state.player_hp}%")
        col2.metric("BOSS HP", f"{st.session_state.boss_hp}%")

        if st.session_state.boss_hp <= 0:
            st.balloons()
            st.success("YOU WON!")
            if st.button("Reset"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
        else:
            bq = BOSS_POOL[0]
            st.markdown(f"<div class='boss-card'><h2>{bq['q']}</h2></div>", unsafe_allow_html=True)
            ans = st.radio("Choose Weapon:", bq['o'])
            
            if st.button("💥 ATTACK BOSS"):
                if ans == bq['a']:
                    st.session_state.boss_hp -= 25
                    trigger_effects("correct")
                    st.toast("CRITICAL HIT!")
                else:
                    st.session_state.player_hp -= 20
                    trigger_effects("wrong") # Isme screen shake effect chalega
                    st.toast("BOSS ATTACKED YOU!")
                time.sleep(1)
                st.rerun()
