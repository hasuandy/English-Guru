import streamlit as st
import sqlite3
import hashlib
from datetime import date, timedelta
import pandas as pd
import random
import time

# --- DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, xp INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS progress(username TEXT, date TEXT, xp_gained INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS dictionary(username TEXT, word TEXT, meaning TEXT)')
conn.commit()

# --- UTILS ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

def add_xp(user, amount):
    c.execute("UPDATE users SET xp = xp + ? WHERE username = ?", (amount, user))
    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (user, str(date.today()), amount))
    conn.commit()

# --- SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# --- UI DESIGN ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

# --- LOGIN / SIGNUP SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🛡️ ENGLISH GURU PORTAL</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        u1 = st.text_input("Username", key="l1")
        p1 = st.text_input("Password", type='password', key="l2")
        if st.button("ENTER ARENA"):
            c.execute('SELECT password FROM users WHERE username =?', (u1,))
            data = c.fetchone()
            if data and check_hashes(p1, data[0]):
                st.session_state.logged_in = True
                st.session_state.user = u1
                st.rerun()
            else: st.error("Wrong details!")

    with tab2:
        new_u = st.text_input("New Username")
        new_p = st.text_input("New Password", type='password')
        invite = st.text_input("Secret Invite Code (Verification)")
        if st.button("REGISTER"):
            if invite == "GURU77": # Ye aapka verification code hai
                try:
                    c.execute('INSERT INTO users VALUES (?,?,?)', (new_u, make_hashes(new_p), 0))
                    conn.commit()
                    st.success("Account Created! Now Login.")
                except: st.error("Username already taken!")
            else: st.error("Invalid Invite Code!")

else:
    # --- MAIN DASHBOARD ---
    st.sidebar.title(f"👤 {st.session_state.user}")
    page = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🎓 MCQ Academy", "⚔️ Boss Battle", "🗂️ Word Vault"])
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- HOME DASHBOARD ---
    if page == "🏠 Dashboard":
        st.title("🚀 Your Progress")
        c.execute("SELECT xp FROM users WHERE username=?", (st.session_state.user,))
        total_xp = c.fetchone()[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total XP", total_xp)
        col2.metric("Rank", "Warrior" if total_xp < 500 else "Elite")
        col3.metric("Status", "Active 🔥")

        # XP Chart
        st.write("### Weekly Growth")
        chart_data = pd.DataFrame({"XP": [random.randint(10, 50) for _ in range(7)]})
        st.area_chart(chart_data)

    # --- MCQ GAME ---
    elif page == "🎓 MCQ Academy":
        st.title("🎓 MCQ Training")
        questions = [
            {"q": "Antonym of 'Fast'?", "o": ["Slow", "Quick", "Rapid"], "a": "Slow"},
            {"q": "Past of 'Go'?", "o": ["Gone", "Went", "Goes"], "a": "Went"}
        ]
        q = random.choice(questions)
        st.info(q['q'])
        ans = st.radio("Select Answer:", q['o'])
        if st.button("Submit"):
            if ans == q['a']:
                st.success("Correct! +10 XP")
                add_xp(st.session_state.user, 10)
                time.sleep(1); st.rerun()
            else: st.error("Wrong! Try again.")

    # --- BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.title("⚔️ Monster Fight")
        col1, col2 = st.columns(2)
        col1.progress(st.session_state.player_hp / 100, text=f"Your HP: {st.session_state.player_hp}")
        col2.progress(st.session_state.boss_hp / 100, text=f"Boss HP: {st.session_state.boss_hp}")
        
        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("Victory! You earned 100 XP")
            add_xp(st.session_state.user, 100)
            if st.button("Reset Fight"): st.session_state.boss_hp=100; st.rerun()
        else:
            if st.button("💥 Attack Boss"):
                st.session_state.boss_hp -= 20
                st.session_state.player_hp -= 10
                st.rerun()

    # --- WORD VAULT ---
    elif page == "🗂️ Word Vault":
        st.title("🗂️ Personal Dictionary")
        w = st.text_input("Word")
        m = st.text_input("Meaning")
        if st.button("Save"):
            c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.user, w, m))
            conn.commit(); st.success("Saved!")
        
        data = c.execute("SELECT word, meaning FROM dictionary WHERE username=?", (st.session_state.user,)).fetchall()
        st.table(pd.DataFrame(data, columns=["Word", "Meaning"]))
