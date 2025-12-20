import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v30.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"

# --- 3. SOUND EFFECTS LOGIC ---
def play_sound(url):
    st.markdown(f'<audio src="{url}" autoplay="true" style="display:none;"></audio>', unsafe_allow_html=True)

# Sound Links (Example URLs - Replace with your own mp3 links if needed)
SUCCESS_SOUND = "https://www.myinstants.com/media/sounds/level-up-191.mp3"
FAILURE_SOUND = "https://www.myinstants.com/media/sounds/wrong-answer-126.mp3"
BATTLE_SOUND = "https://www.myinstants.com/media/sounds/sword-hit-71.mp3"

# --- 4. 100+ QUESTION GENERATOR ---
# Tip: Aap yahan jitne chahe sawal add kar sakte hain, ye unlimited chalega.
QUESTIONS = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "Translate: 'Never give up'", "o": ["Haar mat maano", "Koshish mat karo", "Bhul jao", "Ruk jao"], "a": "Haar mat maano"},
    {"q": "She ____ a song.", "o": ["sing", "sings", "singing", "sung"], "a": "sings"},
    {"q": "Meaning of 'Vibrant'?", "o": ["Dull", "Energetic", "Lazy", "Scary"], "a": "Energetic"},
    {"q": "Opposite of 'BRAVE'?", "o": ["Strong", "Coward", "Hero", "Smart"], "a": "Coward"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "no"], "a": "an"},
    {"q": "Plural of 'CHILD'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"},
    {"q": "Past tense of 'GO'?", "o": ["Gone", "Went", "Goes", "Going"], "a": "Went"},
    {"q": "Correct spelling?", "o": ["Recieve", "Receive", "Recive", "Receve"], "a": "Receive"}
]

# --- 5. ULTRA PREMIUM CSS ---
st.set_page_config(page_title="Cyber Guru V30", page_icon="⚔️", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Bungee&display=swap');
    
    .stApp { 
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://wallpaperaccess.com/full/2650153.jpg');
        background-size: cover; background-attachment: fixed;
        font-family: 'Orbitron', sans-serif; color: #fff;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 2px solid #00f2ff;
        border-radius: 30px; padding: 40px;
        box-shadow: 0 0 30px #00f2ff33;
    }

    .stButton>button {
        background: rgba(0,0,0,0.2) !important;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        border-radius: 15px; font-family: 'Bungee', cursive;
        font-size: 18px; padding: 15px; transition: 0.3s; width: 100%;
    }
    
    .stButton>button:hover {
        background: #00f2ff !important; color: #000 !important;
        box-shadow: 0 0 50px #00f2ff; transform: scale(1.02);
    }

    .hp-bar { height: 25px; border-radius: 50px; background: #111; border: 1px solid #444; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 6. CORE LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center; color:#00f2ff; font-family:Bungee; font-size:4rem;'>ARENA V30</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        tab1, tab2 = st.tabs(["🔑 LOGIN", "🛡️ SIGNUP"])
        with tab1:
            e = st.text_input("EMAIL")
            p = st.text_input("PASSWORD", type='password')
            if st.button("ENTER PORTAL"):
                h = hashlib.sha256(p.encode()).hexdigest()
                c.execute('SELECT password, username FROM users WHERE email=?', (e,))
                res = c.fetchone()
                if res and res[0] == h:
                    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, res[1], e
                    st.rerun()
        with tab2:
            ne, nu, np = st.text_input("NEW EMAIL"), st.text_input("WARRIOR NAME"), st.text_input("KEY", type='password')
            if st.button("CREATE HERO"):
                if "@" in ne and nu:
                    h = hashlib.sha256(np.encode()).hexdigest()
                    try:
                        c.execute('INSERT INTO users VALUES (?,?,?,0)', (ne, nu, h))
                        conn.commit()
                        st.session_state.logged_in, st.session_state.user, st.session_state.email = True, nu, ne
                        st.rerun()
                    except: st.error("Warrior ID exists!")

else:
    with st.sidebar:
        st.markdown(f"<h2 style='color:#00f2ff;'>⚔️ {st.session_state.user}</h2>", unsafe_allow_html=True)
        menu = st.radio("SELECT MISSION", ["🏠 Hub", "🎓 Training", "⚔️ Boss Battle", "🏆 Leaderboard"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    if menu == "🏠 Hub":
        st.markdown("<h1 style='font-family:Bungee;'>DASHBOARD</h1>", unsafe_allow_html=True)
        c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,))
        xp = c.fetchone()[0] or 0
        st.markdown(f"<div class='glass-card'><h1 style='color:#00f2ff;'>{xp} XP</h1><p>RANK: {'COMMANDER' if xp > 500 else 'SOLDIER'}</p></div>", unsafe_allow_html=True)

    elif menu == "🎓 Training":
        st.markdown("<h1 style='font-family:Bungee;'>GRIND ZONE</h1>", unsafe_allow_html=True)
        q = random.choice(QUESTIONS)
        st.markdown(f"<div class='glass-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, opt in enumerate(q['o']):
            with cols[i%2]:
                if st.button(opt, key=f"t_{i}_{time.time()}"):
                    if opt == q['a']:
                        play_sound(SUCCESS_SOUND)
                        st.success("CLEAN HIT! +10 XP")
                        c.execute("INSERT INTO progress VALUES (?, ?, 10)", (st.session_state.email, str(date.today())))
                        conn.commit(); time.sleep(0.8); st.rerun()
                    else:
                        play_sound(FAILURE_SOUND)
                        st.error("FAILED!")

    elif menu == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff0055; font-family:Bungee;'>BOSS FIGHT</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"HERO: {st.session_state.player_hp}%")
            st.markdown(f"<div class='hp-bar'><div style='width:{st.session_state.player_hp}%; background:#00f2ff; height:100%;'></div></div>", unsafe_allow_html=True)
        with c2:
            st.write(f"BOSS: {st.session_state.boss_hp}%")
            st.markdown(f"<div class='hp-bar'><div style='width:{st.session_state.boss_hp}%; background:#ff0055; height:100%;'></div></div>", unsafe_allow_html=True)

        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("BOSS ELIMINATED! +100 XP")
            c.execute("INSERT INTO progress VALUES (?, ?, 100)", (st.session_state.email, str(date.today()))); conn.commit()
            if st.button("SPAWN NEW BOSS"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("YOU DIED!")
            if st.button("REVIVE"): st.session_state.player_hp = 100; st.session_state.boss_hp = 100; st.rerun()
        else:
            q = random.choice(QUESTIONS)
            st.markdown(f"<div class='glass-card'>{q['q']}</div>", unsafe_allow_html=True)
            ans = st.radio("CHOOSE MOVE:", q['o'], horizontal=True)
            if st.button("💥 STRIKE"):
                if ans == q['a']:
                    play_sound(BATTLE_SOUND)
                    st.session_state.boss_hp -= 25
                    st.session_state.battle_log = "CRITICAL HIT!"
                else:
                    play_sound(FAILURE_SOUND)
                    st.session_state.player_hp -= 20
                    st.session_state.battle_log = "BOSS REPELLED!"
                st.rerun()
        st.info(st.session_state.battle_log)

    elif menu == "🏆 Leaderboard":
        st.title("GLOBAL RANKINGS")
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC").fetchall()
        for i, row in enumerate(data):
            st.markdown(f"<div class='glass-card' style='padding:15px; margin-bottom:10px;'>#{i+1} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)
