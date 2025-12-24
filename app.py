import streamlit as st
import sqlite3
from datetime import date
import random
import time

# ==========================================
# 🛠️ DATABASE & SESSION SETUP
# ==========================================
conn = sqlite3.connect('v39_final.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, avatar TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary 
             (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory 
             (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks 
             (email TEXT, task_date TEXT, completed INTEGER)''')
conn.commit()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

# DEV AUTO-LOGIN (Change for production)
if not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Warrior", "player@guru.com"

# ==========================================
# 🎨 ASSETS & DATA
# ==========================================
AVATARS = {
    "Ninja": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    "Robot": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    "Monster": "https://cdn-icons-png.flaticon.com/512/616/616412.png",
    "Ghost": "https://cdn-icons-png.flaticon.com/512/616/616416.png",
    "Cat": "https://cdn-icons-png.flaticon.com/512/616/616432.png",
    "Alien": "https://cdn-icons-png.flaticon.com/512/616/616421.png"
}

TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"}
]

BOSS_POOL = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"}
]

# ==========================================
# ✨ UI & CSS
# ==========================================
st.set_page_config(page_title="English Guru Pro V39", page_icon="⚔️", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255,255,255,0.05); border: 2px solid {st.session_state.theme}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; box-shadow: 0 0 15px {st.session_state.theme}33; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border: none; border-radius: 10px; width: 100%; transition: 0.3s; }}
    .hp-bar {{ height: 20px; border-radius: 10px; background: #111; overflow: hidden; border: 1px solid #444; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# ⚙️ LOGIC FUNCTIONS
# ==========================================
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def check_training_answer(user_choice, correct_answer):
    if user_choice == correct_answer:
        st.session_state.combo += 1
        gain = 10 if st.session_state.combo < 3 else 20
        c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), gain))
        conn.commit(); st.toast(f"✅ Correct! +{gain} XP", icon="🔥")
    else:
        st.session_state.combo = 0; st.toast("❌ Wrong Answer!", icon="💀")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# ==========================================
# 🎮 MAIN APP
# ==========================================
if st.session_state.logged_in:
    # Sync User Data
    c.execute("INSERT OR IGNORE INTO users (email, username, avatar) VALUES (?, ?, ?)", (st.session_state.email, st.session_state.user, "Ninja"))
    conn.commit()
    
    c.execute("SELECT username, avatar FROM users WHERE email=?", (st.session_state.email,))
    u_db = c.fetchone()
    u_name, u_avatar_key = u_db[0], u_db[1]
    
    txp = get_total_xp(st.session_state.email)
    user_lvl = 1 + (txp // 100)

    # Sidebar Navigation
    with st.sidebar:
        st.image(AVATARS.get(u_avatar_key, AVATARS["Ninja"]), width=120)
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>{u_name}</h2>", unsafe_allow_html=True)
        st.write(f"🎖️ **Level:** {user_lvl} | 💰 **XP:** {txp}")
        page = st.radio("NAVIGATION", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "⚙️ Profile Settings"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- PAGE: BASE ---
    if page == "🏠 Base":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.metric("Current Level", user_lvl)
        with col2: st.metric("Experience Points", txp)
        
        st.markdown("<div class='gaming-card'><h3>Daily Mission</h3><p>Complete training to earn combo bonus!</p></div>", unsafe_allow_html=True)

    # --- PAGE: TRAINING (WITH CALLBACKS) ---
    elif page == "🎓 Training":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>TRAINING ZONE</h1>", unsafe_allow_html=True)
        tab_mcq, tab_vault = st.tabs(["🔥 MCQ PRACTICE", "📚 WORD VAULT"])
        
        with tab_mcq:
            if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAINING_DATA)
            tq = st.session_state.current_tq
            st.markdown(f"**Combo Streak:** {'🔥' * st.session_state.combo} ({st.session_state.combo})")
            st.markdown(f"<div class='gaming-card'><h2>{tq['q']}</h2></div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, opt in enumerate(tq['o']):
                with cols[i%2]:
                    st.button(opt, key=f"t_{i}", on_click=check_training_answer, args=(opt, tq['a']))

        with tab_vault:
            w = st.text_input("New Word")
            m = st.text_input("Meaning")
            if st.button("ADD TO DICTIONARY"):
                if w and m:
                    c.execute("INSERT INTO dictionary (email, word, meaning) VALUES (?, ?, ?)", (st.session_state.email, w, m))
                    conn.commit(); st.success("Saved!")

    # --- PAGE: BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS ARENA</h1>", unsafe_allow_html=True)
        
        # Difficulty Scaling
        current_boss_hp_max = 100 + (user_lvl * 20)
        boss_dmg = 15 + (user_lvl * 5)
        
        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"**HERO: {st.session_state.player_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:{st.session_state.theme};'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=120)
            boss_pct = (st.session_state.boss_hp / current_boss_hp_max) * 100
            st.write(f"**BOSS: {st.session_state.boss_hp} / {current_boss_hp_max}**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{boss_pct}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("🏆 BOSS DEFEATED!"); c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 100)); conn.commit()
            if st.button("SPAWN NEXT"): st.session_state.boss_hp = current_boss_hp_max + 20; st.session_state.player_hp=100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 DEFEATED"); 
            if st.button("REVIVE"): st.session_state.player_hp=100; st.rerun()
        else:
            if 'bq' not in st.session_state: st.session_state.bq = random.choice(BOSS_POOL)
            st.markdown(f"<div class='gaming-card'><h3>{st.session_state.bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("CHOOSE ATTACK:", st.session_state.bq['o'], horizontal=True)
            if st.button("🔥 EXECUTE ATTACK"):
                if ans == st.session_state.bq['a']: st.session_state.boss_hp -= 40
                else: st.session_state.player_hp -= boss_dmg
                del st.session_state.bq; st.rerun()

    # --- PAGE: PROFILE SETTINGS ---
    elif page == "⚙️ Profile Settings":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>IDENTITY SETTINGS</h1>", unsafe_allow_html=True)
        
        new_name = st.text_input("Update Display Name", value=u_name)
        if st.button("SAVE USERNAME"):
            c.execute("UPDATE users SET username=? WHERE email=?", (new_name, st.session_state.email))
            conn.commit(); st.success("Name updated!"); time.sleep(1); st.rerun()
            
        st.divider()
        st.subheader("Select Your Hero Avatar")
        cols = st.columns(3)
        for i, (name, url) in enumerate(AVATARS.items()):
            with cols[i % 3]:
                st.image(url, width=80)
                if st.button(f"Choose {name}"):
                    c.execute("UPDATE users SET avatar=? WHERE email=?", (name, st.session_state.email))
                    conn.commit(); st.rerun()
