import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import random

# --- 1. UI CONFIG ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1542751371-adc38448a05e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(0, 242, 255, 0.4);
    }

    .glow-header {
        color: #00f2ff;
        text-shadow: 0 0 15px #00f2ff;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
    }

    .metric-card {
        background: rgba(0, 242, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 20px #00f2ff;
        text-align: center;
        margin-bottom: 20px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        color: white !important;
        border-radius: 12px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE SETUP ---
conn = sqlite3.connect('guru_final_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS dictionary(email TEXT, word TEXT, meaning TEXT)')
conn.commit()

# --- 3. SESSION STATE (Auto-Login Logic) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 4. AUTHENTICATION UI ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='glow-header'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.8,1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "📝 SIGN UP"])
        
        with tab1:
            email_log = st.text_input("Email")
            pass_log = st.text_input("Password", type='password')
            if st.button("ENTER PORTAL"):
                h = hashlib.sha256(pass_log.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (email_log,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in = True
                    st.session_state.user = res[1]
                    st.session_state.email = email_log
                    st.rerun()
                else: st.error("Wrong Details!")
        
        with tab2:
            new_email = st.text_input("Your Email")
            new_user = st.text_input("Username (Hero Name)")
            new_pass = st.text_input("Create Password", type='password')
            
            if st.button("CREATE & START"):
                if "@" in new_email and "." in new_email:
                    h = hashlib.sha256(new_pass.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (new_email, new_user, h))
                        conn.commit()
                        # AUTO LOGIN HERE:
                        st.session_state.logged_in = True
                        st.session_state.user = new_user
                        st.session_state.email = new_email
                        st.success("Account Created! Redirecting...")
                        st.rerun()
                    except: st.error("Email already exists!")
                else: st.warning("Invalid Email!")

# --- 5. MAIN APP (Dashboard + All Options) ---
else:
    st.sidebar.markdown(f"<h2 style='color:#00f2ff;'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("Arena Menu", ["🏠 Dashboard", "🎯 Battle Zone", "⚔️ Boss Fight", "🗂️ Word Vault"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "🏠 Dashboard":
        st.markdown(f"<h2 style='color: #00f2ff;'>Welcome, {st.session_state.user}!</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-card'>🏆 TOTAL XP<br><h2>1,200</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'>🎖️ RANK<br><h2>ELITE</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'>🔥 STREAK<br><h2>15 DAYS</h2></div>", unsafe_allow_html=True)
        st.area_chart(pd.DataFrame([10, 35, 20, 80, 100], columns=['XP']))

    elif page == "🎯 Battle Zone":
        st.title("🎯 MCQ Battle")
        st.info("Identify the Synonym of 'CURIOUS':")
        if st.button("Inquisitive"): st.balloons(); st.success("Power Up! +10 XP")
        if st.button("Lazy"): st.error("Shield Broken!")

    elif page == "⚔️ Boss Fight":
        st.title("⚔️ Boss Battle")
        st.warning("Monster Health: 100%")
        st.progress(0.7, text="Boss HP")
        if st.button("💥 SUPER ATTACK"): st.snow(); st.success("Boss Flinched!")

    elif page == "🗂️ Word Vault":
        st.title("🗂️ Your Personal Dictionary")
        word = st.text_input("New Word")
        mean = st.text_input("Meaning")
        if st.button("Save to Vault"):
            c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, word, mean))
            conn.commit()
            st.success("Saved!")
        
        data = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        if data:
            st.table(pd.DataFrame(data, columns=["Word", "Meaning"]))
