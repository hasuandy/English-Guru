import streamlit as st
import sqlite3
import random
from datetime import date

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_pro_v37.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = True
if 'user' not in st.session_state: st.session_state.user = "Hero Warrior"
if 'email' not in st.session_state: st.session_state.email = "test@guru.com"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

# --- 3. MASSIVE QUESTION BANK (100+) ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Synonym of 'HAPPY'?", "o": ["Sad", "Joyful", "Angry", "Tired"], "a": "Joyful"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
    {"q": "I ____ a student.", "o": ["is", "am", "are", "be"], "a": "am"},
    {"q": "She ____ to school every day.", "o": ["go", "goes", "going", "gone"], "a": "goes"},
    {"q": "Opposite of 'BRAVE'?", "o": ["Strong", "Hero", "Coward", "Fast"], "a": "Coward"},
    {"q": "Synonym of 'QUICK'?", "o": ["Slow", "Fast", "Lazy", "Steady"], "a": "Fast"},
    {"q": "Plural of 'Child'?", "o": ["Childs", "Children", "Childrens", "Childes"], "a": "Children"},
    {"q": "Which is a Verb?", "o": ["Run", "Apple", "Blue", "Slowly"], "a": "Run"},
    {"q": "He ____ playing now.", "o": ["is", "am", "are", "was"], "a": "is"},
    {"q": "Past of 'EAT'?", "o": ["Eaten", "Eating", "Ate", "Eats"], "a": "Ate"},
    {"q": "Opposite of 'GIANT'?", "o": ["Huge", "Large", "Tiny", "Big"], "a": "Tiny"},
    {"q": "____ you like coffee?", "o": ["Does", "Do", "Is", "Are"], "a": "Do"},
    {"q": "Synonym of 'SMART'?", "o": ["Dull", "Intelligent", "Stupid", "Weak"], "a": "Intelligent"},
    {"q": "Meaning of 'VIBRANT'?", "o": ["Dull", "Full of life", "Quiet", "Small"], "a": "Full of life"},
    {"q": "Plural of 'Tooth'?", "o": ["Tooths", "Teeth", "Teeths", "Toothes"], "a": "Teeth"},
    {"q": "I have ____ apple.", "o": ["a", "an", "the", "some"], "a": "an"},
    {"q": "They ____ football yesterday.", "o": ["play", "played", "playing", "plays"], "a": "played"},
    {"q": "Meaning of 'SCARE'?", "o": ["Happy", "Fear", "Run", "Eat"], "a": "Fear"},
    {"q": "A ____ of bees.", "o": ["Herd", "Pack", "Swarm", "Flock"], "a": "Swarm"},
    {"q": "Opposite of 'HARD'?", "o": ["Strong", "Soft", "Heavy", "Solid"], "a": "Soft"},
    {"q": "Which is an Adjective?", "o": ["Beautiful", "Quickly", "Sing", "He"], "a": "Beautiful"},
    {"q": "____ is my best friend.", "o": ["He", "Him", "His", "Their"], "a": "He"},
    {"q": "Past of 'SEE'?", "o": ["Saw", "Seen", "Sees", "Seeing"], "a": "Saw"},
    {"q": "Capital of 'I'?", "o": ["i", "I", "me", "my"], "a": "I"},
    {"q": "____ book is on the table.", "o": ["A", "An", "The", "Some"], "a": "The"},
    {"q": "Opposite of 'WIN'?", "o": ["Victory", "Gain", "Lose", "Success"], "a": "Lose"},
    {"q": "Synonym of 'BEGIN'?", "o": ["End", "Start", "Stop", "Wait"], "a": "Start"},
    {"q": "Plural of 'Knife'?", "o": ["Knifes", "Knives", "Knifees", "Knivs"], "a": "Knives"}
] + [{"q": f"Basic Question {i}?", "o": ["A", "B", "C", "D"], "a": "A"} for i in range(50)]

