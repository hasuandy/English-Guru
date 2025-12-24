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

# --- 1. DATABASE SETUP (Version v32) ---
conn = sqlite3.connect('english_guru_pro_v32.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is waiting... 👹"

# DEV MODE AUTO-LOGIN
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"

# --- 3. DATA POOLS ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "no"], "a": "an"}
]
BOSS_DATA = [
    {"q": "Meaning of 'GIGANTIC'?", "o": ["Small", "Tiny", "Huge", "Thin"], "a": "Huge"},
    {"q": "Correct spelling?", "o": ["Recieve", "Receive", "Recive", "Receve"], "a": "Receive"}
]

# --- 4. CSS & UI ---
st.set_page_config(page_title="English Guru V32", page_icon="👑", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255,255,255,0.05); border: 2px solid {st.session_state.theme}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; }}
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

def get_rank(xp):
    if xp < 100: return "🆕 ROOKIE"
    if xp < 300: return "⚔️ WARRIOR"
    if xp < 700: return "🛡️ KNIGHT"
    return "👑 LEGEND"

def play_sound(sound_type):
    # Sounds disabled for Cloud stability, but kept logic
    pass

# --- 5. MAIN CONTENT ---
if st.session_state.logged_in:
    txp = get_total_xp(st.session_state.email)
    rank = get_rank(txp)
    
    with st.sidebar:
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>{st.session_state.user}</h2>", unsafe_allow_html=True)
        st.write(f"💰 **XP:** {txp} | **Rank:** {rank}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Leaderboard"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- BASE (QUEST FIXED) ---
    if page == "🏠 Base":
        st.markdown("<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        today = str(date.today())
        c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
        quest_done = c.fetchone()

        st.markdown("<div class='gaming-card'>", unsafe_allow_html=True)
        st.subheader("📅 DAILY MISSION")
        if not quest_done:
            st.write("🎯 **Task:** Daily Login Reward")
            if st.button("CLAIM 50 XP"):
                c.execute("INSERT INTO daily_tasks (email, task_date, completed) VALUES (?, ?, ?)", (st.session_state.email, today, 1))
                c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, today, 50))
                conn.commit()
                st.success("Reward Claimed!"); st.rerun()
        else: st.write("✅ Mission Accomplished!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- TRAINING (FIXED) ---
    elif page == "🎓 Training":
        st.markdown("<h1 style='font-family:Bungee;'>TRAINING</h1>", unsafe_allow_html=True)
        q = random.choice(TRAINING_DATA)
        st.markdown(f"<div class='gaming-card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
        for opt in q['o']:
            if st.button(opt, key=f"t_{opt}_{time.time()}"):
                if opt == q['a']:
                    c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 10))
                    conn.commit(); st.balloons(); st.rerun()
                else: st.error("Wrong!"); time.sleep(0.5); st.rerun()

    # --- BOSS BATTLE (FIXED) ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS BATTLE</h1>", unsafe_allow_html=True)
        c.execute("SELECT count FROM inventory WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
        res = c.fetchone(); shields = res[0] if res else 0

        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"**HERO: {st.session_state.player_hp}%** | 🛡️ {shields}")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=150)
            st.write(f"**BOSS: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.success("BOSS DEFEATED!")
            # FIXED QUERY HERE
            c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            if st.button("RESET"): st.session_state.boss_hp=100; st.session_state.player_hp=100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("GAME OVER"); 
            if st.button("REVIVE"): st.session_state.player_hp=100; st.rerun()
        else:
            if 'bq' not in st.session_state: st.session_state.bq = random.choice(BOSS_DATA)
            st.markdown(f"<div class='gaming-card'><h3>{st.session_state.bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("ATTACK:", st.session_state.bq['o'], horizontal=True)
            if st.button("🔥 EXECUTE"):
                if ans == st.session_state.bq['a']:
                    st.session_state.boss_hp -= 34; st.session_state.battle_log = "HIT!"
                else:
                    if shields > 0:
                        c.execute("UPDATE inventory SET count=count-1 WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
                        conn.commit(); st.session_state.battle_log = "SHIELD USED"
                    else:
                        st.session_state.player_hp -= 20; st.session_state.battle_log = "BOSS HIT YOU"
                del st.session_state.bq; st.rerun()
        st.info(st.session_state.battle_log)

    # --- SHOP (FIXED) ---
    elif page == "🛒 Shop":
        st.markdown("<h1 style='font-family:Bungee;'>SHOP</h1>", unsafe_allow_html=True)
        if st.button("Buy Shield (50 XP)"):
            if txp >= 50:
                c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), -50))
                c.execute("INSERT INTO inventory (email, item, count) VALUES (?, '🛡️ Mystic Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1", (st.session_state.email,))
                conn.commit(); st.success("Bought!"); st.rerun()
            else: st.error("No XP")

    # --- LEADERBOARD ---
    elif page == "🏆 Leaderboard":
        st.title("RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data): st.write(f"#{i+1} {row[0]} - {row[1]} XP")
