import sys
import streamlit as st
import sqlite3
from datetime import date, timedelta
import random
import time
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v27.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS progress (username TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (username TEXT, word TEXT, meaning TEXT)''')

# Dummy data for Leaderboard
dummy_users = [('Guru_Master', '2025-12-01', 600), ('Pro_Slayer', '2025-12-05', 450), ('Vocab_Ninja', '2025-12-10', 300)]
for u, d, x in dummy_users:
    c.execute("SELECT * FROM progress WHERE username=?", (u,))
    if not c.fetchone():
        c.execute("INSERT INTO progress VALUES (?, ?, ?)", (u, d, x))
conn.commit()

# --- 2. SESSION STATE ---
if 'user' not in st.session_state: st.session_state.user = "Admin_Tester"
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'page' not in st.session_state: st.session_state.page = "🏠 Home Base"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"
if 'combo' not in st.session_state: st.session_state.combo = 0
if 'v_word' not in st.session_state: st.session_state.v_word = ""
if 'v_meaning' not in st.session_state: st.session_state.v_meaning = ""

# --- 3. MEGA DATASET ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "I ____ to the gym everyday.", "o": ["goes", "go", "going", "gone"], "a": "go"},
    {"q": "Which is a NOUN?", "o": ["Run", "Beautiful", "Table", "Quickly"], "a": "Table"},
    {"q": "Opposite of 'HAPPY'?", "o": ["Sad", "Joyful", "Excited", "Cool"], "a": "Sad"},
    {"q": "Plural of 'MOUSE'?", "o": ["Mouses", "Mice", "Mices", "Mouse"], "a": "Mice"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"},
    {"q": "He ____ a doctor.", "o": ["is", "am", "are", "be"], "a": "is"}
]

# --- 4. CSS ---
st.set_page_config(page_title="English Guru Pro V27", page_icon="⚡", layout="centered")
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 100%); color: #ffffff; }}
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
    </style>
    """, unsafe_allow_html=True)

# --- 5. FUNCTIONS ---
def add_xp(pts):
    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.user, str(date.today()), pts))
    conn.commit()

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown(f"<h1>⭐ {st.session_state.user}</h1>", unsafe_allow_html=True)
    st.divider()
    st.session_state.page = st.radio("MISSIONS:", ["🏠 Home Base", "🎓 MCQ Academy", "⚔️ Daily Boss", "🗂️ Word Vault", "🏆 Leaderboard", "⚙️ Settings"])

# --- 7. PAGES ---

if st.session_state.page == "🏠 Home Base":
    st.markdown("<h1>COMMAND CENTER</h1>", unsafe_allow_html=True)
    c.execute("SELECT SUM(xp) FROM progress WHERE username = ?", (st.session_state.user,))
    total_xp = c.fetchone()[0] or 0
    
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(f"<div class='metric-card'>🏆<br>TOTAL XP<h3>{total_xp}</h3></div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='metric-card'>🎖️<br>RANK<h3>{'PRO' if total_xp > 200 else 'NOVICE'}</h3></div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='metric-card'>🔥<br>STREAK<h3>1 Day</h3></div>", unsafe_allow_html=True)

    # --- UPGRADED GROWTH CHART ---
    st.write("### 🚀 Power Level (Last 7 Days)")
    days_label = [(date.today() - timedelta(days=i)).strftime('%d %b') for i in range(6, -1, -1)]
    actual_dates = [(date.today() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    xp_vals = [c.execute("SELECT SUM(xp) FROM progress WHERE username=? AND date=?", (st.session_state.user, d)).fetchone()[0] or 0 for d in actual_dates]
    
    chart_df = pd.DataFrame({"XP": xp_vals}, index=days_label)
    st.area_chart(chart_df, color=st.session_state.theme)

elif st.session_state.page == "🎓 MCQ Academy":
    st.title("🎓 MCQ ACADEMY")
    q = random.choice(MCQ_DATA)
    st.markdown(f"<div class='metric-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, opt in enumerate(q['o']):
        with cols[idx%2]:
            if st.button(opt, key=f"mcq_{idx}"):
                if opt == q['a']:
                    st.balloons(); add_xp(10); st.success("Correct! +10 XP")
                else: st.error("Wrong!")
                time.sleep(1); st.rerun()

elif st.session_state.page == "⚔️ Daily Boss":
    st.markdown("<h1 style='color:red;'>⚔️ BOSS BATTLE</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: 
        st.write(f"🦸 Player: {st.session_state.player_hp}%")
        st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#2ecc71;'></div></div>", unsafe_allow_html=True)
    with c2: 
        st.write(f"👹 Boss: {st.session_state.boss_hp}%")
        st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#e74c3c;'></div></div>", unsafe_allow_html=True)
    
    if st.session_state.combo > 1:
        st.markdown(f"<p class='combo-text'>🔥 COMBO X{st.session_state.combo}!</p>", unsafe_allow_html=True)

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("YOU KILLED THE BOSS! +100 XP"); add_xp(100)
        if st.button("New Challenger?"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.session_state.combo = 0; st.rerun()
    elif st.session_state.player_hp <= 0:
        st.error("DEFEATED!"); 
        if st.button("Revive"): st.session_state.player_hp = 100; st.session_state.boss_hp = 100; st.session_state.combo = 0; st.rerun()
    else:
        q = random.choice(MCQ_DATA)
        st.write(f"### Q: {q['q']}")
        ans = st.radio("Attack Options:", q['o'], key="boss_atk")
        if st.button("💥 HIT BOSS"):
            if ans == q['a']:
                st.session_state.combo += 1
                damage = 25 * st.session_state.combo
                st.session_state.boss_hp -= damage
                st.session_state.battle_log = f"CRITICAL HIT! You dealt {damage} damage!"
            else:
                st.session_state.combo = 0
                st.session_state.player_hp -= 20
                st.session_state.battle_log = "OUCH! Boss hit you back for 20 damage!"
            st.rerun()
    st.info(st.session_state.battle_log)

elif st.session_state.page == "🗂️ Word Vault":
    st.title("🗂️ WORD VAULT")
    col1, col2 = st.columns(2)
    with col1: st.session_state.v_word = st.text_input("Word", value=st.session_state.v_word)
    with col2: st.session_state.v_meaning = st.text_input("Meaning", value=st.session_state.v_meaning)
    
    if st.button("🔄 Swap"):
        st.session_state.v_word, st.session_state.v_meaning = st.session_state.v_meaning, st.session_state.v_word
        st.rerun()
    if st.button("💾 Save"):
        if st.session_state.v_word:
            c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.user, st.session_state.v_word, st.session_state.v_meaning))
            conn.commit(); st.session_state.v_word = ""; st.session_state.v_meaning = ""; st.rerun()
    
    rows = c.execute("SELECT word, meaning FROM dictionary WHERE username=?", (st.session_state.user,)).fetchall()
    for r in rows: st.markdown(f"<div class='metric-card'>{r[0]} : {r[1]}</div>", unsafe_allow_html=True)

elif st.session_state.page == "🏆 Leaderboard":
    st.title("🏆 RANKINGS")
    data = c.execute("SELECT username, SUM(xp) as total FROM progress GROUP BY username ORDER BY total DESC").fetchall()
    for i, row in enumerate(data):
        rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🎖️"
        st.markdown(f"<div class='metric-card'><h3>{rank} {row[0]}</h3><p>{row[1]} XP</p></div>", unsafe_allow_html=True)

elif st.session_state.page == "⚙️ Settings":
    st.session_state.theme = st.color_picker("Pick Glow Color", st.session_state.theme)