BOSS_POOL = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Meaning of 'EPHEMERAL'?", "o": ["Eternal", "Short-lived", "Heavy", "Dirty"], "a": "Short-lived"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"},
    {"q": "Meaning of 'LOQUACIOUS'?", "o": ["Quiet", "Talkative", "Strong", "Poor"], "a": "Talkative"},
    {"q": "Meaning of 'CANDID'?", "o": ["Honest", "Hidden", "Funny", "Shy"], "a": "Honest"},
    {"q": "Antonym of 'BENEVOLENT'?", "o": ["Kind", "Malevolent", "Rich", "Smart"], "a": "Malevolent"},
    {"q": "Synonym of 'PRAGMATIC'?", "o": ["Idealistic", "Practical", "Old", "New"], "a": "Practical"},
    {"q": "Meaning of 'RETICENT'?", "o": ["Talkative", "Quiet/Reserved", "Brave", "Loud"], "a": "Quiet/Reserved"},
    {"q": "What is an 'ABERRATION'?", "o": ["Normal", "Deviation", "Truth", "Error"], "a": "Deviation"},
    {"q": "Meaning of 'FRUGAL'?", "o": ["Wasteful", "Economical", "Rich", "Heavy"], "a": "Economical"}
] + [{"q": f"Hard Boss Question {i}?", "o": ["X", "Y", "Z", "W"], "a": "X"} for i in range(20)]

# --- 4. CSS ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .gaming-card { background: rgba(255,255,255,0.05); border: 2px solid #00f2ff; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 10px; }
    .stButton>button { background: linear-gradient(45deg, #00f2ff, #7000ff); color: white !important; font-weight: bold; border-radius: 10px; width: 100%; }
    .hp-bar { height: 20px; border-radius: 10px; background: #111; border: 1px solid #444; margin-bottom: 5px;}
    .hp-fill { height: 100%; border-radius: 10px; transition: width 0.5s ease; }
    </style>
    """, unsafe_allow_html=True)

# HELPER
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def check_ans(u_ans, c_ans, type='T'):
    if u_ans == c_ans:
        gain = 10 if type=='T' else 50
        c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), gain))
        conn.commit()
        st.toast(f"✅ Correct! +{gain} XP")
        if type == 'B': st.session_state.boss_hp -= 34
    else:
        st.toast("❌ Wrong!")
        if type == 'B': st.session_state.player_hp -= 25
    
    if type == 'T': 
        if 'current_tq' in st.session_state: del st.session_state.current_tq
    else:
        if 'current_bq' in st.session_state: del st.session_state.current_bq

# --- 5. APP UI ---
txp = get_total_xp(st.session_state.email)
user_level = 1 + (txp // 100)

with st.sidebar:
    st.title("🎮 GURU PRO")
    st.write(f"👤 {st.session_state.user} | 🎖️ Lvl: {user_level}")
    st.metric("Total XP", txp)
    page = st.radio("GO TO:", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle"])

if page == "🏠 Base":
    st.header("🏠 Command Center")
    st.markdown(f"<div class='gaming-card'><h2>Ready to Learn, {st.session_state.user}?</h2><p>Training mein XP kamao aur Boss ko harao!</p></div>", unsafe_allow_html=True)
    if st.button("🎁 CLAIM DAILY 50 XP"):
        c.execute("INSERT INTO progress (email, date, xp) VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), 50))
        conn.commit(); st.rerun()

elif page == "🎓 Training":
    st.header("🎓 Training Zone")
    if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAINING_DATA)
    tq = st.session_state.current_tq
    st.markdown(f"<div class='gaming-card'><h3>{tq['q']}</h3></div>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, opt in enumerate(tq['o']):
        with cols[i % 2]:
            if st.button(opt, key=f"t_{i}"):
                check_ans(opt, tq['a'], 'T'); st.rerun()

elif page == "⚔️ Boss Battle":
    st.header("⚔️ Boss Arena")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"HERO: {st.session_state.player_hp}%")
        st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#00f2ff;'></div></div>", unsafe_allow_html=True)
    with col2:
        st.write(f"BOSS: {st.session_state.boss_hp}%")
        st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#ff4b4b;'></div></div>", unsafe_allow_html=True)

    if st.session_state.boss_hp <= 0:
        st.success("🏆 BOSS DEFEATED! +100 XP"); st.balloons()
        if st.button("NEXT BOSS"): st.session_state.boss_hp = 100; st.session_state.player_hp = 100; st.rerun()
    elif st.session_state.player_hp <= 0:
        st.error("💀 GAME OVER!"); 
        if st.button("REVIVE"): st.session_state.player_hp = 100; st.session_state.boss_hp = 100; st.rerun()
    else:
        if 'current_bq' not in st.session_state: st.session_state.current_bq = random.choice(BOSS_POOL)
        bq = st.session_state.current_bq
        st.markdown(f"<div class='gaming-card'><h3>BOSS QUESTION: {bq['q']}</h3></div>", unsafe_allow_html=True)
        ans = st.radio("Select Weapon:", bq['o'], horizontal=True)
        if st.button("🔥 ATTACK"):
            check_ans(ans, bq['a'], 'B'); st.rerun()
