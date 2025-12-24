import streamlit as st
import sqlite3
import random
from datetime import date

# ==========================================
# 1. DATABASE ENGINE (Error-Proof)
# ==========================================
DB_NAME = 'final_v99.db'

def run_query(query, params=()):
    with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()

# Initialize Tables
run_query('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, avatar TEXT)''')
run_query('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, xp INTEGER)''')

# ==========================================
# 2. SESSION & UI SETUP
# ==========================================
st.set_page_config(page_title="English Guru Final", layout="wide")

if 'xp' not in st.session_state: st.session_state.xp = 0
if 'user' not in st.session_state: st.session_state.user = "Hero"
if 'email' not in st.session_state: st.session_state.email = "test@guru.com"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; background: #00f2ff; color: black; font-weight: bold; }
    .stat-card { padding: 20px; border: 2px solid #00f2ff; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR & NAV
# ==========================================
# Sync with DB
run_query("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (st.session_state.email, st.session_state.user, "Ninja"))
db_user = run_query("SELECT username FROM users WHERE email=?", (st.session_state.email,))
u_name = db_user[0][0] if db_user else st.session_state.user

with st.sidebar:
    st.title(f"🎮 {u_name}")
    xp_data = run_query("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
    total_xp = xp_data[0][0] if xp_data[0][0] else 0
    st.metric("Total XP", total_xp)
    page = st.radio("Menu", ["Base", "Training", "Boss Battle", "Settings"])

# ==========================================
# 4. PAGES
# ==========================================

if page == "Base":
    st.header("🏠 Home Base")
    st.markdown(f"<div class='stat-card'><h1>Welcome {u_name}</h1><p>Level Up by Training!</p></div>", unsafe_allow_html=True)

elif page == "Training":
    st.header("🎓 Training")
    q = {"q": "Opposite of 'FAST'?", "o": ["Quick", "Slow", "Run", "High"], "a": "Slow"}
    
    st.subheader(q["q"])
    ans = st.radio("Choose:", q["o"])
    
    if st.button("Submit Answer"):
        if ans == q["a"]:
            run_query("INSERT INTO progress VALUES (?, ?)", (st.session_state.email, 10))
            st.success("Correct! +10 XP Sent to Database")
            st.balloons()
        else:
            st.error("Wrong! Try again.")

elif page == "Boss Battle":
    st.header("⚔️ Boss Arena")
    col1, col2 = st.columns(2)
    with col1: st.metric("Boss HP", f"{st.session_state.boss_hp}%")
    
    if st.button("🔥 ATTACH BOSS"):
        st.session_state.boss_hp -= 20
        if st.session_state.boss_hp <= 0:
            st.success("Victory!")
            st.session_state.boss_hp = 100
        st.rerun()

elif page == "Settings":
    st.header("⚙️ Settings")
    new_name = st.text_input("Change Name", value=u_name)
    if st.button("Update"):
        run_query("UPDATE users SET username=? WHERE email=?", (new_name, st.session_state.email))
        st.success("Name Changed!")
        st.rerun()
