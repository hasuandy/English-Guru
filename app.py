import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro_v3.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER, goal INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "📊 Dashboard"

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. PREMIUM UI CSS ---
st.set_page_config(page_title="English Guru", page_icon="🎓", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background: #050505; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }
    .brand-title {
        font-family: 'Bungee', cursive; font-size: 5rem; text-align: center;
        background: linear-gradient(90deg, #ffd700, #00f2ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: -50px;
    }
    .cyber-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 20px; padding: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px; text-align: center;
    }
    .hint-box {
        background: rgba(255, 215, 0, 0.1); border-left: 5px solid #ffd700;
        padding: 10px; color: #ffd700; border-radius: 5px; margin: 10px 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ffd700, #ff8c00) !important;
        color: black !important; font-family: 'Bungee' !important; border-radius: 12px !important;
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
            e = st.text_input("Warrior Email")
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
                c.execute('INSERT INTO users (email, username, password, xp, goal) VALUES (?,?,?,0,50)', (ne, nu, h))
                conn.commit(); st.balloons(); st.success("Created!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Navigation
    with st.sidebar:
        st.markdown(f"<h1 style='color:#ffd700; font-family:Bungee;'>🛡️ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.selectbox("MISSION SELECT", 
                     ["📊 Dashboard", "📚 Vocab Vault", "✍️ Grammar Lab", "🎧 Audio Hub", "⚙️ Settings"], 
                     key="nav_key", on_change=set_page)
        st.write("---")
        if st.button("LOGOUT"): st.session_state.logged_in = False; st.rerun()

    page = st.session_state.user_page
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

    # Global Data Fetch
    c.execute("SELECT xp, username, goal FROM users WHERE email=?", (st.session_state.email,))
    user_info = c.fetchone()
    current_xp = user_info[0] or 0
    current_name = user_info[1]
    current_goal = user_info[2] or 50

    if page == "📊 Dashboard":
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"<div class='cyber-card'><h3>🏆 XP</h3><h1 style='color:#ffd700;'>{current_xp}</h1></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='cyber-card'><h3>🎯 GOAL</h3><h1 style='color:#00f2ff;'>{current_goal}</h1></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='cyber-card'><h3>🎖️ RANK</h3><h1 style='color:#ff00ff;'>{'PRO' if current_xp > 100 else 'NOOB'}</h1></div>", unsafe_allow_html=True)
        st.markdown("<div class='cyber-card'><h3>DAILY PROGRESS</h3>", unsafe_allow_html=True)
        st.progress(min(current_xp/current_goal, 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "📚 Vocab Vault":
        st.markdown("<div class='cyber-card'><h2>Word: 'Eloquent'</h2><p>Guess the meaning!</p></div>", unsafe_allow_html=True)
        if st.checkbox("💡 Get Hint"):
            st.markdown("<div class='hint-box'>Hint: Think of someone who speaks very smoothly and beautifully, like a great leader.</div>", unsafe_allow_html=True)
        ans = st.text_input("Your Answer:")
        if st.button("VERIFY"):
            if "fluent" in ans.lower() or "clear" in ans.lower():
                st.balloons(); c.execute("INSERT INTO progress VALUES (?,?,?,?)", (st.session_state.email, str(date.today()), 10, "Vocab"))
                c.execute("UPDATE users SET xp = xp + 10 WHERE email=?", (st.session_state.email,))
                conn.commit(); st.success("Correct! +10 XP"); time.sleep(1); st.rerun()

    elif page == "✍️ Grammar Lab":
        st.markdown("<div class='cyber-card'><h3>'He ____ (don't/doesn't) like pizza.'</h3></div>", unsafe_allow_html=True)
        if st.checkbox("💡 Get Hint"):
            st.markdown("<div class='hint-box'>Hint: Third person singular (He/She/It) always takes 'doesn't'.</div>", unsafe_allow_html=True)
        ans = st.text_input("Correction:")
        if st.button("SUBMIT"):
            if ans.lower().strip() == "doesn't":
                c.execute("INSERT INTO progress VALUES (?,?,?,?)", (st.session_state.email, str(date.today()), 20, "Grammar"))
                c.execute("UPDATE users SET xp = xp + 20 WHERE email=?", (st.session_state.email,))
                conn.commit(); st.success("Masterful! +20 XP"); time.sleep(1); st.rerun()

    elif page == "🎧 Audio Hub":
        st.markdown("<div class='cyber-card'><h3>Neural Audio Feed</h3>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "⚙️ Settings":
        st.markdown("<h2 style='text-align:center;'>CONTROL CENTER</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
            new_name = st.text_input("Update Codename", value=current_name)
            new_goal = st.number_input("Set Daily XP Goal", value=current_goal, step=10)
            
            if st.button("💾 SAVE CONFIGURATION"):
                c.execute("UPDATE users SET username=?, goal=? WHERE email=?", (new_name, new_goal, st.session_state.email))
                conn.commit()
                st.session_state.user = new_name
                st.success("System Updated Successfully!")
                time.sleep(1)
                st.rerun()
            
            st.write("---")
            st.write(f"Warrior Email: {st.session_state.email}")
            st.markdown("</div>", unsafe_allow_html=True)
