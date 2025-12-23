import streamlit as st
import sqlite3
import hashlib
from datetime import date, datetime, timedelta
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro_v29.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"
if 'combo' not in st.session_state: st.session_state.combo = 0

MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"},
    {"q": "Meaning of 'GIGANTIC'?", "o": ["Small", "Tiny", "Huge", "Thin"], "a": "Huge"}
]

# --- 3. HELPER FUNCTIONS ---
def get_streak(email):
    dates = [row[0] for row in c.execute("SELECT DISTINCT date FROM progress WHERE email=? ORDER BY date DESC", (email,)).fetchall()]
    streak = 0
    today = date.today()
    for i in range(len(dates)):
        expected = (today - timedelta(days=i)).isoformat()
        if dates[i] == expected: streak += 1
        else: break
    return streak

# --- 4. CSS ---
st.set_page_config(page_title="English Guru V29", page_icon="🎮", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: #ffffff; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255, 255, 255, 0.05); border: 2px solid {st.session_state.theme}; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 0 15px {st.session_state.theme}44; margin-bottom: 10px; }}
    .hp-bar {{ height: 20px; border-radius: 10px; background: #111; border: 1px solid #444; overflow: hidden; margin-top: 5px; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. AUTH / LOGOUT ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; color:#00f2ff;'>ARENA V29</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        tab1, tab2 = st.tabs(["🔥 LOGIN", "💎 SIGNUP"])
        with tab1:
            e = st.text_input("Email")
            p = st.text_input("Password", type='password')
            if st.button("START BATTLE"):
                h = hashlib.sha256(p.encode()).hexdigest()
                res = c.execute('SELECT password, username FROM users WHERE email=?', (e,)).fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
        with tab2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Hero Name"), st.text_input("Set Key", type='password')
            if st.button("CREATE ACCOUNT"):
                if "@" in ne:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, ne
                        st.rerun()
                    except: st.error("User exists!")

else:
    with st.sidebar:
        st.markdown(f"## 🛡️ {st.session_state.user}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🗂️ Word Vault", "🏆 Leaderboard"])
        if st.button("EXIT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- 🏠 BASE (DASHBOARD WITH STREAKS & CHART) ---
    if page == "🏠 Base":
        st.markdown("<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        txp = c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,)).fetchone()[0] or 0
        streak = get_streak(st.session_state.email)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f"<div class='gaming-card'>🏆 TOTAL XP<br><h2>{txp}</h2></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='gaming-card'>🔥 STREAK<br><h2>{streak} Days</h2></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='gaming-card'>🎖️ RANK<br><h2>{'LEGEND' if txp > 500 else 'WARRIOR'}</h2></div>", unsafe_allow_html=True)
        with col4: st.markdown(f"<div class='gaming-card'>⚡ LEVEL<br><h2>{1 + (txp // 100)}</h2></div>", unsafe_allow_html=True)

        st.subheader("📈 XP Progress History")
        history = c.execute("SELECT date, SUM(xp) FROM progress WHERE email=? GROUP BY date ORDER BY date ASC", (st.session_state.email,)).fetchall()
        if history:
            df = pd.DataFrame(history, columns=['Date', 'XP'])
            st.area_chart(df.set_index('Date'))
        else:
            st.info("No battles fought yet. Go to Training!")

    # --- ⚔️ BOSS BATTLE (FIXED WITH FORM) ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS BATTLE</h1>", unsafe_allow_html=True)
        
        cp, cb = st.columns(2)
        cp.markdown(f"**HERO: {st.session_state.player_hp}%**")
        cp.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        cb.markdown(f"**BOSS: {st.session_state.boss_hp}%**")
        cb.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS DESTROYED! +100 XP")
            c.execute("INSERT INTO progress VALUES (?, ?, 100)", (st.session_state.email, str(date.today()))); conn.commit()
            if st.button("NEXT BOSS"): 
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.combo = 100, 100, 0
                st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("YOU DIED!"); 
            if st.button("REVIVE"): 
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.combo = 100, 100, 0
                st.rerun()
        else:
            q = random.choice(MCQ_DATA)
            with st.form("battle_form"):
                st.markdown(f"<div class='gaming-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
                ans = st.radio("SELECT WEAPON:", q['o'], horizontal=True)
                if st.form_submit_button("💥 ATTACK"):
                    if ans == q['a']:
                        st.session_state.combo += 1
                        dmg = 20 * st.session_state.combo
                        st.session_state.boss_hp -= dmg
                        st.session_state.battle_log = f"🔥 COMBO X{st.session_state.combo}! Dealt {dmg} DMG!"
                    else:
                        st.session_state.combo = 0
                        st.session_state.player_hp -= 25
                        st.session_state.battle_log = "⚠️ MISSED! Boss hit you for 25 DMG!"
                    st.rerun()
        st.info(st.session_state.battle_log)

    # --- TRAINING & OTHERS (Existing Logic) ---
    elif page == "🎓 Training":
        st.markdown("<h1 style='font-family:Bungee;'>TRAINING</h1>", unsafe_allow_html=True)
        q = random.choice(MCQ_DATA)
        st.markdown(f"<div class='gaming-card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            if cols[i%2].button(opt, key=f"t_{i}_{time.time()}"):
                if opt == q['a']:
                    c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today()))); conn.commit()
                    st.success("Correct! +10 XP"); time.sleep(0.5); st.rerun()
                else: st.error("Wrong!")

    elif page == "🗂️ Word Vault":
        st.title("🗂️ VAULT")
        w, m = st.text_input("Word"), st.text_input("Meaning")
        if st.button("SAVE"):
            c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m)); conn.commit()
        
        vault_data = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        if vault_data:
            st.table(pd.DataFrame(vault_data, columns=['Word', 'Meaning']))

    elif page == "🏆 Leaderboard":
        st.title("🏆 RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.markdown(f"<div class='gaming-card' style='text-align:left;'>#{i+1} <b>{row[0]}</b> — {row[1]} XP</div>", unsafe_allow_html=True)
