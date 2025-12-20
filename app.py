import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import random
import time

# --- 1. UI CONFIG (V28 Look & Feel) ---
st.set_page_config(page_title="English Guru: Arena V28 Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1511512578047-dfb367046420?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        color: #ffffff;
    }
    /* V28 Glass Box */
    [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(0, 242, 255, 0.4);
    }
    .metric-card {
        background: rgba(0, 242, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00f2ff;
        box-shadow: 0 0 15px #00f2ff;
        text-align: center;
    }
    .boss-box {
        background: rgba(255, 0, 0, 0.1);
        border: 2px solid #ff4b4b;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 0 20px #ff4b4b;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff);
        color: white !important;
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
conn = sqlite3.connect('arena_v28_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)')
c.execute('CREATE TABLE IF NOT EXISTS dictionary(email TEXT, word TEXT, meaning TEXT)')
conn.commit()

# --- 3. SESSION STATES ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'xp' not in st.session_state: st.session_state.xp = 0

# --- 4. QUESTIONS BANK ---
QUESTIONS = [
    {"q": "Choose the correct spelling:", "o": ["Excellent", "Exelent", "Excellant"], "a": "Excellent"},
    {"q": "Synonym of 'Abundant'?", "o": ["Plentiful", "Rare", "Scarcity"], "a": "Plentiful"},
    {"q": "Antonym of 'Vague'?", "o": ["Clear", "Blurry", "Uncertain"], "a": "Clear"},
    {"q": "I ____ working on my app.", "o": ["am", "is", "are"], "a": "am"},
    {"q": "Past of 'Buy'?", "o": ["Bought", "Buyed", "Boughted"], "a": "Bought"}
]

# --- 5. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⚔️ ARENA V28 PRO</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        t1, t2 = st.tabs(["🔑 LOGIN", "📝 JOIN GUILD"])
        with t1:
            e = st.text_input("Email")
            p = st.text_input("Password", type='password')
            if st.button("ENTER PORTAL"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password, username, xp FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email, st.session_state.xp = True, res[1], e, res[2]
                    st.rerun()
                else: st.error("Access Denied!")
        with t2:
            ne, nu, np = st.text_input("Your Email"), st.text_input("Hero Name"), st.text_input("Set Key", type='password')
            if st.button("CREATE & START"):
                if "@" in ne:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email, st.session_state.xp = True, nu, ne, 0
                        st.rerun()
                    except: st.error("Already Registered!")

# --- 6. MAIN NAVIGATION ---
else:
    st.sidebar.title(f"🛡️ {st.session_state.user}")
    menu = st.sidebar.radio("Arena Map", ["🏠 Dashboard", "🎯 Battle Zone", "⚔️ Boss Fight", "🗂️ Word Vault"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- DASHBOARD ---
    if menu == "🏠 Dashboard":
        st.title(f"Arena Status: {st.session_state.user}")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-card'>🏆 TOTAL XP<br><h2>{st.session_state.xp}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='metric-card'>🎖️ RANK<br><h2>ELITE WARRIOR</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='metric-card'>🔥 STREAK<br><h2>V28 ACTIVE</h2></div>", unsafe_allow_html=True)
        st.area_chart(pd.DataFrame([random.randint(20,80) for _ in range(7)], columns=['Battle XP']))

    # --- MCQ BATTLE ---
    elif menu == "🎯 Battle Zone":
        st.title("🎯 Battle Zone (MCQ Training)")
        # Session state for tracking current question
        if 'current_q' not in st.session_state: st.session_state.current_q = random.choice(QUESTIONS)
        
        st.subheader(st.session_state.current_q['q'])
        ans = st.radio("Pick your weapon:", st.session_state.current_q['o'], key="mcq_radio")
        
        if st.button("Submit Attack"):
            if ans == st.session_state.current_q['a']:
                st.balloons()
                st.success("Perfect Hit! +10 XP")
                st.session_state.xp += 10
                c.execute("UPDATE users SET xp = ? WHERE email = ?", (st.session_state.xp, st.session_state.email))
                conn.commit()
                st.session_state.current_q = random.choice(QUESTIONS)
                time.sleep(1)
                st.rerun()
            else: st.error("Missed! Try again.")

    # --- BOSS FIGHT ---
    elif menu == "⚔️ Boss Fight":
        st.title("⚔️ The Dark Lord Challenge")
        st.markdown("<div class='boss-box'>", unsafe_allow_html=True)
        st.header("👹 BOSS HEALTH")
        st.progress(st.session_state.boss_hp / 100)
        
        if st.session_state.boss_hp <= 0:
            st.balloons()
            st.success("🏆 VICTORY! You have conquered the Arena!")
            if st.button("Respawn Boss"): st.session_state.boss_hp = 100; st.rerun()
        else:
            # Boss Fight Logic with Questions
            if 'boss_q' not in st.session_state: st.session_state.boss_q = random.choice(QUESTIONS)
            st.info(f"**ANSWER TO ATTACK:** {st.session_state.boss_q['q']}")
            boss_ans = st.radio("Choices:", st.session_state.boss_q['o'], key="boss_radio")
            
            if st.button("💥 FIRE SUPER ATTACK"):
                if boss_ans == st.session_state.boss_q['a']:
                    st.session_state.boss_hp -= 20
                    st.snow()
                    st.success("CRITICAL HIT! Boss -20 HP")
                    st.session_state.boss_q = random.choice(QUESTIONS)
                    time.sleep(1)
                    st.rerun()
                else: st.error("Boss Deflected your attack!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- WORD VAULT ---
    elif menu == "🗂️ Word Vault":
        st.title("🗂️ Ancient Word Vault")
        w, m = st.text_input("New Word"), st.text_input("Definition")
        if st.button("Store in Vault"):
            if w and m:
                c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                conn.commit()
                st.success("Word Stored Safely!")
        
        data = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        if data: st.table(pd.DataFrame(data, columns=["Word", "Meaning"]))
