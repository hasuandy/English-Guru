import streamlit as st
import sqlite3
from datetime import date
import random
import time

# --- DATABASE SETUP ---
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

# --- Assets ---
CORRECT_SND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WRONG_SND = "https://www.soundjay.com/buttons/sounds/button-10.mp3"
BOSS_GIF = "https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif"

TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"}
]

# --- Effects ---
def trigger_effects(effect_type):
    if effect_type == "correct":
        st.markdown(f'<audio src="{CORRECT_SND}" autoplay></audio>', unsafe_allow_html=True)
    elif effect_type == "wrong":
        st.markdown(f'<audio src="{WRONG_SND}" autoplay></audio>', unsafe_allow_html=True)
        st.markdown("<script>window.parent.document.querySelector('.stApp').animate([{transform:'translate(2px,2px)'},{transform:'translate(-2px,-2px)'}],{duration:100,iterations:3});</script>", unsafe_allow_html=True)

# --- Session & Stats ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Hero_Player", "player@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)

# --- UI Layout ---
st.set_page_config(page_title="English Guru Pro v37", page_icon="🎓", layout="wide")
st.markdown("""<style>@import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap'); .stApp { background: #0e1117; color: white; }</style>""", unsafe_allow_html=True)

# --- Navigation ---
page = st.sidebar.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🏆 Hall of Fame"])

if page == "🏠 Dashboard":
    st.title("🛡️ HERO DASHBOARD")
    st.metric("Level", user_level)
    st.metric("Total XP", txp)
    st.info("💡 Awaaz sunne ke liye screen par ek baar click karein!")

elif page == "🎓 Training":
    st.title("🎓 Practice Area")
    if 't_q' not in st.session_state: st.session_state.t_q = random.choice(TRAINING_DATA)
    q = st.session_state.t_q
    st.subheader(q['q'])
    for opt in q['o']:
        if st.button(opt, use_container_width=True):
            if opt == q['a']:
                trigger_effects("correct"); st.success("Sahi Jawab!")
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 10))
                conn.commit()
            else:
                trigger_effects("wrong"); st.error("Galat!")
            del st.session_state.t_q; time.sleep(1); st.rerun()

elif page == "⚔️ Boss Battle":
    st.markdown("<h1 style='color:red; font-family:Bungee; text-align:center;'>👹 BOSS ARENA</h1>", unsafe_allow_html=True)
    
    # --- FIXED PROGRESS BARS ---
    boss_max_hp = 100 + (user_level * 25)
    
    # Ye wo safe math hai jo error ko rokega
    p_safe = max(0.0, min(st.session_state.player_hp / 100.0, 1.0))
    b_safe = max(0.0, min(st.session_state.boss_hp / boss_max_hp, 1.0))
    
    col_hp1, col_hp2 = st.columns(2)
    col_hp1.write(f"🛡️ Hero: {int(p_safe*100)}%")
    col_hp1.progress(p_safe)
    col_hp2.write(f"👾 Boss: {int(b_safe*100)}%")
    col_hp2.progress(b_safe)

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("BOSS DEFEATED!")
        if st.button("Spawn Next Monster"):
            st.session_state.boss_hp = 100 + ((user_level + 1) * 25)
            st.session_state.player_hp = 100
            st.rerun()
    elif st.session_state.player_hp <= 0:
        st.error("GAME OVER!")
        if st.button("Revive"): st.session_state.player_hp = 100; st.rerun()
    else:
        st.image(BOSS_GIF, width=200)
        q = TRAINING_DATA[0]
        st.subheader(q['q'])
        ans = st.radio("Choose Your Attack Weapon:", q['o'], horizontal=True)
        if st.button("🔥 EXECUTE ATTACK"):
            if ans == q['a']:
                st.session_state.boss_hp -= 30
                trigger_effects("correct")
            else:
                st.session_state.player_hp -= 20
                trigger_effects("wrong")
            st.rerun()

elif page == "🏆 Hall of Fame":
    st.title("🏆 Leaderboard")
    data = c.execute("SELECT username, SUM(xp) as s FROM progress p JOIN users u ON p.email=u.email GROUP BY u.email ORDER BY s DESC").fetchall()
    for i, row in enumerate(data, 1):
        st.write(f"👑 #{i} {row[0]} - {row[1]} XP")
