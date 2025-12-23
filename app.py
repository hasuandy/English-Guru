import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import random
import time

# --- 1. UI CONFIG (Wahi Purana Gaming Look) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    /* Full Page Gaming Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://wallpaperaccess.com/full/2565415.jpg');
        background-size: cover;
        background-position: center;
        color: #ffffff;
    }
    
    /* Neon Glow Cards (Pehle Jaisa Look) */
    .metric-card {
        background: rgba(0, 242, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 20px #00f2ff;
        text-align: center;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 35px #00f2ff;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #00f2ff;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff);
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        box-shadow: 0 0 15px #7000ff;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_final.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, xp INTEGER)')
conn.commit()

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 4. LOGIN / SIGNUP UI ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #00f2ff; text-shadow: 0 0 25px #00f2ff;'>🛡️ ENGLISH GURU ARENA</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        tab1, tab2 = st.tabs(["⚡ LOGIN", "📝 JOIN GUILD"])
        
        with tab1:
            u = st.text_input("Hero Name")
            p = st.text_input("Secret Key", type='password')
            if st.button("START MISSION"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password FROM users WHERE username=?', (u,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Wrong Key! Try Again.")
        
        with tab2:
            nu = st.text_input("Choose Hero Name")
            np = st.text_input("Create Secret Key", type='password')
            inv = st.text_input("Verification Code")
            if st.button("REGISTER HERO"):
                if inv == "GURU77":
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,0)', (nu, h))
                        conn.commit()
                        st.success("Hero Registered! Now Login.")
                    except: st.error("Name already taken!")
                else: st.warning("Hint: Verification Code is GURU77")

# --- 5. MAIN APP (After Login) ---
else:
    st.sidebar.markdown(f"<h2 style='color:#00f2ff;'>👤 {st.session_state.user}</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("Navigation", ["🏠 Home Base", "🎓 MCQ Training", "⚔️ Boss Battle"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "🏠 Home Base":
        st.markdown(f"<h2 style='color: #00f2ff;'>Welcome back, Warrior!</h2>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-card'>🏆 TOTAL XP<br><h2>850</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'>🎖️ RANK<br><h2>ELITE</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'>🔥 STREAK<br><h2>7 DAYS</h2></div>", unsafe_allow_html=True)
        
        st.write("### 📈 Level Progress")
        st.area_chart(pd.DataFrame([20, 45, 30, 70, 90], columns=['XP']))

    elif page == "🎓 MCQ Training":
        st.title("🎯 Academy")
        st.info("Identify the Correct Synonym for 'GENEROUS':")
        if st.button("Kind"): 
            st.balloons()
            st.success("Brilliant! +10 XP")
        if st.button("Selfish"): 
            st.error("Incorrect! Try again.")

    elif page == "⚔️ Boss Battle":
        st.title("⚔️ Final Boss Fight")
        st.progress(0.6, text="Boss HP: 60%")
        if st.button("💥 USE SPECIAL ATTACK"):
            st.snow()
            st.success("Critical Hit!")
