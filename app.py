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

# --- 1. DATABASE SETUP (Version v33) ---
conn = sqlite3.connect('english_guru_pro_v33.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff" # Default Neon Blue
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

# --- 4. CSS (Dynamic Theme Based) ---
st.set_page_config(page_title="English Guru V33", page_icon="🎨", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255,255,255,0.05); border: 2px solid {st.session_state.theme}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; box-shadow: 0 0 15px {st.session_state.theme}33; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border: none; border-radius: 10px; transition: 0.3s; }}
    .stButton>button:hover {{ transform: scale(1.02); box-shadow: 0 0 20px {st.session_state.theme}; }}
    .hp-bar {{ height: 20px; border-radius: 10px; background: #111; overflow: hidden; border: 1px solid #444; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# HELPER FUNCTIONS
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

# --- 5. MAIN CONTENT ---
if st.session_state.logged_in:
    txp = get_total_xp(st.session_state.email)
    
    with st.sidebar:
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>{st.session_state.user}</h2>", unsafe_allow_html=True)
        st.write(f"💰 **XP Balance:** {txp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Leaderboard"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- BASE ---
    if page == "🏠 Base":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>COMMAND CENTER</h1>", unsafe_allow_html=True)
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
                conn.commit(); st.success("Reward Claimed!"); time.sleep(1); st.rerun()
        else: st.write("✅ Mission Accomplished for today!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- SHOP (THEME STORE ADDED) ---
    elif page == "🛒 Shop":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>ULTRA SHOP</h1>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🛡️ POWER-UPS", "🎨 THEME STORE"])
        
        with tab1:
            st.markdown("<div class='gaming-card'>🛡️<h3>Mystic Shield</h3><p>Blocks 1 Boss Attack</p><b>Cost: 50 XP</b></div>", unsafe_allow_html=True)
            if st.button("BUY SHIELD"):
                if txp >= 50:
                    c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), -50))
                    c.execute("INSERT INTO inventory (email, item, count) VALUES (?, '🛡️ Mystic Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1", (st.session_state.email,))
                    conn.commit(); st.success("Shield Purchased!"); st.rerun()
                else: st.error("Inadequate XP!")

        with tab2:
            st.write("### Customize Your UI")
            themes = [
                {"name": "Neon Red", "color": "#ff4b4b", "price": 100},
                {"name": "Golden", "color": "#ffcc00", "price": 200},
                {"name": "Emerald", "color": "#00ff88", "price": 150}
            ]
            cols = st.columns(3)
            for i, t in enumerate(themes):
                with cols[i]:
                    st.markdown(f"<div style='background:{t['color']}; height:40px; border-radius:10px; border:2px solid white;'></div>", unsafe_allow_html=True)
                    if st.button(f"Unlock {t['name']} ({t['price']} XP)"):
                        if txp >= t['price']:
                            st.session_state.theme = t['color']
                            c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), -t['price']))
                            conn.commit(); st.success(f"{t['name']} Theme Applied!"); time.sleep(1); st.rerun()
                        else: st.error("Need more XP!")

    # --- TRAINING ---
    elif page == "🎓 Training":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>TRAINING ZONE</h1>", unsafe_allow_html=True)
        q = random.choice(TRAINING_DATA)
        st.markdown(f"<div class='gaming-card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
        for opt in q['o']:
            if st.button(opt, key=f"t_{opt}_{time.time()}"):
                if opt == q['a']:
                    c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 10))
                    conn.commit(); st.balloons(); st.rerun()
                else: st.error("Wrong!"); time.sleep(0.5); st.rerun()

    # --- BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS ARENA</h1>", unsafe_allow_html=True)
        c.execute("SELECT count FROM inventory WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
        res = c.fetchone(); shields = res[0] if res else 0

        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"**HERO HP: {st.session_state.player_hp}%** | 🛡️ {shields}")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:{st.session_state.theme};'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=150)
            st.write(f"**BOSS HP: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.success("🏆 BOSS DEFEATED!"); c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 100)); conn.commit()
            if st.button("SPAWN NEW BOSS"): st.session_state.boss_hp=100; st.session_state.player_hp=100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 GAME OVER"); 
            if st.button("REVIVE"): st.session_state.player_hp=100; st.rerun()
        else:
            if 'bq' not in st.session_state: st.session_state.bq = random.choice(BOSS_DATA)
            st.markdown(f"<div class='gaming-card'><h3>{st.session_state.bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("SELECT WEAPON:", st.session_state.bq['o'], horizontal=True)
            if st.button("💥 LAUNCH"):
                if ans == st.session_state.bq['a']:
                    st.session_state.boss_hp -= 34; st.session_state.battle_log = "DIRECT HIT! 34 DMG"
                else:
                    if shields > 0:
                        c.execute("UPDATE inventory SET count=count-1 WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
                        conn.commit(); st.session_state.battle_log = "🛡️ SHIELD BLOCKED!"
                    else:
                        st.session_state.player_hp -= 20; st.session_state.battle_log = "⚠️ COUNTERED! 20 DMG"
                del st.session_state.bq; st.rerun()
        st.info(st.session_state.battle_log)

    # --- LEADERBOARD ---
    elif page == "🏆 Leaderboard":
        st.title("GLOBAL RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.markdown(f"<div class='gaming-card' style='text-align:left;'>#{i+1} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)
