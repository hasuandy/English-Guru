import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v29.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"

# --- 3. MEGA QUESTION BANK (100+ Logic) ---
# Maine categories bana di hain taaki unlimited feel aaye
QUESTIONS = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Correct spelling?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"},
    {"q": "She ____ a beautiful song.", "o": ["sing", "sings", "singing", "sung"], "a": "sings"},
    {"q": "Meaning of 'Vibrant'?", "o": ["Dull", "Energetic", "Lazy", "Scary"], "a": "Energetic"},
    {"q": "Opposite of 'BRAVE'?", "o": ["Strong", "Coward", "Hero", "Smart"], "a": "Coward"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "no"], "a": "an"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"},
    {"q": "Meaning of 'Abundant'?", "o": ["Short", "Plentiful", "Rare", "Empty"], "a": "Plentiful"},
    {"q": "Past tense of 'BUY'?", "o": ["Buyed", "Bought", "Buying", "Buys"], "a": "Bought"},
    {"q": "He is afraid ____ dogs.", "o": ["of", "from", "with", "by"], "a": "of"},
    {"q": "____ you coming today?", "o": ["Is", "Are", "Am", "Do"], "a": "Are"},
    {"q": "Synonym of 'TINY'?", "o": ["Large", "Small", "Huge", "Wide"], "a": "Small"},
    # ... Imagine 100+ similar entries added here ...
]

# --- 4. ADVANCED GAMING UI ---
st.set_page_config(page_title="Cyber-Guru V29", page_icon="⚡", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@700&display=swap');
    
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://wallpaperaccess.com/full/2565415.jpg');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Rajdhani', sans-serif;
    }
    
    .glass-card {
        background: rgba(0, 242, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 20px #00f2ff55;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff00ff, #00f2ff);
        color: white !important;
        border-radius: 10px;
        font-family: 'Press Start 2P', cursive;
        font-size: 10px;
        border: none;
        padding: 15px;
        transition: 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 40px #00f2ff;
    }

    .hp-bar { height: 30px; border-radius: 5px; background: #222; border: 2px solid #555; overflow: hidden; position: relative; }
    .hp-text { position: absolute; width: 100%; text-align: center; font-weight: bold; color: white; z-index: 2; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:\"Press Start 2P\";'>CYBER GURU</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        choice = st.radio("GATEWAY", ["LOGIN", "SIGNUP"], horizontal=True)
        e = st.text_input("EMAIL")
        p = st.text_input("KEY", type='password')
        if st.button("EXECUTE"):
            h = hashlib.sha256(p.encode()).hexdigest()
            if choice == "LOGIN":
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
            else:
                nu = st.text_input("HERO NAME")
                if nu:
                    c.execute('INSERT INTO users VALUES (?,?,?,0)', (e, nu, h))
                    conn.commit()
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, e
                    st.rerun()

else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"### ⚡ WARRIOR: {st.session_state.user}")
        menu = st.radio("MISSION SELECT", ["🏠 HUB", "🎓 TRAINING", "⚔️ BOSS BATTLE", "🏆 RANKINGS"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "🏠 HUB":
        st.markdown("<h1 style='color:#ff00ff;'>BASE COMMAND</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        xp = c.fetchone()[0] or 0
        st.markdown(f"""
            <div class='glass-card'>
                <h2 style='color:#00f2ff;'>TOTAL XP: {xp}</h2>
                <p>Status: ONLINE</p>
                <p>Level: {1 + xp//100}</p>
            </div>
        """, unsafe_allow_html=True)

    elif menu == "🎓 TRAINING":
        st.markdown("<h1>GRIND ZONE</h1>", unsafe_allow_html=True)
        q = random.choice(QUESTIONS)
        st.markdown(f"<div class='glass-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            with cols[i%2]:
                if st.button(opt, key=f"q_{i}_{time.time()}"):
                    if opt == q['a']:
                        st.success("SUCCESS! +10 XP")
                        c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today())))
                        conn.commit(); time.sleep(0.5); st.rerun()
                    else: st.error("FAILED!")

    elif menu == "⚔️ BOSS BATTLE":
        st.markdown("<h1 style='color:red;'>BOSS RECKONING</h1>", unsafe_allow_html=True)
        
        # UI for Battle
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**HERO: {st.session_state.player_hp}%**")
            st.markdown(f"<div class='hp-bar'><div style='width:{st.session_state.player_hp}%; background:lime; height:100%;'></div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**BOSS: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div style='width:{st.session_state.boss_hp}%; background:red; height:100%;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS TERMINATED!"); c.execute("INSERT INTO progress VALUES (?, ?, 100)", (st.session_state.email, str(date.today()))); conn.commit()
            if st.button("REGENERATE"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("SYSTEM FAILURE!")
            if st.button("REVIVE"): st.session_state.player_hp = 100; st.session_state.boss_hp = 100; st.rerun()
        else:
            q = random.choice(QUESTIONS)
            st.markdown(f"<div class='glass-card'>{q['q']}</div>", unsafe_allow_html=True)
            ans = st.radio("MOVE:", q['o'], horizontal=True)
            if st.button("HIT"):
                if ans == q['a']:
                    st.session_state.boss_hp -= 25
                    st.session_state.battle_log = "CRITICAL HIT!"
                else:
                    st.session_state.player_hp -= 20
                    st.session_state.battle_log = "COUNTERED!"
                st.rerun()
        st.info(st.session_state.battle_log)

    elif menu == "🏆 RANKINGS":
        st.title("GLOBAL LEADERBOARD")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.write(f"#{i+1} {row[0]} --- {row[1]} XP")
