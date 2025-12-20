import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v45.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

# --- 2. SESSION STATE (The Engine) ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "📊 Dashboard"

# Function to handle page change
def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. KILLER GAMING CSS ---
st.set_page_config(page_title="English Guru", page_icon="🎓", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    .stApp { background: #050505; color: #00f2ff; font-family: 'Rajdhani', sans-serif; }
    
    .brand-title {
        font-family: 'Bungee', cursive;
        color: #ff00ff; font-size: 4rem; text-align: center;
        text-shadow: 0 0 15px #ff00ff, 0 0 30px #00f2ff;
        margin-top: -30px;
    }

    .cyber-card {
        background: rgba(20, 20, 40, 0.8);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 25px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
        margin-bottom: 20px;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff) !important;
        color: white !important; font-family: 'Bungee' !important;
        border: none !important; border-radius: 10px !important;
        height: 50px; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { box-shadow: 0 0 30px #ff00ff; transform: translateY(-3px); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["⚡ LOGIN", "🛠️ SIGNUP"])
        with tab1:
            e = st.text_input("Warrior Email")
            p = st.text_input("Key", type='password')
            if st.button("INITIALIZE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT username FROM users WHERE email=? AND password=?', (e, h))
                res = c.fetchone()
                if res:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[0], e
                    st.rerun()
                else: st.error("Access Denied!")
        with tab2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Codename"), st.text_input("Passkey", type='password')
            if st.button("CREATE HERO"):
                h = hashlib.sha256(np.encode()).hexdigest()
                c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                conn.commit(); st.success("Warrior Profile Created!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- NAVIGATION SIDEBAR (The Fix) ---
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ff00ff; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        # on_change property se page switch ko force kiya
        st.selectbox(
            "CHOOSE MISSION", 
            ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🎧 Listening Hub"],
            key="nav_key",
            on_change=set_page
        )
        st.write("---")
        if st.button("EXIT ARENA"):
            st.session_state.logged_in = False
            st.rerun()

    # --- RENDER PAGES ---
    current = st.session_state.user_page

    if current == "📊 Dashboard":
        st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        xp_res = c.fetchone()
        xp = xp_res[0] if xp_res and xp_res[0] else 0
        
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='cyber-card'><h3>🏆 TOTAL XP</h3><h2 style='color:#00f2ff;'>{xp}</h2></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='cyber-card'><h3>🎖️ RANK</h3><h2 style='color:#ff00ff;'>{'ELITE' if xp > 100 else 'NOOB'}</h2></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='cyber-card'><h3>🔥 STREAK</h3><h2 style='color:#00f2ff;'>Active</h2></div>", unsafe_allow_html=True)

    elif current == "📚 Vocab Vault":
        st.markdown("<h1 style='text-align:center;'>VOCABULARY VAULT</h1>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h2>Word: 'Luminous'</h2><p>Meaning: Giving off light; bright or shining.</p></div>", unsafe_allow_html=True)
        if st.button("COLLECT 10 XP"):
            c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), 10, "Vocab"))
            conn.commit()
            st.toast("XP Collected!", icon="🔥")
            time.sleep(1)
            st.rerun()

    elif current == "✍️ Grammar Lab":
        st.markdown("<h1 style='text-align:center;'>GRAMMAR CORE</h1>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h3>Identify the Correct Form:</h3><p>They ____ (has/have) already arrived.</p></div>", unsafe_allow_html=True)
        ans = st.text_input("Enter Answer:")
        if st.button("VERIFY STRIKE"):
            if ans.lower().strip() == "have":
                st.balloons()
                c.execute("INSERT INTO progress VALUES (?, ?, ?, ?)", (st.session_state.email, str(date.today()), 20, "Grammar"))
                conn.commit()
                st.success("Correct! +20 XP")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Incorrect! System Offline.")

    elif current == "🎧 Listening Hub":
        st.markdown("<h1 style='text-align:center;'>AUDIO COMMAND</h1>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h3>Neural Audio Feed</h3>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.markdown("</div>", unsafe_allow_html=True)
