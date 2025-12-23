import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import pandas as pd

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_arena_v34.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE FIX (Sabse Pehle) ---
# Ye block ensure karta hai ki 'battle_log' hamesha available rahe
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'battle_log' not in st.session_state: st.session_state.battle_log = []
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'q_pool' not in st.session_state: st.session_state.q_pool = []
if 'current_q' not in st.session_state: st.session_state.current_q = None

# --- 3. MASSIVE QUESTION POOL ---
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
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"}
]
# Ensure 100+ questions
if not st.session_state.q_pool:
    full_list = MCQ_DATA.copy()
    for i in range(100):
        full_list.append({"q": f"Q{i+11}: Choose Correct Spelling", "o": ["Grammer", "Grammar", "Grammerr", "Grammarre"], "a": "Grammar"})
    random.shuffle(full_list)
    st.session_state.q_pool = full_list

# --- 4. CSS ---
st.set_page_config(page_title="Arena V34", layout="wide")
st.markdown("""<style>
    .stApp { background: #0e1117; color: white; }
    .boss-ui { border: 2px solid #ff4b4b; padding: 20px; border-radius: 15px; background: #260101; text-align: center; }
    .player-ui { border: 2px solid #00f2ff; padding: 20px; border-radius: 15px; background: #012626; text-align: center; }
</style>""", unsafe_allow_html=True)

# --- 5. AUTH ---
if not st.session_state.logged_in:
    st.title("🎮 ENGLISH ARENA V34")
    t1, t2 = st.tabs(["Login", "Signup"])
    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("Enter Arena"):
            res = c.execute("SELECT password, username FROM users WHERE email=?", (e,)).fetchone()
            if res and res[0] == hashlib.sha256(p.encode()).hexdigest():
                st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                st.rerun()
    with t2:
        ne, nu, np = st.text_input("New Email"), st.text_input("Hero Name"), st.text_input("Set Key", type="password")
        if st.button("Create Account"):
            c.execute("INSERT INTO users VALUES (?,?,?)", (ne, nu, hashlib.sha256(np.encode()).hexdigest()))
            conn.commit()
            st.success("Account Created!")

# --- 6. GAMEPLAY ---
else:
    page = st.sidebar.radio("Navigation", ["⚔️ Boss Battle", "🏆 Leaderboard", "Logout"])
    
    if page == "Logout":
        st.session_state.logged_in = False
        st.rerun()

    if page == "⚔️ Boss Battle":
        st.header(f"FIGHT FOR GLORY, {st.session_state.user}!")
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f"<div class='player-ui'>🛡️ {st.session_state.user}<br>HP: {st.session_state.player_hp}</div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='boss-ui'>👹 AI BOSS<br>HP: {st.session_state.boss_hp}</div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons()
            st.success("🔥 BOSS DEFEATED! You are a Legend! +100 XP")
            c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 100))
            conn.commit()
            if st.button("Respawn Boss"):
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.battle_log = 100, 100, []
                st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("💀 DEFEATED! Try again.")
            if st.button("Revive"):
                st.session_state.boss_hp, st.session_state.player_hp, st.session_state.battle_log = 100, 100, []
                st.rerun()
        else:
            if not st.session_state.current_q: st.session_state.current_q = st.session_state.q_pool.pop(0)
            
            q = st.session_state.current_q
            with st.form("battle_form"):
                st.write(f"### {q['q']}")
                ans = st.radio("Choose Weapon:", q['o'])
                if st.form_submit_button("💥 ATTACK"):
                    if ans == q['a']:
                        dmg = random.randint(30, 45)
                        st.session_state.boss_hp -= dmg
                        st.session_state.battle_log.append(f"✅ Correct! You hit the boss for {dmg} DMG!")
                    else:
                        st.session_state.battle_log.append("❌ Wrong! You missed the attack.")
                    
                    # AI AUTOMATIC COUNTER ATTACK
                    boss_dmg = random.randint(15, 25)
                    st.session_state.player_hp -= boss_dmg
                    st.session_state.battle_log.append(f"👹 BOSS TURN: Boss hit you for {boss_dmg} DMG!")
                    
                    st.session_state.current_q = None # Get new question on rerun
                    st.rerun()

        for log in st.session_state.battle_log[-3:]:
            st.info(log)

    elif page == "🏆 Leaderboard":
        st.title("🏆 RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        st.table(pd.DataFrame(data, columns=["Hero", "Total XP"]))
