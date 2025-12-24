import streamlit as st
import sqlite3
from datetime import date
import random
import time

# ==========================================
# 🛠️ DATABASE SETUP (V41 - FIXED)
# ==========================================
conn = sqlite3.connect('v41_final.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, avatar TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
conn.commit()

# ==========================================
# ⚙️ SESSION STATE
# ==========================================
if 'logged_in' not in st.session_state: st.session_state.logged_in = True
if 'user' not in st.session_state: st.session_state.user = "Hero Warrior"
if 'email' not in st.session_state: st.session_state.email = "player@guru.com"
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'combo' not in st.session_state: st.session_state.combo = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# ==========================================
# 🎨 ASSETS & DATA
# ==========================================
AVATARS = {
    "Ninja": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    "Robot": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    "Monster": "https://cdn-icons-png.flaticon.com/512/616/616412.png",
    "Ghost": "https://cdn-icons-png.flaticon.com/512/616/616416.png"
}

TRAIN_QS = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"}
]

BOSS_QS = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"}
]

# ==========================================
# ✨ UI & STYLING
# ==========================================
st.set_page_config(page_title="English Guru Pro V41", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp {{ background: #0e1117; color: white; }}
    .gaming-card {{ background: rgba(255,255,255,0.05); border: 2px solid {st.session_state.theme}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; }}
    .stButton>button {{ background: {st.session_state.theme}; color: black !important; font-family: 'Bungee'; border-radius: 10px; width: 100%; font-weight: bold; }}
    .hp-bar {{ height: 20px; border-radius: 10px; background: #111; overflow: hidden; border: 1px solid #444; margin-bottom: 5px; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🕹️ LOGIC FUNCTIONS (CALLBACKS)
# ==========================================
def get_xp():
    c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
    res = c.fetchone()[0]
    return res if res else 0

def check_training(choice, correct):
    if choice == correct:
        st.session_state.combo += 1
        gain = 10 if st.session_state.combo < 3 else 20
        c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), gain))
        conn.commit()
        st.toast(f"✅ Correct! +{gain} XP", icon="🔥")
    else:
        st.session_state.combo = 0
        st.toast("❌ Wrong Choice!", icon="💀")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# ==========================================
# 🎮 MAIN APP
# ==========================================
# Database Sync
c.execute("INSERT OR IGNORE INTO users (email, username, avatar) VALUES (?, ?, ?)", (st.session_state.email, st.session_state.user, "Ninja"))
conn.commit()
c.execute("SELECT username, avatar FROM users WHERE email=?", (st.session_state.email,))
u_data = c.fetchone()
u_name, u_avatar = u_data[0], u_data[1]

# Sidebar Navigation
with st.sidebar:
    st.image(AVATARS.get(u_avatar, AVATARS["Ninja"]), width=100)
    st.markdown(f"### {u_name}")
    st.write(f"💰 XP: {get_xp()}")
    page = st.radio("Navigation", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "⚙️ Profile Settings"])

# --- PAGE: BASE ---
if page == "🏠 Base":
    st.title("🏠 Command Center")
    st.markdown(f"<div class='gaming-card'><h2>Welcome Back, {u_name}!</h2><p>Ready to level up your English skills?</p></div>", unsafe_allow_html=True)

# --- PAGE: TRAINING ---
elif page == "🎓 Training":
    st.title("🎓 Training Zone")
    if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAIN_QS)
    tq = st.session_state.current_tq
    st.write(f"**Combo Streak:** {'🔥' * st.session_state.combo}")
    st.markdown(f"<div class='gaming-card'><h3>{tq['q']}</h3></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, opt in enumerate(tq['o']):
        with cols[i%2]:
            st.button(opt, key=f"t_{i}", on_click=check_training, args=(opt, tq['a']))

# --- PAGE: BOSS BATTLE ---
elif page == "⚔️ Boss Battle":
    st.title("⚔️ Boss Arena")
    col_p, col_b = st.columns(2)
    with col_p:
        st.write(f"**HERO HP: {st.session_state.player_hp}%**")
        st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:{st.session_state.theme};'></div></div>", unsafe_allow_html=True)
    with col_b:
        st.write(f"**BOSS HP: {st.session_state.boss_hp}%**")
        st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)
    
    if st.session_state.boss_hp <= 0:
        st.success("🏆 VICTORY! Boss Defeated!")
        if st.button("Spawn Next Boss"): 
            st.session_state.boss_hp = 100
            st.session_state.player_hp = 100
            st.rerun()
    elif st.session_state.player_hp <= 0:
        st.error("💀 You Fainted!")
        if st.button("Revive (100% HP)"): 
            st.session_state.player_hp = 100
            st.rerun()
    else:
        if 'current_bq' not in st.session_state: st.session_state.current_bq = random.choice(BOSS_QS)
        bq = st.session_state.current_bq
        st.markdown(f"<div class='gaming-card'><h3>{bq['q']}</h3></div>", unsafe_allow_html=True)
        b_cols = st.columns(2)
        for i, opt in enumerate(bq['o']):
            with b_cols[i%2]:
                if st.button(opt, key=f"b_{i}"):
                    if opt == bq['a']:
                        st.session_state.boss_hp -= 34
                        st.toast("💥 Critical Hit!", icon="⚔️")
                    else:
                        st.session_state.player_hp -= 25
                        st.toast("⚠️ Boss Countered!", icon="💥")
                    del st.session_state.current_bq
                    st.rerun()

# --- PAGE: PROFILE ---
elif page == "⚙️ Profile Settings":
    st.title("⚙️ Profile Settings")
    new_n = st.text_input("Change Username", value=u_name)
    if st.button("Update Name"):
        c.execute("UPDATE users SET username=? WHERE email=?", (new_n, st.session_state.email))
        conn.commit()
        st.rerun()
    st.divider()
    st.write("### Choose Your Avatar")
    acols = st.columns(4)
    for i, (name, url) in enumerate(AVATARS.items()):
        with acols[i]:
            st.image(url, width=80)
            if st.button(f"Pick {name}"):
                c.execute("UPDATE users SET avatar=? WHERE email=?", (name, st.session_state.email))
                conn.commit()
                st.rerun()
