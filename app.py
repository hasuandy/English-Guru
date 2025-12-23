import streamlit as st
import sqlite3
import hashlib
from datetime import date, timedelta
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v28_final.db', check_same_thread=False)
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

# --- 3. DATASET ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"}
]

# --- 4. CSS (Wahi V27 wala Stylish Look) ---
st.set_page_config(page_title="English Guru Pro V28", page_icon="⚡", layout="centered")
st.markdown(f"""
    <style>
    .stApp {{ 
        background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 100%); 
        color: #ffffff; 
    }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px;
        border: 2px solid {st.session_state.theme}; text-align: center; margin: 10px 0px;
        box-shadow: 0 0 15px {st.session_state.theme};
    }}
    .hp-bar {{ height: 20px; border-radius: 10px; background: #333; overflow: hidden; margin: 10px 0; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease-in-out; }}
    .combo-text {{ color: #ffcc00; font-weight: bold; font-size: 20px; text-shadow: 0 0 10px #ffcc00; }}
    .stButton>button {{
        background: linear-gradient(45deg, #00dbde 0%, {st.session_state.theme} 100%);
        color: white; border-radius: 30px; font-weight: bold; width: 100%; border:none; padding:12px;
    }}
    h1, h2, h3 {{ text-shadow: 0 0 15px {st.session_state.theme}; color: {st.session_state.theme}; text-align: center; }}
    /* Login Box Styling */
    .login-box {{
        background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 20px;
        border: 1px solid {st.session_state.theme}; backdrop-filter: blur(10px);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. AUTHENTICATION LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='font-size: 3rem;'>⚡ ARENA LOGIN</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "📝 SIGN UP"])
        with tab1:
            e = st.text_input("Email")
            p = st.text_input("Password", type='password')
            if st.button("ENTER ARENA"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
                else: st.error("Wrong details, Warrior!")
        with tab2:
            ne = st.text_input("New Email")
            nu = st.text_input("Hero Name")
            np = st.text_input("Set Password", type='password')
            if st.button("CREATE HERO & ENTER"):
                if "@" in ne and len(np) > 3:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, ne
                        st.rerun()
                    except: st.error("Email already exists!")

# --- 6. MAIN APP CONTENT ---
else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"<h1>⭐ {st.session_state.user}</h1>", unsafe_allow_html=True)
        st.divider()
        page = st.radio("MISSIONS:", ["🏠 Home Base", "🎓 MCQ Academy", "⚔️ Daily Boss", "🗂️ Word Vault", "🏆 Leaderboard", "⚙️ Settings"])
        if st.button("🚪 Exit Arena"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "🏠 Home Base":
        st.markdown("<h1>COMMAND CENTER</h1>", unsafe_allow_html=True)
        # Calculate XP
        c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (st.session_state.email,))
        total_xp = c.fetchone()[0] or 0
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='metric-card'>🏆<br>TOTAL XP<h3>{total_xp}</h3></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='metric-card'>🎖️<br>RANK<h3>{'PRO' if total_xp > 500 else 'NOVICE'}</h3></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='metric-card'>🔥<br>STREAK<h3>1 Day</h3></div>", unsafe_allow_html=True)

        st.write("### 🚀 Power Level (Last 7 Days)")
        actual_dates = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
        xp_vals = [c.execute("SELECT SUM(xp) FROM progress WHERE email=? AND date=?", (st.session_state.email, d)).fetchone()[0] or 0 for d in actual_dates]
        chart_df = pd.DataFrame({"XP": xp_vals}, index=[(date.today() - timedelta(days=i)).strftime('%d %b') for i in range(6, -1, -1)])
        st.area_chart(chart_df, color=st.session_state.theme)

    elif page == "🎓 MCQ Academy":
        st.title("🎓 MCQ ACADEMY")
        q = random.choice(MCQ_DATA)
        st.markdown(f"<div class='metric-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, opt in enumerate(q['o']):
            with cols[idx%2]:
                if st.button(opt, key=f"mcq_{idx}"):
                    if opt == q['a']:
                        st.balloons()
                        c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 10))
                        conn.commit()
                        st.success("Correct! +10 XP")
                    else: st.error("Wrong!")
                    time.sleep(1); st.rerun()

    elif page == "⚔️ Daily Boss":
        st.markdown("<h1 style='color:red;'>⚔️ BOSS BATTLE</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: 
            st.write(f"🦸 {st.session_state.user}: {st.session_state.player_hp}%")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#2ecc71;'></div></div>", unsafe_allow_html=True)
        with c2: 
            st.write(f"👹 Boss: {st.session_state.boss_hp}%")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#e74c3c;'></div></div>", unsafe_allow_html=True)
        
        if st.session_state.combo > 1:
            st.markdown(f"<p class='combo-text'>🔥 COMBO X{st.session_state.combo}!</p>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS KILLED! +100 XP")
            c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            if st.button("Next Challenger?"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.session_state.combo = 0; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("YOU DIED!"); 
            if st.button("Revive"): st.session_state.player_hp = 100; st.session_state.boss_hp = 100; st.session_state.combo = 0; st.rerun()
        else:
            q = random.choice(MCQ_DATA)
            st.write(f"### CHALLENGE: {q['q']}")
            ans = st.radio("Select Weapon:", q['o'], key="boss_atk")
            if st.button("💥 HIT BOSS"):
                if ans == q['a']:
                    st.session_state.combo += 1
                    dmg = 25 * st.session_state.combo
                    st.session_state.boss_hp -= dmg
                    st.session_state.battle_log = f"CRITICAL! You dealt {dmg} damage!"
                else:
                    st.session_state.combo = 0
                    st.session_state.player_hp -= 20
                    st.session_state.battle_log = "MISSED! Boss hit you for 20 damage!"
                st.rerun()
        st.info(st.session_state.battle_log)

    elif page == "🗂️ Word Vault":
        st.title("🗂️ WORD VAULT")
        w = st.text_input("Word")
        m = st.text_input("Meaning")
        if st.button("💾 Save Word"):
            if w and m:
                c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                conn.commit(); st.rerun()
        
        rows = c.execute("SELECT word, meaning FROM dictionary WHERE email=?", (st.session_state.email,)).fetchall()
        for r in rows: st.markdown(f"<div class='metric-card'>{r[0]} : {r[1]}</div>", unsafe_allow_html=True)

    elif page == "🏆 Leaderboard":
        st.title("🏆 TOP WARRIORS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🎖️"
            st.markdown(f"<div class='metric-card'><h3>{rank} {row[0]}</h3><p>{row[1]} XP</p></div>", unsafe_allow_html=True)

    elif page == "⚙️ Settings":
        st.title("⚙️ CUSTOMIZE")
        st.session_state.theme = st.color_picker("Change Glow Color", st.session_state.theme)
        st.write("Theme will update on next interaction!")
