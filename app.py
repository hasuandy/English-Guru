import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# ==========================================
# 🛠️ DEVELOPER SETTINGS
DEV_MODE = True 
# ==========================================

# --- 1. DATABASE SETUP (Version v38) ---
conn = sqlite3.connect('english_guru_pro_v38.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER, hero_class TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS achievements (email TEXT, name TEXT, date TEXT, UNIQUE(email, name))''')
conn.commit()

# --- 2. SESSION STATE ---
for key, default in [('logged_in', False), ('theme', '#00f2ff'), ('boss_hp', 100), ('player_hp', 100), ('battle_log', 'Prepare for battle! ⚔️'), ('combo', 0), ('story_stage', 0)]:
    if key not in st.session_state: st.session_state[key] = default

# DEV MODE AUTO-LOGIN
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email, st.session_state.hero_class = True, "Tester_Hero", "test@guru.com", "Grammar Knight"

# --- 3. DYNAMIC DATA POOLS ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
    {"q": "I ____ a student.", "o": ["is", "am", "are", "be"], "a": "am"}
]

BOSS_POOL = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"}
]

STORY_STAGES = [
    {"name": "🌲 Forest of Words", "questions": 3},
    {"name": "🏰 Grammar Castle", "questions": 3},
    {"name": "🐉 Vocabulary Dragon", "questions": 3},
    {"name": "👑 English Emperor", "questions": 1}
]

# --- 4. CSS ---
st.set_page_config(page_title="English Guru V38", page_icon="🎓", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255,255,255,0.05); border: 2px solid {st.session_state.theme}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; box-shadow: 0 0 15px {st.session_state.theme}33; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border: none; border-radius: 10px; }}
    .hp-bar {{ height: 20px; border-radius: 10px; background: #111; overflow: hidden; border: 1px solid #444; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# HELPER FUNCTIONS
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def unlock_achievement(name):
    try:
        c.execute("INSERT INTO achievements (email, name, date) VALUES (?, ?, ?)" , (st.session_state.email, name, str(date.today())))
        conn.commit()
        st.toast(f"🏆 Achievement Unlocked: {name}")
    except:
        pass

# CALLBACK FOR TRAINING
def check_training_answer(user_choice, correct_answer):
    if user_choice == correct_answer:
        st.session_state.combo += 1
        gain = 10 if st.session_state.combo < 3 else 20
        if st.session_state.hero_class == "Grammar Knight": gain += 5
        c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", 
                 (st.session_state.email, str(date.today()), gain))
        conn.commit()
        st.toast(f"✅ Correct! +{gain} XP", icon="🔥")
        if st.session_state.combo >= 5: unlock_achievement("🔥 Fire Combo")
    else:
        st.session_state.combo = 0
        st.toast(f"❌ Wrong! Correct: {correct_answer}", icon="💀")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# --- 5. MAIN CONTENT ---
if st.session_state.logged_in:
    txp = get_total_xp(st.session_state.email)
    user_level = 1 + (txp // 100)
    with st.sidebar:
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>{st.session_state.user}</h2>", unsafe_allow_html=True)
        st.write(f"🎖️ **Level:** {user_level} | 💰 **XP:** {txp}")
        st.write(f"🧙 Hero Class: {st.session_state.hero_class}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Leaderboard"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- BASE PAGE ---
    if page == "🏠 Base":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.metric("Level", user_level)
        with col2: st.metric("Total XP", txp)
        today = str(date.today())
        c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
        if not c.fetchone():
            if st.button("CLAIM DAILY 50 XP"):
                c.execute("INSERT INTO daily_tasks (email, task_date, completed) VALUES (?, ?, ?)", (st.session_state.email, today, 1))
                c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)" , (st.session_state.email, today, 50))
                conn.commit(); st.rerun()

    # --- TRAINING ---
    elif page == "🎓 Training":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>🎓 TRAINING</h1>", unsafe_allow_html=True)
        t_tab1, t_tab2 = st.tabs(["🔥 MCQ PRACTICE", "📚 WORD VAULT"])
        with t_tab1:
            if 'current_tq' not in st.session_state:
                st.session_state.current_tq = random.choice(TRAINING_DATA)
            tq = st.session_state.current_tq
            st.markdown(f"### Combo: {'🔥' * st.session_state.combo} ({st.session_state.combo})")
            st.markdown(f"<div class='gaming-card'><h2>{tq['q']}</h2></div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, opt in enumerate(tq['o']):
                with cols[i % 2]:
                    st.button(opt, key=f"t_opt_{i}", on_click=check_training_answer, args=(opt, tq['a']), use_container_width=True)
        with t_tab2:
            st.subheader("Your Personal Dictionary")
            w = st.text_input("Word")
            m = st.text_input("Meaning")
            if st.button("SAVE"):
                if w and m:
                    c.execute("INSERT INTO dictionary (email, word, meaning) VALUES (?, ?, ?)", (st.session_state.email, w, m))
                    conn.commit(); st.success("Saved!")
            words = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
            for row in words: st.write(f"📖 **{row[0]}**: {row[1]}")

    # --- BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        current_boss_max_hp = 100 + (user_level * 25)
        boss_dmg = 15 + (user_level * 5)
        st.markdown(f"<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS ARENA</h1>", unsafe_allow_html=True)
        c.execute("SELECT count FROM inventory WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
        res = c.fetchone(); shields = res[0] if res else 0
        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"**HERO: {st.session_state.player_hp}%** | 🛡️ {shields}")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:{st.session_state.theme};'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=120)
            boss_pct = (st.session_state.boss_hp / current_boss_max_hp) * 100
            st.write(f"**BOSS: {st.session_state.boss_hp} / {current_boss_max_hp}**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{boss_pct}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)
        if st.session_state.boss_hp <= 0:
            st.balloons()
            c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            st.success("Victory! +100 XP")
            unlock_achievement("Boss Slayer")
            if st.button("SPAWN NEXT"):
                st.session_state.boss_hp = 100 + ((user_level+1)*25)
                st.session_state.player_hp=100
                st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 DEFEATED")
            if st.button("REVIVE"):
                st.session_state.player_hp=100
                st.rerun()
        else:
            if 'bq' not in st.session_state: st.session_state.bq = random.choice(BOSS_POOL)
            st.markdown(f"<div class='gaming-card'><h3>{st.session_state.bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("CHOOSE:", st.session_state.bq['o'], horizontal=True)
            if st.button("🔥 ATTACK"):
                if ans == st.session_state.bq['a']:
                    st.session_state.boss_hp -= 40
                else:
                    if shields > 0:
                        c.execute("UPDATE inventory SET count=count-1 WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
                        conn.commit()
                    else: st.session_state.player_hp -= boss_dmg
                del st.session_state.bq
                st.rerun()

    # --- SHOP ---
    elif page == "🛒 Shop":
        st.markdown("<h1 style='font-family:Bungee;'>SHOP</h1>", unsafe_allow_html=True)
        if st.button("Buy Shield (50 XP)"):
            if txp >= 50:
                c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), -50))
                c.execute("INSERT INTO inventory (email, item, count) VALUES (?, '🛡️ Mystic Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1", (st.session_state.email,))
                conn.commit(); st.success("Bought!")
                st.rerun()

    # --- LEADERBOARD ---
    elif page == "🏆 Leaderboard":
        st.title("RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data): st.write(f"#{i+1} {row[0]} - {row[1]} XP")
        st.subheader("Achievements")
        achs = c.execute("SELECT name, date FROM achievements WHERE email=?", (st.session_state.email,)).fetchall()
        for a in achs: st.write(f"🏅 {a[0]} ({a[1]})")
