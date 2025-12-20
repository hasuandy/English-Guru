import streamlit as st
import sqlite3
import random
import time

# --- 1. DATABASE SETUP ---
# Database background mein chalta rahega taaki features crash na ho
conn = sqlite3.connect('english_guru_guest_mode.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT, xp INTEGER, hp INTEGER, goal INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS vault (word TEXT, meaning TEXT)''')
conn.commit()

# --- 2. SESSION STATE (Bypass Login) ---
# Humne logged_in ko permanent TRUE kar diya hai thodi der ke liye
if 'user' not in st.session_state: st.session_state.user = "Guest Warrior"
if 'user_page' not in st.session_state: st.session_state.user_page = "🏰 Home Base"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'guest_xp' not in st.session_state: st.session_state.guest_xp = 0
if 'guest_hp' not in st.session_state: st.session_state.guest_hp = 100

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. RPG NEON STYLING ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@400;900&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Orbitron', sans-serif; }
    .brand-title { font-family: 'Bungee'; font-size: 4rem; text-align: center; color: #ff0055; text-shadow: 0 0 15px #ff0055; }
    .cyber-card { background: rgba(30, 30, 60, 0.4); border: 1px solid #00f2ff; border-radius: 15px; padding: 25px; box-shadow: 0 0 20px rgba(0, 242, 255, 0.1); text-align: center; }
    .stButton>button { background: linear-gradient(45deg, #ff0055, #00f2ff) !important; color: white !important; font-family: 'Bungee' !important; border-radius: 12px !important; border:none; height: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION SIDEBAR ---
with st.sidebar:
    st.markdown(f"<h1 style='color:#ff0055; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
    st.markdown("⚠️ **GUEST MODE ACTIVE**")
    st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault", "🏆 Leaderboard"], 
                 key="nav_key", on_change=set_page)

# --- 5. PAGES ---
page = st.session_state.user_page
st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

if page == "🏰 Home Base":
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='cyber-card'><h3>XP</h3><h1>{st.session_state.guest_xp}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='cyber-card'><h3>STAMINA</h3><h1>{st.session_state.guest_hp}%</h1></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='cyber-card'><h3>GOAL</h3><h1>100</h1></div>", unsafe_allow_html=True)
    
    st.write("### 📈 Growth Chart")
    st.area_chart({"Progress": [0, 10, 25, st.session_state.guest_xp]})

elif page == "👹 Daily Boss":
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp}/500")
        st.progress(st.session_state.boss_hp/500)
    with col2:
        st.write(f"### 🛡️ YOUR HP: {st.session_state.guest_hp}/100")
        st.progress(st.session_state.guest_hp/100)
    
    st.write("---")
    ans = st.radio("Battle Quiz: 'I ____ to the gym every day.'", ["goes", "go", "going"])
    if st.button("💥 LAUNCH ATTACK"):
        if ans == "go":
            dmg = random.randint(60, 120)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.guest_xp += 50
            st.success(f"CRITICAL HIT! -{dmg} HP to Boss! +50 XP")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.session_state.guest_hp = max(0, st.session_state.guest_hp - 20)
            st.error("MISS! The Boss hit you for 20 damage!")
        time.sleep(1)
        st.rerun()

elif page == "📚 Word Vault":
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    w = st.text_input("Add Word to Vault")
    m = st.text_input("Meaning")
    if st.button("🔒 SEAL WORD"):
        c.execute("INSERT INTO vault VALUES (?,?)", (w, m))
        conn.commit()
        st.success(f"'{w}' has been locked in the vault!")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🏆 Leaderboard":
    st.write("### 💠 TOP WARRIORS (Global)")
    st.markdown("<div class='cyber-card'>1. Yash (Elite) - 2500 XP<br>2. Guest (You) - {} XP</div>".format(st.session_state.guest_xp), unsafe_allow_html=True)
