import streamlit as st
import sqlite3
import hashlib
from datetime import date, datetime, timedelta
import random
import time

# --- 1. DATABASE & ARCHITECTURE ---
conn = sqlite3.connect('english_guru_v42.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER, level TEXT, daily_goal INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- 3. HIGH-ENERGY CYBER CSS ---
st.set_page_config(page_title="English Guru Pro", page_icon="🎓", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@400;700&family=Rajdhani:wght@600&display=swap');
    
    .stApp { 
        background: #050505;
        background-image: radial-gradient(circle at 20% 30%, #1a1a2e 0%, #050505 100%);
        color: #00f2ff; font-family: 'Rajdhani', sans-serif;
    }
    
    /* Neon Branding */
    .brand-title {
        font-family: 'Bungee', cursive;
        color: #ff00ff;
        font-size: 4.5rem;
        text-align: center;
        text-shadow: 0 0 15px #ff00ff, 0 0 30px #00f2ff;
        margin-top: -40px;
    }

    .cyber-card {
        background: rgba(10, 10, 20, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 20px; padding: 30px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        margin-bottom: 25px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .cyber-card:hover { 
        border-color: #ff00ff; 
        transform: translateY(-8px);
        box-shadow: 0 0 40px rgba(255, 0, 255, 0.4);
    }

    /* Animated Gaming Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important; font-family: 'Orbitron', sans-serif !important;
        border: none !important; border-radius: 10px !important;
        padding: 15px 30px !important; font-weight: bold !important;
        width: 100%; letter-spacing: 2px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 50px #00f2ff !important;
        transform: scale(1.02);
    }

    /* Custom Progress Bar */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff00ff, #00f2ff) !important;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. CORE FUNCTIONS ---
def add_xp(amount, cat):
    c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), amount, cat))
    conn.commit()

# --- 5. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1,1.5,1])
    with col2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        tab = st.tabs(["⚡ ACCESS PORTAL", "🛠️ NEW RECRUIT"])
        with tab[0]:
            e = st.text_input("Warrior Email")
            p = st.text_input("Secret Key", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with tab[1]:
            ne, nu, np = st.text_input("New Email"), st.text_input("Codename"), st.text_input("Passkey", type='password')
            if st.button("CREATE PROFILE"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0,"Scout",100)', (ne, nu, h))
                conn.commit(); st.balloons(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Fetch User XP
    c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
    xp_data = c.fetchone()
    current_xp = xp_data[0] if xp_data and xp_data[0] else 0

    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff00ff; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.markdown(f"**XP:** `{current_xp}` | **LVL:** `{1 + current_xp//100}`")
        page = st.selectbox("MISSION SELECT", ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🗣️ Speaking Hub"])
        if st.button("ABORT MISSION"): st.session_state.logged_in = False; st.rerun()

    # --- DASHBOARD ---
    if page == "📊 Dashboard":
        st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='cyber-card'><h3>🏆 XP</h3><h2>{current_xp}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='cyber-card'><h3>🎖️ RANK</h3><h2>{'ELITE' if current_xp > 500 else 'SCOUT'}</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='cyber-card'><h3>🔥 STREAK</h3><h2>5 DAYS</h2></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='cyber-card'><h3>Evolution Progress</h3>", unsafe_allow_html=True)
        st.progress(min((current_xp % 100)/100, 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

    # --- VOCAB VAULT ---
    elif page == "📚 Vocab Vault":
        st.markdown("<h1>VOCABULARY VAULT</h1>", unsafe_allow_html=True)
        word = {"w": "Resilient", "m": "Able to withstand or recover quickly from difficult conditions."}
        st.markdown(f"<div class='cyber-card'><h1 style='text-align:center; font-size:4rem; color:#00f2ff;'>{word['w']}</h1></div>", unsafe_allow_html=True)
        if st.button("⚡ SCAN INTEL"):
            st.markdown(f"<div class='cyber-card'><h3>Meaning:</h3><p style='font-size:1.4rem;'>{word['m']}</p></div>", unsafe_allow_html=True)
            add_xp(10, "Vocab"); st.toast("XP GAINED!", icon="🔥")

    # --- GRAMMAR LAB ---
    elif page == "✍️ Grammar Lab":
        st.markdown("<h1>GRAMMAR CORE</h1>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h3>Mission: Identify Correct Verb</h3><p>She ____ (finish/finishes) her work on time.</p></div>", unsafe_allow_html=True)
        ans = st.text_input("Enter Answer:")
        if st.button("💥 EXECUTE STRIKE"):
            if ans.lower().strip() == "finishes":
                st.balloons(); st.success("CRITICAL HIT! +20 XP"); add_xp(20, "Grammar")
            else: st.error("MISSED! Try again.")

    # --- SPEAKING HUB ---
    elif page == "🗣️ Speaking Hub":
        st.markdown("<h1>VOCAL INTERFACE</h1>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h4>Mission: Pronunciation Check</h4><p>Say: 'Technological advancements are inevitable.'</p></div>", unsafe_allow_html=True)
        if st.button("🎙️ ACTIVATE SENSORS"):
            with st.spinner("Analyzing Vocal Patterns..."):
                time.sleep(2)
                st.info("Accuracy: 94%. You are a natural, Warrior.")
                add_xp(30, "Speaking")
