import sys
import streamlit as st
import sqlite3
from datetime import date, timedelta
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v28.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS progress (username TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (username TEXT, word TEXT, meaning TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'user' not in st.session_state: st.session_state.user = "Admin_Tester"
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'page' not in st.session_state: st.session_state.page = "🏠 Home Base"
if 'opponent' not in st.session_state: st.session_state.opponent = None
if 'p1_hp' not in st.session_state: st.session_state.p1_hp = 100
if 'p2_hp' not in st.session_state: st.session_state.p2_hp = 100

# --- 3. DATASET ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Plural of 'MOUSE'?", "o": ["Mouses", "Mice", "Mices", "Mouse"], "a": "Mice"},
    {"q": "Correct spelling?", "o": ["Recieve", "Receive", "Receve", "Riceive"], "a": "Receive"}
]

# --- 4. CSS ---
st.set_page_config(page_title="Arena Edition", page_icon="⚔️", layout="centered")
st.markdown(f"""
    <style>
    .stApp {{ background: #0d0d1a; color: #ffffff; }}
    .arena-box {{
        background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px;
        border: 2px solid {st.session_state.theme}; text-align: center; margin: 10px 0px;
    }}
    .hp-bar {{ height: 15px; border-radius: 10px; background: #333; overflow: hidden; margin: 5px 0; }}
    .hp-fill {{ height: 100%; transition: width 0.5s; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNCTIONS ---
def add_xp(pts):
    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.user, str(date.today()), pts))
    conn.commit()

# --- 6. SIDEBAR ---
with st.sidebar:
    st.title("GURU PRO")
    st.session_state.page = st.radio("MENU:", ["🏠 Home Base", "⚔️ Global Arena", "🎓 MCQ Academy", "🏆 Leaderboard", "⚙️ Settings"])

# --- 7. ARENA MODE (MULTIPLAYER LOGIC) ---
if st.session_state.page == "⚔️ Global Arena":
    st.markdown("<h1>⚔️ GLOBAL ARENA</h1>", unsafe_allow_html=True)
    
    if st.session_state.opponent is None:
        st.info("Searching for online opponents...")
        if st.button("Find Match"):
            # Dummy Matchmaking
            st.session_state.opponent = random.choice(["Gamer_X", "Vocab_Ninja", "English_Pro"])
            st.rerun()
    else:
        st.write(f"### Match: {st.session_state.user} vs {st.session_state.opponent}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"You: {st.session_state.p1_hp} HP")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.p1_hp}%; background:cyan;'></div></div>", unsafe_allow_html=True)
        with col2:
            st.write(f"{st.session_state.opponent}: {st.session_state.p2_hp} HP")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.p2_hp}%; background:magenta;'></div></div>", unsafe_allow_html=True)

        if st.session_state.p2_hp <= 0:
            st.success(f"VICTORY! You defeated {st.session_state.opponent}!"); add_xp(50); st.balloons()
            if st.button("New Match"): st.session_state.opponent = None; st.session_state.p1_hp = 100; st.session_state.p2_hp = 100; st.rerun()
        elif st.session_state.p1_hp <= 0:
            st.error("DEFEAT! Better luck next time."); 
            if st.button("New Match"): st.session_state.opponent = None; st.session_state.p1_hp = 100; st.session_state.p2_hp = 100; st.rerun()
        else:
            q = random.choice(MCQ_DATA)
            st.markdown(f"<div class='arena-box'><h4>{q['q']}</h4></div>", unsafe_allow_html=True)
            ans = st.radio("Choose Action:", q['o'], key="arena_q")
            if st.button("ATTACK 💥"):
                if ans == q['a']:
                    st.session_state.p2_hp -= 25
                    st.success("Great Shot!")
                else:
                    st.session_state.p1_hp -= 20
                    st.error(f"{st.session_state.opponent} counter-attacked!")
                time.sleep(1); st.rerun()

# --- OTHER PAGES (Wahi purana stable code) ---
elif st.session_state.page == "🏠 Home Base":
    st.markdown("<h1>COMMAND CENTER</h1>", unsafe_allow_html=True)
    c.execute("SELECT SUM(xp) FROM progress WHERE username = ?", (st.session_state.user,))
    total_xp = c.fetchone()[0] or 0
    st.write(f"### Total XP: {total_xp}")
    # ... graph logic ...

elif st.session_state.page == "🏆 Leaderboard":
    st.title("🏆 RANKINGS")
    # ... leaderboard logic ...

elif st.session_state.page == "⚙️ Settings":
    st.session_state.theme = st.color_picker("Pick Theme Color", st.session_state.theme)
