import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import random
import time

# --- 1. UI CONFIG (V28 Arena Look) ---
st.set_page_config(page_title="English Guru: Arena Edition (V28)", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1542751371-adc38448a05e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* V28 Glassmorphism Interface */
    [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        border: 2px solid rgba(0, 242, 255, 0.4);
        box-shadow: 0 0 30px rgba(0, 0, 0, 1);
    }

    .v28-header {
        color: #00f2ff;
        text-shadow: 0 0 20px #00f2ff, 0 0 40px #0072ff;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900;
        letter-spacing: 3px;
    }

    .metric-card {
        background: rgba(0, 242, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 20px #00f2ff;
        text-align: center;
    }

    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        color: white !important;
        border-radius: 15px;
        border: none;
        padding: 12px;
        font-weight: bold;
        text-transform: uppercase;
        width: 100%;
        transition: 0.4s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v28.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS dictionary(email TEXT, word TEXT, meaning TEXT)')
conn.commit()

# --- 3. AUTO-LOGIN LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 4. AUTHENTICATION (Login/Signup) ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='v28-header'>ENGLISH GURU: V28</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1.8,1])
    with col2:
        tab1, tab2 = st.tabs(["⚡ ACCESS PORTAL", "📝 CREATE HERO"])
        
        with tab1:
            email_log = st.text_input("Email")
            pass_log = st.text_input("Password", type='password')
            if st.button("INITIALIZE MISSION"):
                h = hashlib.sha256(pass_log.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (email_log,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in = True
                    st.session_state.user = res[1]
                    st.session_state.email = email_log
                    st.rerun()
                else: st.error("❌ Identification Failed!")
        
        with tab2:
            new_email = st.text_input("Enter Email")
            new_user = st.text_input("Hero Name (Display)")
            new_pass = st.text_input("Set Key (Password)", type='password')
            
            if st.button("REGISTER & ENTER"):
                if "@" in new_email and "." in new_email:
                    h = hashlib.sha256(new_pass.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (new_email, new_user, h))
                        conn.commit()
                        # AUTO-LOGIN AFTER SIGNUP
                        st.session_state.logged_in = True
                        st.session_state.user = new_user
                        st.session_state.email = new_email
                        st.success("✅ Welcome Hero! Arena Loaded.")
                        time.sleep(1)
                        st.rerun()
                    except: st.error("⚠️ Email already registered!")
                else: st.warning("Please enter a valid email.")

# --- 5. MAIN V28 ARENA (All Options Added) ---
else:
    st.sidebar.markdown(f"<h2 style='color:#00f2ff;'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
    page = st.sidebar.radio("Arena Menu", ["🏠 Dashboard", "🎯 Battle Training", "⚔️ Boss Battle", "🗂️ Word Vault"])
    
    if st.sidebar.button("🚪 Exit Arena"):
        st.session_state.logged_in = False
        st.rerun()

    # --- DASHBOARD ---
    if page == "🏠 Dashboard":
        st.markdown(f"<h2 style='color: #00f2ff;'>Welcome back, {st.session_state.user}!</h2>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='metric-card'>🏆 TOTAL XP<br><h2>1,450</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'>🎖️ RANK<br><h2>WARRIOR</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'>🔥 STREAK<br><h2>18 DAYS</h2></div>", unsafe_allow_html=True)
        
        st.write("### 📈 Recent Activity Progress")
        st.area_chart(pd.DataFrame([15, 40, 25, 85, 120], columns=['XP']))

    # --- MCQ BATTLE ---
    elif page == "🎯 Battle Training":
        st.title("🎯 MCQ Battle Zone")
        st.info("What is the synonym of 'BRAVE'?")
        if st.button("Valiant"): 
            st.balloons()
            st.success("Victory! +10 XP")
        if st.button("Fearful"): st.error("Shield Broken! Try again.")

    # --- BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.title("⚔️ Final Boss Fight")
        st.warning("Ancient Dragon Health: 75%")
        st.progress(0.75, text="Boss Health Bar")
        if st.button("💥 RELEASE ULTIMATE ATTACK"):
            st.snow()
            st.success("CRITICAL HIT! Boss Health reduced.")

    # --- WORD VAULT ---
    elif page == "🗂️ Word Vault":
        st.title("🗂️ Personal Word Vault")
        w = st.text_input("New Vocabulary Word")
        m = st.text_input("Meaning/Usage")
        if st.button("🔒 Save to Vault"):
            if w and m:
                c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                conn.commit()
                st.success("Word Encrypted and Saved!")
            else: st.warning("Fill both fields!")
        
        vault_data = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        if vault_data:
            st.table(pd.DataFrame(vault_data, columns=["Word", "Definition"]))
