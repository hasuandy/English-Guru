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

# --- 1. DATABASE SETUP (Version v34) ---
conn = sqlite3.connect('english_guru_pro_v34.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Prepare for battle! ⚔️"

# DEV MODE AUTO-LOGIN
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"

# --- 3. DYNAMIC DATA POOLS ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"}
]
# Hard Boss Questions for Higher Levels
BOSS_POOL = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"}
]

# --- 4. CSS ---
st.set_page_config(page_title="English Guru V34", page_icon="⚔️", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255,255,255,0.05); border: 2px solid {st.session_state.theme}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; box-shadow: 0 0 15px {st.session_state.theme}33; }}
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
    user_level = 1 + (txp // 100)
    
    with st.sidebar:
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>{st.session_state.user}</h2>", unsafe_allow_html=True)
        st.write(f"🎖️ **Level:** {user_level} | 💰 **XP:** {txp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Leaderboard"])

    # --- BOSS BATTLE (With Difficulty Scaling) ---
    if page == "⚔️ Boss Battle":
        # Boss Stats Scale with Level
        current_boss_max_hp = 100 + (user_level * 25)
        boss_dmg = 15 + (user_level * 5)
        
        st.markdown(f"<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS ARENA (LVL {user_level})</h1>", unsafe_allow_html=True)
        
        c.execute("SELECT count FROM inventory WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
        res = c.fetchone(); shields = res[0] if res else 0

        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"**HERO HP: {st.session_state.player_hp}%** | 🛡️ {shields}")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:{st.session_state.theme};'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=150)
            boss_pct = (st.session_state.boss_hp / current_boss_max_hp) * 100
            st.write(f"**BOSS HP: {st.session_state.boss_hp} / {current_boss_max_hp}**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{boss_pct}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            reward = 100 + (user_level * 10)
            st.balloons(); st.success(f"🏆 BOSS DEFEATED! +{reward} XP")
            c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), reward))
            conn.commit()
            if st.button("NEXT BOSS"): 
                st.session_state.boss_hp = 100 + ((user_level+1) * 25)
                st.session_state.player_hp = 100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 DEFEAT!"); 
            if st.button("REVIVE"): st.session_state.player_hp=100; st.rerun()
        else:
            if 'bq' not in st.session_state: st.session_state.bq = random.choice(BOSS_POOL)
            st.markdown(f"<div class='gaming-card'><h3>{st.session_state.bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("SELECT ATTACK:", st.session_state.bq['o'], horizontal=True)
            if st.button("🔥 LAUNCH"):
                if ans == st.session_state.bq['a']:
                    st.session_state.boss_hp -= 40
                    st.session_state.battle_log = "✅ DIRECT HIT! 40 DMG"
                else:
                    if shields > 0:
                        c.execute("UPDATE inventory SET count=count-1 WHERE email=? AND item='🛡️ Mystic Shield'", (st.session_state.email,))
                        conn.commit(); st.session_state.battle_log = "🛡️ SHIELD BLOCKED THE HIT!"
                    else:
                        st.session_state.player_hp -= boss_dmg
                        st.session_state.battle_log = f"⚠️ BOSS COUNTERED! Took {boss_dmg} DMG!"
                del st.session_state.bq; st.rerun()
        st.info(st.session_state.battle_log)

    # --- Other pages (Base, Shop, etc.) kept same as v33 ---
    elif page == "🏠 Base":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        st.write("Welcome back, Commander.")
        st.metric("Total XP", txp)
        st.metric("Level", user_level)

    elif page == "🛒 Shop":
        st.markdown("### ULTRA SHOP")
        if st.button("Buy Shield (50 XP)"):
            if txp >= 50:
                c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), -50))
                c.execute("INSERT INTO inventory (email, item, count) VALUES (?, '🛡️ Mystic Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1", (st.session_state.email,))
                conn.commit(); st.success("Bought!"); st.rerun()

    elif page == "🎓 Training":
        q = random.choice(TRAINING_DATA)
        st.markdown(f"<div class='gaming-card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
        if st.button("Submit Answer"): # Basic structure for brevity
            pass
