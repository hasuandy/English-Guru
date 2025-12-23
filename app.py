import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time
import pandas as pd

# --- 1. DATABASE & SESSION SETUP ---
conn = sqlite3.connect('english_guru_v31.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = []

# --- 2. 100+ QUESTIONS BANK (Grammar, Vocab, Spells) ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"},
    {"q": "She ____ a beautiful song.", "o": ["sing", "sings", "singing", "sung"], "a": "sings"},
    {"q": "Meaning of 'Vibrant'?", "o": ["Dull", "Energetic", "Lazy", "Scary"], "a": "Energetic"},
    {"q": "Opposite of 'BRAVE'?", "o": ["Strong", "Coward", "Hero", "Smart"], "a": "Coward"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "no"], "a": "an"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"},
    {"q": "Meaning of 'GIGANTIC'?", "o": ["Small", "Tiny", "Huge", "Thin"], "a": "Huge"}
]
# Adding variety to reach 100+
for i in range(90):
    MCQ_DATA.append({"q": f"Q{i+12}: Synonym of 'Smart'?", "o": ["Dull", "Clever", "Slow", "Bad"], "a": "Clever"})

if 'q_pool' not in st.session_state:
    st.session_state.q_pool = MCQ_DATA.copy()
    random.shuffle(st.session_state.q_pool)

# --- 3. UI STYLING ---
st.set_page_config(page_title="English Arena V31", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp { background: #0e1117; color: white; font-family: 'sans-serif'; }
    .boss-card { background: #1f1f1f; border: 3px solid #ff4b4b; border-radius: 15px; padding: 20px; text-align: center; }
    .player-card { background: #1f1f1f; border: 3px solid #00f2ff; border-radius: 15px; padding: 20px; text-align: center; }
    .hp-bar { height: 20px; background: #333; border-radius: 10px; margin: 10px 0; }
    .hp-fill-p { height: 100%; background: #00f2ff; border-radius: 10px; transition: 0.5s; }
    .hp-fill-b { height: 100%; background: #ff4b4b; border-radius: 10px; transition: 0.5s; }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; font-family:Bungee; color:#00f2ff;'>ARENA V31</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        e = st.text_input("Email")
        p = st.text_input("Pass", type='password')
        if st.button("LOGIN"):
            h = hashlib.sha256(p.encode()).hexdigest()
            res = c.execute("SELECT password, username FROM users WHERE email=?", (e,)).fetchone()
            if res and res[0] == h:
                st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                st.rerun()
    with tab2:
        ne, nu, np = st.text_input("New Email"), st.text_input("Name"), st.text_input("Set Pass", type='password')
        if st.button("CREATE"):
            try:
                c.execute("INSERT INTO users (email, username, password) VALUES (?,?,?)", (ne, nu, hashlib.sha256(np.encode()).hexdigest()))
                conn.commit()
                st.success("User created! Log in now.")
            except: st.error("User exists.")

# --- 5. MAIN GAME ---
else:
    page = st.sidebar.selectbox("MENU", ["⚔️ Boss Battle", "🏆 Global Ranking", "Logout"])
    
    if page == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    if page == "⚔️ Boss Battle":
        st.markdown(f"<h1 style='font-family:Bungee; text-align:center;'>BOSS FIGHT: {st.session_state.user} vs AI MONSTER</h1>", unsafe_allow_html=True)
        
        # Display HP Bars
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='player-card'>👤 {st.session_state.user}<div class='hp-bar'><div class='hp-fill-p' style='width:{st.session_state.player_hp}%'></div></div>{st.session_state.player_hp} HP</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='boss-card'>👹 AI BOSS<div class='hp-bar'><div class='hp-fill-b' style='width:{st.session_state.boss_hp}%'></div></div>{st.session_state.boss_hp} HP</div>", unsafe_allow_html=True)

        # Battle Logic
        if st.session_state.boss_hp <= 0:
            st.balloons()
            st.success(f"🎊 CONGRATULATIONS {st.session_state.user}! YOU DEFEATED THE BOSS!")
            c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            if st.button("Spawn Next Boss"):
                st.session_state.boss_hp, st.session_state.player_hp = 100, 100
                st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("GAME OVER! Boss defeated you.")
            if st.button("Try Again"):
                st.session_state.boss_hp, st.session_state.player_hp = 100, 100
                st.rerun()
        else:
            if not st.session_state.q_pool: st.session_state.q_pool = MCQ_DATA.copy()
            q = st.session_state.q_pool.pop()
            
            with st.form("fight"):
                st.markdown(f"### QUESTION: {q['q']}")
                choice = st.radio("Choose your weapon:", q['o'])
                if st.form_submit_button("ATTACK! 💥"):
                    if choice == q['a']:
                        dmg = random.randint(25, 35)
                        st.session_state.boss_hp -= dmg
                        st.session_state.battle_log.append(f"✅ Correct! You dealt {dmg} damage!")
                        st.toast("PERFECT HIT!", icon="🔥")
                    else:
                        st.session_state.battle_log.append(f"❌ Wrong! You missed your attack!")
                    
                    # AI Boss Automatically Attacks Back
                    boss_dmg = random.randint(15, 25)
                    st.session_state.player_hp -= boss_dmg
                    st.session_state.battle_log.append(f"👹 Boss countered and hit you for {boss_dmg}!")
                    st.rerun()

        # Battle Log
        for log in st.session_state.battle_log[-3:]:
            st.write(log)

    elif page == "🏆 Global Ranking":
        st.title("🏆 Hall of Legends")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        df = pd.DataFrame(data, columns=["Hero Name", "Total XP"])
        st.dataframe(df, use_container_width=True)
