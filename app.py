import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import random

# --- 1. UI CONFIG (Cyberpunk Look) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    /* Premium Gaming Background */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1542751371-adc38448a05e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Transparent Glass Login Box */
    [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(0, 242, 255, 0.4);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    .glow-header {
        color: #00f2ff;
        text-shadow: 0 0 15px #00f2ff, 0 0 30px #0072ff;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        margin-bottom: 30px;
    }

    /* Glow Cards for Dashboard */
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
        padding: 12px;
        font-weight: bold;
        text-transform: uppercase;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE SETUP ---
conn = sqlite3.connect('guru_final_v7.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)')
conn.commit()

# --- 3. LOGIN / SIGNUP LOGIC ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 class='glow-header'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.8,1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "📝 SIGN UP"])
        
        with tab1:
            email_log = st.text_input("Email", placeholder="example@mail.com")
            pass_log = st.text_input("Password", type='password', placeholder="••••••••")
            if st.button("ENTER PORTAL"):
                h = hashlib.sha256(pass_log.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (email_log,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in = True
                    st.session_state.user = res[1]
                    st.rerun()
                else: st.error("Wrong Email or Password!")
        
        with tab2:
            new_email = st.text_input("Your Email")
            new_user = st.text_input("Username (Hero Name)")
            new_pass = st.text_input("Create Password", type='password')
            
            if st.button("CREATE ACCOUNT"):
                if "@" in new_email and "." in new_email:
                    h = hashlib.sha256(new_pass.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (new_email, new_user, h))
                        conn.commit()
                        st.success("Account Created! Now go to LOGIN tab.")
                    except: st.error("This Email is already in our database!")
                else:
                    st.warning("Please enter a valid email address.")

# --- 4. MAIN DASHBOARD ---
else:
    st.sidebar.markdown(f"<h2 style='color:#00f2ff;'>🛡️ Warrior: {st.session_state.user}</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("Arena Menu", ["🏠 Dashboard", "🎯 Battle Zone"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "🏠 Dashboard":
        st.markdown(f"<h2 style='color: #00f2ff;'>Welcome back, {st.session_state.user}!</h2>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-card'>🏆 TOTAL XP<br><h2>1,200</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'>🎖️ RANK<br><h2>ELITE</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'>🔥 STREAK<br><h2>15 DAYS</h2></div>", unsafe_allow_html=True)
        
        st.write("### 📈 Your Progress Graph")
        st.line_chart(pd.DataFrame([10, 35, 20, 80, 100], columns=['XP']))

    elif page == "🎯 Battle Zone":
        st.title("🎯 Training Ground")
        st.info("Guess the Synonym of 'HAPPY':")
        if st.button("Joyful"): 
            st.balloons()
            st.success("Correct! +10 XP")
        if st.button("Sad"): st.error("Wrong! Try again.")
