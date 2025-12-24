import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# ==========================================
# 🛠️ DEVELOPER SETTINGS
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
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is waiting... 👹"
if 'combo' not in st.session_state: st.session_state.combo = 0

if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.user = "Tester_Hero"
    st.session_state.email = "test@guru.com"

# --- 3. SEPARATE QUESTIONS POOLS ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "no"], "a": "an"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"}
]

BOSS_DATA = [
    {"q": "Meaning of 'GIGANTIC'?", "o": ["Small", "Tiny", "Huge", "Thin"], "a": "Huge"},
    {"q": "Meaning of 'Vibrant'?", "o": ["Dull", "Energetic", "Lazy", "Scary"], "a": "Energetic"},
    {"q": "Correct spelling?", "o": ["Recieve", "Receive", "Recive", "Receve"], "a": "Receive"},
    {"q": "Which is a synonym of 'Meticulous'?", "o": ["Careless", "Careful", "Lazy", "Fast"], "a": "Careful"},
    {"q": "Opposite of 'Fortunate'?", "o": ["Lucky", "Unlucky", "Rich", "Happy"], "a": "Unlucky"}
]

# --- 4. CSS ---
st.set_page_config(page_title="English Guru V29 - AUTO BOSS", page_icon="⚔️", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ background: rgba(255, 255, 255, 0.05); border: 2px solid {st.session_state.theme}; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 0 15px {st.session_state.theme}44; margin-bottom: 15px; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border-radius: 12px; transition: 0.4s; width: 100%; border: none; padding: 10px; }}
    .hp-bar {{ height: 25px; border-radius: 15px; background: #111; border: 1px solid #444; overflow: hidden; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    </style>
    """, unsafe_allow_html=True)

def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def get_item_count(email, item):
    c.execute("SELECT count FROM inventory WHERE email=? AND item=?", (email, item))
    res = c.fetchone()
    return res[0] if res else 0

# --- 5. MAIN CONTENT ---
if st.session_state.logged_in:
    txp = get_total_xp(st.session_state.email)
    
    with st.sidebar:
        if DEV_MODE: st.error("🛠️ DEV MODE")
        st.markdown(f"<h2 style='color:{st.session_state.theme}; font-family:Bungee;'>🛡️ {st.session_state.user}</h2>", unsafe_allow_html=True)
        st.write(f"💰 **XP:** {txp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Leaderboard"])

    if page == "🏠 Base":
        st.markdown("<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        st.write(f"Welcome, **{st.session_state.user}**. Gear up for the next battle!")
        st.metric("Total XP", txp)

    elif page == "🎓 Training":
        st.markdown("<h1 style='font-family:Bungee;'>TRAINING ZONE</h1>", unsafe_allow_html=True)
        q = random.choice(TRAINING_DATA)
        st.markdown(f"<div class='gaming-card'><h2>{q['q']}</h2></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            with cols[i%2]:
                if st.button(opt, key=f"t_{i}_{time.time()}"):
                    if opt == q['a']:
                        c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today()), 10))
                        conn.commit()
                        st.balloons(); st.success("Correct! +10 XP"); time.sleep(0.5); st.rerun()
                    else: st.error("Wrong!"); time.sleep(0.5); st.rerun()

    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee;'>BOSS ARENA</h1>", unsafe_allow_html=True)
        shields = get_item_count(st.session_state.email, "🛡️ Mystic Shield")
        
        col_p, col_b = st.columns(2)
        with col_p:
            st.markdown(f"**HERO HP: {st.session_state.player_hp}%** | 🛡️ {shields}")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
        with col_b:
            st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=180)
            st.markdown(f"**BOSS HP: {st.session_state.boss_hp}%**")
            st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.success("🏆 BOSS DEFEATED!"); c.execute("INSERT INTO progress VALUES (?, ?, 100)", (st.session_state.email, str(date.today()), 100)); conn.commit()
            if st.button("RESET"): st.session_state.boss_hp=100; st.session_state.player_hp=100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 YOU DIED!"); 
            if st.button("REVIVE"): st.session_state.boss_hp=100; st.session_state.player_hp=100; st.rerun()
        else:
            # Boss Battle Question
            if 'current_boss_q' not in st.session_state:
                st.session_state.current_boss_q = random.choice(BOSS_DATA)
            
            bq = st.session_state.current_boss_q
            st.markdown(f"<div class='gaming-card'><h3>{bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("SELECT YOUR ATTACK:", bq['o'], horizontal=True)
            
            if st.button("🔥 EXECUTE ATTACK"):
                # --- PLAYER ATTACK ---
                if ans == bq['a']:
                    dmg = 25
                    st.session_state.boss_hp -= dmg
                    st.session_state.battle_log = f"✅ You hit the Boss for {dmg} DMG!"
                else:
                    st.session_state.battle_log = "❌ Your attack missed!"
                
                # --- AUTOMATIC BOSS COUNTER ---
                if st.session_state.boss_hp > 0:
                    time.sleep(0.3)
                    boss_dmg = random.choice([0, 15, 20, 25]) # Boss can miss or hit
                    if boss_dmg > 0:
                        if shields > 0:
                            c.execute("UPDATE inventory SET count=count-1 WHERE email=? AND item=?", (st.session_state.email, "🛡️ Mystic Shield"))
                            conn.commit()
                            st.session_state.battle_log += " | 🛡️ Shield saved you!"
                        else:
                            st.session_state.player_hp -= boss_dmg
                            st.session_state.battle_log += f" | ⚠️ Boss countered for {boss_dmg} DMG!"
                    else:
                        st.session_state.battle_log += " | 💨 Boss missed his counter!"
                
                # Refresh question for next turn
                st.session_state.current_boss_q = random.choice(BOSS_DATA)
                st.rerun()

        st.info(st.session_state.battle_log)

    elif page == "🛒 Shop":
        st.markdown("<h1 style='font-family:Bungee;'>SHOP</h1>", unsafe_allow_html=True)
        if st.button("Buy Shield (50 XP)"):
            if txp >= 50:
                c.execute("INSERT INTO progress VALUES (?, ?, -50)", (st.session_state.email, str(date.today()), -50))
                c.execute("INSERT INTO inventory VALUES (?, '🛡️ Mystic Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1")
                conn.commit(); st.success("Shield Purchased!"); st.rerun()
            else: st.error("No XP!")

    elif page == "🏆 Leaderboard":
        st.title("RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data): st.write(f"{i+1}. {row[0]} - {row[1]} XP")
