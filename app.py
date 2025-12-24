import streamlit as st
import sqlite3
from datetime import date
import random
import time

# --- 1. DATABASE SETUP (Version v38) ---
conn = sqlite3.connect('english_guru_pro_v38.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, avatar TEXT)''')
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
if 'combo' not in st.session_state: st.session_state.combo = 0

# DEV MODE AUTO-LOGIN
if not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"

# --- 3. AVATAR DATA ---
AVATARS = {
    "Ninja": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    "Robot": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    "Monster": "https://cdn-icons-png.flaticon.com/512/616/616412.png",
    "Ghost": "https://cdn-icons-png.flaticon.com/512/616/616416.png",
    "Cat": "https://cdn-icons-png.flaticon.com/512/616/616432.png",
    "Alien": "https://cdn-icons-png.flaticon.com/512/616/616421.png"
}

# --- 4. DATA POOLS ---
TRAINING_DATA = [{"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"}]
BOSS_POOL = [{"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"}]

# --- 5. CSS ---
st.set_page_config(page_title="English Guru V38", page_icon="👤", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255,255,255,0.05); border: 2px solid {st.session_state.theme}; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def get_user_data(email):
    c.execute("SELECT username, avatar FROM users WHERE email=?", (email,))
    return c.fetchone()

# CALLBACKS
def check_training_answer(user_choice, correct_answer):
    if user_choice == correct_answer:
        st.session_state.combo += 1
        gain = 10 if st.session_state.combo < 3 else 20
        c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), gain))
        conn.commit(); st.toast(f"✅ Correct! +{gain} XP")
    else:
        st.session_state.combo = 0; st.toast("❌ Wrong!")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# --- 6. MAIN CONTENT ---
if st.session_state.logged_in:
    # Ensure user exists in DB for this version
    c.execute("INSERT OR IGNORE INTO users (email, username, avatar) VALUES (?, ?, ?)", (st.session_state.email, st.session_state.user, "Ninja"))
    conn.commit()
    
    u_name, u_avatar_key = get_user_data(st.session_state.email)
    txp = get_total_xp(st.session_state.email)
    user_level = 1 + (txp // 100)
    
    with st.sidebar:
        st.image(AVATARS.get(u_avatar_key, AVATARS["Ninja"]), width=100)
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>{u_name}</h2>", unsafe_allow_html=True)
        st.write(f"🎖️ **Level:** {user_level} | 💰 **XP:** {txp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Leaderboard", "⚙️ Profile Settings"])

    # --- PROFILE SETTINGS ---
    if page == "⚙️ Profile Settings":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>PROFILE SETTINGS</h1>", unsafe_allow_html=True)
        
        with st.container():
            st.subheader("Edit Identity")
            new_name = st.text_input("Change Username", value=u_name)
            if st.button("UPDATE NAME"):
                c.execute("UPDATE users SET username=? WHERE email=?", (new_name, st.session_state.email))
                conn.commit(); st.session_state.user = new_name; st.success("Name Updated!"); st.rerun()
            
            st.divider()
            st.subheader("Choose Your Avatar")
            cols = st.columns(3)
            for i, (name, url) in enumerate(AVATARS.items()):
                with cols[i % 3]:
                    st.image(url, width=80)
                    if st.button(f"Select {name}"):
                        c.execute("UPDATE users SET avatar=? WHERE email=?", (name, st.session_state.email))
                        conn.commit(); st.success(f"{name} Activated!"); st.rerun()

    # --- OTHER PAGES (BASE, TRAINING, BOSS) ---
    elif page == "🏠 Base":
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        st.metric("Total XP", txp)
        
    elif page == "🎓 Training":
        st.markdown("<h1 style='font-family:Bungee;'>TRAINING</h1>", unsafe_allow_html=True)
        if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAINING_DATA)
        tq = st.session_state.current_tq
        st.markdown(f"<div class='gaming-card'><h2>{tq['q']}</h2></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(tq['o']):
            with cols[i%2]: st.button(opt, key=f"t_{i}", on_click=check_training_answer, args=(opt, tq['a']), use_container_width=True)

    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS ARENA</h1>", unsafe_allow_html=True)
        st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=120)
        # (Rest of boss logic from v37...)
        st.write("Boss battle is ready! Attack to win XP.")

    elif page == "🏆 Leaderboard":
        st.title("RANKINGS")
        data = c.execute("SELECT username, SUM(xp) FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY SUM(xp) DESC").fetchall()
        for i, row in enumerate(data): st.write(f"#{i+1} {row[0]} - {row[1]} XP")
