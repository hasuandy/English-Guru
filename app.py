import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# ==========================================
# 🛠️ DEVELOPER SETTINGS
# Isse True rakhne par Login skip ho jayega
DEV_MODE = True 
# ==========================================

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro_v29.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER)''') 
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"
if 'combo' not in st.session_state: st.session_state.combo = 0

# DEV MODE BYPASS
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.user = "Tester_Hero"
    st.session_state.email = "test@guru.com"

# --- 3. QUESTIONS POOL ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"}
]

# --- 4. CSS ---
st.set_page_config(page_title="English Guru V29 - DEV", page_icon="🛠️", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255, 255, 255, 0.05); border: 2px solid {st.session_state.theme}; border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 0 15px {st.session_state.theme}44; margin-bottom: 20px; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border-radius: 12px; transition: 0.4s; width: 100%; border: none; padding: 10px; }}
    .hp-bar {{ height: 25px; border-radius: 15px; background: #111; border: 1px solid #444; overflow: hidden; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# HELPER FUNCTIONS
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def get_item_count(email, item):
    c.execute("SELECT count FROM inventory WHERE email=? AND item=?", (email, item))
    res = c.fetchone()
    return res[0] if res else 0

# --- 5. AUTHENTICATION (Skip if DEV_MODE is True) ---
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
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
        with tab2:
            ne, nu, np = st.text_input("New Email"), st.text_input("Hero Name"), st.text_input("Set Key", type='password')
            if st.button("CREATE ACCOUNT"):
                h = hashlib.sha256(np.encode()).hexdigest()
                try:
                    c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                    conn.commit()
                    st.success("Account Created!")
                except: st.error("User exists!")

# --- 6. MAIN CONTENT ---
else:
    txp = get_total_xp(st.session_state.email)
    
    with st.sidebar:
        if DEV_MODE: st.error("🛠️ DEVELOPER MODE ACTIVE")
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
        st.write(f"💰 **XP Balance:** {txp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Power-Up Shop", "🏆 Leaderboard"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    if page == "🏠 Base":
        st.markdown("<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='gaming-card'>🏆 TOTAL XP<br><h2>{txp}</h2></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='gaming-card'>🎖️ RANK<br><h2>{'LEGEND' if txp > 500 else 'WARRIOR'}</h2></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='gaming-card'>⚡ LEVEL<br><h2>{1 + (txp // 100)}</h2></div>", unsafe_allow_html=True)

    elif page == "🛒 Power-Up Shop":
        st.markdown("<h1 style='font-family:Bungee; color:#ffcc00;'>POWER-UP SHOP</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        shop_items = [
            {"name": "🛡️ Mystic Shield", "price": 50, "desc": "Saves you from 1 Boss hit!", "img": "🛡️"},
            {"name": "⚡ XP Booster", "price": 100, "desc": "Double XP in Training!", "img": "⚡"}
        ]
        for i, item in enumerate(shop_items):
            with [c1, c2][i]:
                st.markdown(f"<div class='gaming-card'><h1>{item['img']}</h1><h3>{item['name']}</h3><p>{item['desc']}</p><b>Cost: {item['price']} XP</b></div>", unsafe_allow_html=True)
                if st.button(f"BUY {item['name']}", key=item['name']):
                    if txp >= item['price'] or DEV_MODE: # Dev mode mein free
                        c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), -item['price']))
                        curr = get_item_count(st.session_state.email, item['name'])
                        if curr > 0: c.execute("UPDATE inventory SET count=? WHERE email=? AND item=?", (curr+1, st.session_state.email, item['name']))
                        else: c.execute("INSERT INTO inventory VALUES (?, ?, ?)", (st.session_state.email, item['name'], 1))
                        conn.commit()
                        st.success("Item Acquired!")
                        st.rerun()
                    else: st.error("Need more XP!")

    elif page == "🎓 Training":
        st.markdown("<h1 style='font-family:Bungee;'>TRAINING ZONE</h1>", unsafe_allow_html=True)
        q = random.choice(MCQ_DATA)
        st.markdown(f"<div class='gaming-card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            with cols[i%2]:
                if st.button(opt, key=f"t_{i}_{time.time()}"):
                    if opt == q['a']:
                        c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today()), 10))
                        conn.commit()
                        st.balloons()
                        st.rerun()

    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS BATTLE</h1>", unsafe_allow_html=True)
        shields = get_item_count(st.session_state.email, "🛡️ Mystic Shield")
        col_p, col_b = st.columns(2)
        with col_p:
            st.markdown(f"**HERO HP: {st.session_state.player_hp}%** | 🛡️ {shields}")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=200)
            st.markdown(f"**BOSS HP: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)
        
        # Battle logic... (Same as before)
        q = random.choice(MCQ_DATA)
        st.markdown(f"<div class='gaming-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
        ans = st.radio("Choose:", q['o'], horizontal=True)
        if st.button("💥 ATTACK"):
            if ans == q['a']:
                st.session_state.boss_hp -= 20
                st.success("HIT!")
            else:
                if shields > 0:
                    c.execute("UPDATE inventory SET count=count-1 WHERE email=? AND item=?", (st.session_state.email, "🛡️ Mystic Shield"))
                    conn.commit()
                    st.warning("Shield Saved You!")
                else:
                    st.session_state.player_hp -= 20
                    st.error("BOSS HIT YOU!")
            st.rerun()

    elif page == "🏆 Leaderboard":
        st.title("🏆 RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.write(f"{i+1}. {row[0]} - {row[1]} XP")
