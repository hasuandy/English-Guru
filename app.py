import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import random
import time

# --- 1. UI CONFIG (Cyberpunk Glassmorphism) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    /* Premium Gaming Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1542751371-adc38448a05e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Transparent Glass Login Box */
    [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 45px;
        border: 1px solid rgba(0, 242, 255, 0.4);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Glow Heading */
    .glow-header {
        color: #00f2ff;
        text-shadow: 0 0 15px #00f2ff, 0 0 30px #0072ff;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin-bottom: 20px;
    }

    /* Pehle Wale Glow Cards for Dashboard */
    .metric-card {
        background: rgba(0, 242, 255, 0.1);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 20px #00f2ff;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Buttons Style */
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: bold;
        text-transform: uppercase;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
        width: 100%;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 25px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v5.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, xp INTEGER)')
conn.commit()

# --- 3. LOGIN / SIGNUP LOGIC ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 class='glow-header'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.8,1])
    with col2:
        tab1, tab2 = st.tabs(["⚡ ENTER PORTAL", "📝 CREATE HERO"])
        
        with tab1:
            u = st.text_input("Hero Name", placeholder="Username...")
            p = st.text_input("Secret Key", type='password', placeholder="Password...")
            if st.button("INITIALIZE MISSION"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password FROM users WHERE username=?', (u,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else: st.error("❌ Authentication Failed!")
        
        with tab2:
            nu = st.text_input("New Hero Name")
            np = st.text_input("New Secret Key", type='password')
            inv = st.text_input("Verification Code (GURU77)")
            if st.button("REGISTER HERO"):
                if inv == "GURU77":
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,0)', (nu, h))
                        conn.commit()
                        st.success("✅ Hero Created! Now Login.")
                    except: st.error("⚠️ Name already exists!")
                else: st.warning("Need Invite Code: GURU77")

# --- 4. MAIN DASHBOARD ---
else:
    st.sidebar.markdown(f"<h2 style='color:#00f2ff;'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("Arena Menu", ["🏠 Dashboard", "🎯 MCQ Battle", "⚔️ Boss Battle"])
    
    if st.sidebar.button("Exit Portal"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "🏠 Dashboard":
        st.markdown(f"<h2 style='color: #00f2ff;'>Welcome back, Warrior {st.session_state.user}!</h2>", unsafe_allow_html=True)
        
        # Glow Cards
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-card'>🏆 TOTAL XP<br><h2>1,050</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'>🎖️ RANK<br><h2>ELITE</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'>🔥 STREAK<br><h2>12 DAYS</h2></div>", unsafe_allow_html=True)
        
        st.write("### 📊 Your Battle History")
        st.area_chart(pd.DataFrame([10, 30, 25, 60, 85, 120], columns=['XP']))

    elif page == "🎯 MCQ Battle":
        st.title("🎯 MCQ Training")
        st.info("Pick the correct synonym for 'VIBRANT':")
        if st.button("Energetic"): 
            st.balloons()
            st.success("Power Up! +10 XP")
        if st.button("Dull"): st.error("Shield Broken! Try again.")
