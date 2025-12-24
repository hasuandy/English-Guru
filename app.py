import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP (Modified) ---
conn = sqlite3.connect('english_guru_pro_v28.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER)''') # Naya Table
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"
if 'combo' not in st.session_state: st.session_state.combo = 0

# --- 3. MCQ DATA ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"}
]

# --- 4. CSS (Bungee Font & Gaming UI) ---
st.set_page_config(page_title="English Guru V28", page_icon="🎮", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255, 255, 255, 0.05); border: 2px solid {st.session_state.theme}; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 15px; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border-radius: 10px; transition: 0.3s; }}
    .hp-bar {{ height: 20px; border-radius: 10px; background: #111; overflow: hidden; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def get_item_count(email, item):
    c.execute("SELECT count FROM inventory WHERE email=? AND item=?", (email, item))
    res = c.fetchone()
    return res[0] if res else 0

# --- 5. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; color:#00f2ff;'>ARENA V28</h1>", unsafe_allow_html=True)
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
    with st.sidebar:
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
        txp = get_total_xp(st.session_state.email)
        st.write(f"💰 **XP Balance:** {txp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Power-Up Shop", "🏆 Leaderboard"])
        if st.button("EXIT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- SHOP SYSTEM ---
    if page == "🛒 Power-Up Shop":
        st.markdown("<h1 style='font-family:Bungee;'>POWER-UP SHOP</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        items = [
            {"name": "🛡️ Mystic Shield", "price": 50, "desc": "Protects you from 1 Boss hit"},
            {"name": "⚡ XP Booster", "price": 100, "desc": "Get double XP in Training"}
        ]
        
        for i, item in enumerate(items):
            with [col1, col2][i]:
                st.markdown(f"<div class='gaming-card'><h3>{item['name']}</h3><p>{item['desc']}</p><b>Cost: {item['price']} XP</b></div>", unsafe_allow_html=True)
                if st.button(f"Buy {item['name']}", key=item['name']):
                    if txp >= item['price']:
                        # Deduct XP (Adding negative entry)
                        c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), -item['price']))
                        # Add to Inventory
                        current = get_item_count(st.session_state.email, item['name'])
                        if current > 0:
                            c.execute("UPDATE inventory SET count=? WHERE email=? AND item=?", (current+1, st.session_state.email, item['name']))
                        else:
                            c.execute("INSERT INTO inventory VALUES (?, ?, ?)", (st.session_state.email, item['name'], 1))
                        conn.commit()
                        st.success(f"Bought {item['name']}!")
                        st.rerun()
                    else:
                        st.error("Not enough XP!")

    # --- MODIFIED BOSS BATTLE (Shield Logic) ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS BATTLE</h1>", unsafe_allow_html=True)
        shields = get_item_count(st.session_state.email, "🛡️ Mystic Shield")
        st.info(f"Available Shields: {shields}")

        col_p, col_b = st.columns(2)
        with col_p:
            st.markdown(f"**HERO: {st.session_state.player_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"**BOSS: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp > 0 and st.session_state.player_hp > 0:
            q = random.choice(MCQ_DATA)
            st.markdown(f"<div class='gaming-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("CHOOSE WEAPON:", q['o'], horizontal=True)
            
            if st.button("💥 ATTACK"):
                if ans == q['a']:
                    st.session_state.combo += 1
                    dmg = 20 * st.session_state.combo
                    st.session_state.boss_hp -= dmg
                    st.session_state.battle_log = f"🔥 CRITICAL! {dmg} damage dealt!"
                else:
                    if shields > 0:
                        c.execute("UPDATE inventory SET count=count-1 WHERE email=? AND item=?", (st.session_state.email, "🛡️ Mystic Shield"))
                        conn.commit()
                        st.warning("SHIELD BROKEN! Damage avoided.")
                    else:
                        st.session_state.player_hp -= 25
                        st.session_state.battle_log = "❌ OUCH! Boss hit you for 25 damage!"
                    st.session_state.combo = 0
                st.rerun()
        st.write(st.session_state.battle_log)

    # --- Baki pages (Base, Training, Leaderboard) same rahengi ---
    elif page == "🏠 Base":
        st.markdown(f"<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        st.write(f"Welcome back, **{st.session_state.user}**!")
        st.metric("Total XP", txp)

    elif page == "🎓 Training":
        st.title("TRAINING ZONE")
        q = random.choice(MCQ_DATA)
        st.write(f"### {q['q']}")
        boost = get_item_count(st.session_state.email, "⚡ XP Booster")
        for opt in q['o']:
            if st.button(opt):
                if opt == q['a']:
                    reward = 20 if boost > 0 else 10
                    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), reward))
                    conn.commit()
                    st.success(f"Correct! +{reward} XP")
                    time.sleep(1)
                    st.rerun()
                else: st.error("Wrong!")

    elif page == "🏆 Leaderboard":
        st.title("GLOBAL RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.write(f"{i+1}. {row[0]} - {row[1]} XP")
