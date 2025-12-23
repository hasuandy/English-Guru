import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_arena_v33.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE INITIALIZATION (BOHOT ZAROORI HAI) ---
# Isse AttributeError kabhi nahi aayega
state_defaults = {
    'logged_in': False,
    'user': None,
    'email': None,
    'boss_hp': 100,
    'player_hp': 100,
    'battle_log': [],
    'q_pool': [],
    'current_q': None
}

for key, value in state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 3. MASSIVE 100+ QUESTIONS BANK ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"},
    {"q": "She ____ a beautiful song.", "o": ["sing", "sings", "singing", "sung"], "a": "sings"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "no"], "a": "an"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"}
]
# Adding 100+ items logic
if not st.session_state.q_pool:
    temp_pool = MCQ_DATA.copy()
    for i in range(100):
        temp_pool.append({"q": f"Level {i}: Correct spelling?", "o": ["Grammer", "Grammar", "Grammarre", "Gramme"], "a": "Grammar"})
    random.shuffle(temp_pool)
    st.session_state.q_pool = temp_pool

# --- 4. UI STYLING ---
st.set_page_config(page_title="English Arena V33", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp { background: #0a0e14; color: white; }
    .boss-box { background: #3b0000; border: 2px solid #ff4b4b; border-radius: 15px; padding: 20px; text-align: center; }
    .player-box { background: #002b36; border: 2px solid #00f2ff; border-radius: 15px; padding: 20px; text-align: center; }
    .hp-bar-bg { width: 100%; background: #222; border-radius: 10px; height: 15px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 5. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; color:#00f2ff;'>ARENA V33</h1>", unsafe_allow_html=True)
    mode = st.tabs(["🔥 Login", "💎 Signup"])
    
    with mode[0]:
        le = st.text_input("Email", key="le")
        lp = st.text_input("Password", type="password", key="lp")
        if st.button("START BATTLE"):
            res = c.execute("SELECT password, username FROM users WHERE email=?", (le,)).fetchone()
            if res and res[0] == hashlib.sha256(lp.encode()).hexdigest():
                st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], le
                st.rerun()
            else: st.error("Wrong Key!")
            
    with mode[1]:
        ne, nu, np = st.text_input("New Email"), st.text_input("Hero Name"), st.text_input("Set Key", type="password")
        if st.button("CREATE HERO"):
            try:
                c.execute("INSERT INTO users VALUES (?,?,?)", (ne, nu, hashlib.sha256(np.encode()).hexdigest()))
                conn.commit()
                st.success("Hero Created! Please Login.")
            except: st.error("Email already taken!")

# --- 6. GAME CONTENT ---
else:
    page = st.sidebar.selectbox("COMMANDS", ["⚔️ Boss Battle", "🏆 Leaderboard", "Logout"])
    
    if page == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    if page == "⚔️ Boss Battle":
        st.markdown(f"<h2 style='text-align:center; font-family:Bungee;'>MISSION: DESTROY AI MONSTER</h2>", unsafe_allow_html=True)

        # Health Display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='player-box'>🛡️ {st.session_state.user}<div class='hp-bar-bg'><div style='width:{st.session_state.player_hp}%; background:#00f2ff; height:100%; border-radius:10px;'></div></div>{st.session_state.player_hp} HP</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='boss-box'>👹 AI BOSS<div class='hp-bar-bg'><div style='width:{st.session_state.boss_hp}%; background:#ff4b4b; height:100%; border-radius:10px;'></div></div>{st.session_state.boss_hp} HP</div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons()
            st.success(f"🎊 CONGRATULATIONS {st.session_state.user}! You saved the Arena!")
            c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            if st.button("SPAWN NEW BOSS"):
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.battle_log = 100, 100, []
                st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 DEFEATED! The Boss was too strong.")
            if st.button("REVIVE"):
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.battle_log = 100, 100, []
                st.rerun()
        else:
            # Pick a question if not already picked
            if not st.session_state.current_q:
                st.session_state.current_q = st.session_state.q_pool.pop(0)

            q = st.session_state.current_q
            with st.form("fight_form"):
                st.write(f"### ❓ {q['q']}")
                ans = st.radio("Choose Weapon:", q['o'])
                if st.form_submit_button("💥 LAUNCH ATTACK"):
                    if ans == q['a']:
                        dmg = random.randint(30, 45)
                        st.session_state.boss_hp -= dmg
                        st.session_state.battle_log.append(f"✅ EXCELLENT! You dealt {dmg} DMG!")
                        st.toast(f"Critical Hit! +{dmg} Damage", icon="🔥")
                    else:
                        st.session_state.battle_log.append("❌ MISSED! Your attack failed.")
                    
                    # AI Opponent Automatic Turn
                    boss_dmg = random.randint(15, 25)
                    st.session_state.player_hp -= boss_dmg
                    st.session_state.battle_log.append(f"👹 BOSS TURN: Counter-attacked for {boss_dmg} DMG!")
                    
                    st.session_state.current_q = None # Reset for next turn
                    st.rerun()

        # Display Logs
        for log in st.session_state.battle_log[-3:]:
            st.info(log)

    elif page == "🏆 Leaderboard":
        st.markdown("<h1 style='font-family:Bungee;'>HALL OF LEGENDS</h1>", unsafe_allow_html=True)
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        if data:
            st.dataframe(pd.DataFrame(data, columns=["Hero", "Total XP"]), use_container_width=True)
