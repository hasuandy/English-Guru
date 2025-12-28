import streamlit as st
import sqlite3
from datetime import date
import random
import time

# ==========================================
# 🛠️ SETTINGS & DATABASE
# ==========================================
DEV_MODE = True 
DB_NAME = 'english_guru_pro_v37.db'

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (email TEXT, item TEXT, count INTEGER, UNIQUE(email, item))''') 
    c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
    conn.commit()

init_db()

# --- Data Pool (Merged 50+ Questions) ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
    {"q": "Synonym of 'HAPPY'?", "o": ["Sad", "Joyful", "Angry", "Brave"], "a": "Joyful"},
    {"q": "Antonym of 'BRAVE'?", "o": ["Strong", "Cowardly", "Fast", "Quiet"], "a": "Cowardly"},
    {"q": "Past tense of 'Eat'?", "o": ["Eaten", "Eats", "Ate", "Eating"], "a": "Ate"},
    {"q": "Synonym of 'LARGE'?", "o": ["Tiny", "Huge", "Soft", "Hard"], "a": "Huge"},
    {"q": "Plural of 'Child'?", "o": ["Childs", "Childrens", "Children", "Childes"], "a": "Children"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Steady"], "a": "Quick"},
    {"q": "Opposite of 'BEAUTIFUL'?", "o": ["Pretty", "Ugly", "Nice", "Clean"], "a": "Ugly"},
    {"q": "I ____ a student.", "o": ["is", "am", "are", "be"], "a": "am"},
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"}
    # ... (Aap aur questions bhi add kar sakte hain)
]

# --- Session State ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Tester_Hero", "test@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

# --- UI CONFIG ---
st.set_page_config(page_title="English Guru Pro", page_icon="🎓", layout="wide")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #0e1117; color: white; font-family: 'Rajdhani', sans-serif; }}
    .stat-card {{ background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 20px; border-left: 5px solid {st.session_state.theme}; text-align: center; }}
    .stat-value {{ font-family: 'Bungee'; font-size: 24px; color: {st.session_state.theme}; }}
    .main-card {{ background: linear-gradient(145deg, #1e2130, #161922); padding: 25px; border-radius: 20px; border: 1px solid #333; }}
    .stButton>button {{ background: linear-gradient(45deg, {st.session_state.theme}, #7000ff); color: white !important; font-family: 'Bungee'; border: none; border-radius: 10px; transition: 0.3s; }}
    .stButton>button:hover {{ transform: scale(1.05); box-shadow: 0 0 15px {st.session_state.theme}; }}
    </style>
    """, unsafe_allow_html=True)

# --- Helpers ---
def get_total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email = ?", (email,))
    res = c.fetchone()[0]
    return res if res else 0

def check_training_answer(user_choice, correct_answer):
    if user_choice.replace("✨ ", "") == correct_answer:
        st.session_state.combo += 1
        gain = 10 if st.session_state.combo < 3 else 20
        c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, str(date.today()), gain))
        conn.commit()
        st.toast(f"✅ Correct! +{gain} XP (Combo: {st.session_state.combo})", icon="🔥")
    else:
        st.session_state.combo = 0
        st.toast(f"❌ Wrong! Correct: {correct_answer}", icon="💀")
    if 'current_tq' in st.session_state: del st.session_state.current_tq

# ==========================================
# 🚀 MAIN APP LOGIC
# ==========================================
if st.session_state.logged_in:
    txp = get_total_xp(st.session_state.email)
    user_level = 1 + (txp // 100)
    xp_in_level = txp % 100
    
    with st.sidebar:
        st.markdown(f"<h1 style='font-family:Bungee; color:{st.session_state.theme};'>GURU V37</h1>", unsafe_allow_html=True)
        st.write(f"🎖️ Lvl: {user_level} | 🔥 Combo: {st.session_state.combo}")
        page = st.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🛒 Shop", "🏆 Hall of Fame"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.rerun()

    # --- 🏠 DASHBOARD ---
    if page == "🏠 Dashboard":
        st.markdown(f"<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f"<div class='stat-card'><small>LEVEL</small><div class='stat-value'>{user_level}</div></div>", unsafe_allow_html=True)
        with col2: st.markdown(f"<div class='stat-card'><small>TOTAL XP</small><div class='stat-value'>{txp}</div></div>", unsafe_allow_html=True)
        with col3: st.markdown(f"<div class='stat-card' style='border-left-color:#ff4b4b;'><small>COMBO</small><div class='stat-value'>🔥 {st.session_state.combo}</div></div>", unsafe_allow_html=True)
        with col4: 
            c.execute("SELECT COUNT(*) FROM dictionary WHERE email=?", (st.session_state.email,))
            st.markdown(f"<div class='stat-card' style='border-left-color:#7000ff;'><small>WORDS</small><div class='stat-value'>{c.fetchone()[0]}</div></div>", unsafe_allow_html=True)

        st.write("### 🎯 Level Progress")
        st.progress(max(0.0, min(xp_in_level / 100.0, 1.0)))
        
        c_left, c_right = st.columns([2, 1])
        with c_left:
            st.subheader("📜 History")
            history = c.execute("SELECT date, xp FROM progress WHERE email=? ORDER BY rowid DESC LIMIT 3", (st.session_state.email,)).fetchall()
            for d, x in history: st.info(f"📅 {d}: {x} XP")
        with c_right:
            st.subheader("🎁 Gift")
            today = str(date.today())
            c.execute("SELECT completed FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
            if not c.fetchone():
                if st.button("CLAIM 50 XP"):
                    c.execute("INSERT INTO daily_tasks VALUES (?, ?, ?)", (st.session_state.email, today, 1))
                    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (st.session_state.email, today, 50))
                    conn.commit(); st.balloons(); st.rerun()
            else: st.success("Gift Claimed!")

    # --- 🎓 TRAINING ---
    elif page == "🎓 Training":
        st.markdown(f"<h1 style='font-family:Bungee;'>🎓 TRAINING</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🎯 MCQs", "📖 DICTIONARY"])
        with t1:
            if 'current_tq' not in st.session_state: st.session_state.current_tq = random.choice(TRAINING_DATA)
            tq = st.session_state.current_tq
            st.markdown(f"<div class='main-card' style='text-align:center;'><h2>{tq['q']}</h2></div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, opt in enumerate(tq['o']):
                with cols[i%2]: 
                    if st.button(f"✨ {opt}", key=f"t_{i}", use_container_width=True):
                        check_training_answer(opt, tq['a']); st.rerun()
        with t2:
            w = st.text_input("New Word")
            m = st.text_input("Meaning")
            if st.button("SAVE"):
                if w and m:
                    c.execute("INSERT INTO dictionary VALUES (?,?,?)", (st.session_state.email, w, m))
                    conn.commit(); st.success("Added!")

    # --- ⚔️ BOSS BATTLE ---
    elif page == "⚔️ Boss Battle":
        st.markdown("<h1 style='color:#ff4b4b; font-family:Bungee; text-align:center;'>👹 MONSTER ARENA</h1>", unsafe_allow_html=True)
        boss_max = 100 + (user_level * 25)
        
        # Safe Progress Calculations
        p_val = max(0.0, min(st.session_state.player_hp / 100.0, 1.0))
        b_val = max(0.0, min(st.session_state.boss_hp / boss_max, 1.0))
        
        col_p, col_b = st.columns(2)
        with col_p:
            st.write(f"🛡️ HERO: {int(p_val*100)}%")
            st.progress(p_val)
        with col_b:
            st.write(f"👾 BOSS: {int(b_val*100)}%")
            st.progress(b_val)
        
        if st.session_state.boss_hp <= 0:
            st.balloons(); st.success("Victory!")
            if st.button("SPAWN NEXT"):
                st.session_state.boss_hp = boss_max + 50
                st.session_state.player_hp = 100
                st.rerun()
        elif st.session_state.player_hp <= 0:
            st.error("Defeated!"); 
            if st.button("REVIVE"): st.session_state.player_hp = 100; st.rerun()
        else:
            if 'bq' not in st.session_state: st.session_state.bq = random.choice(TRAINING_DATA)
            st.markdown(f"<div class='main-card' style='text-align:center;'><h3>{st.session_state.bq['q']}</h3></div>", unsafe_allow_html=True)
            ans = st.radio("Select Attack:", st.session_state.bq['o'], horizontal=True)
            if st.button("🔥 EXECUTE ATTACK"):
                if ans == st.session_state.bq['a']:
                    st.session_state.boss_hp -= 35; st.toast("CRITICAL HIT!")
                else:
                    st.session_state.player_hp -= 20; st.toast("BOSS ATTACKED!")
                del st.session_state.bq; st.rerun()

    # --- 🛒 SHOP ---
    elif page == "🛒 Shop":
        st.title("🛒 ITEM SHOP")
        st.write(f"Credits: {txp} XP")
        if st.button("Buy Shield (50 XP)"):
            if txp >= 50:
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), -50))
                c.execute("INSERT INTO inventory VALUES (?, '🛡️ Shield', 1) ON CONFLICT(email, item) DO UPDATE SET count=count+1", (st.session_state.email,))
                conn.commit(); st.success("Bought!"); st.rerun()

    # --- 🏆 HALL OF FAME ---
    elif page == "🏆 Hall of Fame":
        st.markdown("<h1 style='font-family:Bungee; text-align:center;'>🏆 TOP GURUS</h1>", unsafe_allow_html=True)
        data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC LIMIT 10").fetchall()
        for i, row in enumerate(data, 1):
            color = "gold" if i==1 else "silver" if i==2 else "#cd7f32" if i==3 else "white"
            st.markdown(f"<div style='padding:10px; border-bottom:1px solid #333; color:{color};'>#{i} {row[0]} — {row[1]} XP</div>", unsafe_allow_html=True)
