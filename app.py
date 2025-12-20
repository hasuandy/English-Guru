import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "📊 Dashboard"

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. PREMIUM UI ---
st.set_page_config(page_title="English Guru", page_icon="🎓", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    .stApp { background: #050505; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    
    .brand-title {
        font-family: 'Bungee', cursive;
        font-size: 5rem; text-align: center;
        background: linear-gradient(90deg, #ffd700, #00f2ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: -50px;
    }

    .cyber-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center; margin-bottom: 20px;
    }

    .hint-box {
        background: rgba(255, 215, 0, 0.1);
        border-left: 5px solid #ffd700;
        padding: 10px; margin: 10px 0; border-radius: 5px;
        color: #ffd700; font-style: italic;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ffd700, #ff8c00) !important;
        color: black !important; font-family: 'Bungee' !important;
        border-radius: 12px !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 ACCESS", "🛡️ JOIN"])
        with t1:
            e = st.text_input("Email")
            p = st.text_input("Key", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
        with t2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Name"), st.text_input("Set Key", type='password')
            if st.button("CREATE HERO"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                conn.commit(); st.balloons(); st.success("Created!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ffd700; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("MISSION SELECT", ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🎧 Hub", "🗣️ Speaking"], key="nav_key", on_change=set_page)
        if st.button("LOGOUT"): st.session_state.logged_in = False; st.rerun()

    page = st.session_state.user_page
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

    if page == "📊 Dashboard":
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        xp = c.fetchone()[0] or 0
        st.markdown(f"<div class='cyber-card'><h2>YOUR CURRENT XP: <span style='color:#ffd700;'>{xp}</span></h2></div>", unsafe_allow_html=True)
        st.progress(min((xp % 100)/100, 1.0))

    elif page == "📚 Vocab Vault":
        st.markdown("<div class='cyber-card'><h2>Word: 'Lethargic'</h2><p>Guess the meaning!</p></div>", unsafe_allow_html=True)
        if st.checkbox("💡 Get Hint"):
            st.markdown("<div class='hint-box'>Think of how you feel when you haven't slept for 24 hours... very slow and tired.</div>", unsafe_allow_html=True)
        
        ans = st.text_input("Enter Meaning:")
        if st.button("VERIFY"):
            if "lazy" in ans.lower() or "tired" in ans.lower():
                st.success("Correct! +10 XP")
                c.execute("INSERT INTO progress VALUES (?,?,?,?)", (st.session_state.email, str(date.today()), 10, "Vocab"))
                conn.commit(); time.sleep(1); st.rerun()

    elif page == "✍️ Grammar Lab":
        st.markdown("<div class='cyber-card'><h3>'Neither of the two books ____ (is/are) interesting.'</h3></div>", unsafe_allow_html=True)
        if st.checkbox("💡 Get Hint"):
            st.markdown("<div class='hint-box'>Clue: 'Neither' is always treated as Singular in formal English.</div>", unsafe_allow_html=True)
        
        ans = st.text_input("Your Answer:")
        if st.button("STRIKE"):
            if ans.lower().strip() == "is":
                st.balloons(); st.success("Masterful! +20 XP")
                c.execute("INSERT INTO progress VALUES (?,?,?,?)", (st.session_state.email, str(date.today()), 20, "Grammar"))
                conn.commit(); time.sleep(1); st.rerun()
            else: st.error("Incorrect. Try using the hint!")

    elif page == "🎧 Hub":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.info("Listen and repeat the lyrics to improve flow.")
