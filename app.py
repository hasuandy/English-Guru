import streamlit as st
import sqlite3
from datetime import date
import random

# =============================
# DEV SETTINGS
DEV_MODE = True
# =============================

# ---------- DATABASE ----------
conn = sqlite3.connect("english_guru_pro.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    username TEXT,
    password TEXT,
    xp INTEGER DEFAULT 0
)""")

c.execute("""CREATE TABLE IF NOT EXISTS progress (
    email TEXT,
    date TEXT,
    xp INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS dictionary (
    email TEXT,
    word TEXT,
    meaning TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS inventory (
    email TEXT,
    item TEXT,
    count INTEGER,
    UNIQUE(email, item)
)""")

c.execute("""CREATE TABLE IF NOT EXISTS daily_tasks (
    email TEXT,
    task_date TEXT,
    completed INTEGER
)""")

conn.commit()

# ---------- SESSION ----------
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "combo" not in st.session_state: st.session_state.combo = 0
if "boss_hp" not in st.session_state: st.session_state.boss_hp = 100
if "player_hp" not in st.session_state: st.session_state.player_hp = 100
if "theme" not in st.session_state: st.session_state.theme = "#00f2ff"

# ---------- DEV AUTO LOGIN ----------
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.user = "Tester_Hero"
    st.session_state.email = "test@guru.com"
    c.execute(
        "INSERT OR IGNORE INTO users (email, username) VALUES (?, ?)",
        (st.session_state.email, st.session_state.user)
    )
    conn.commit()

# ---------- DATA ----------
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
]

BOSS_POOL = [
    {"q": "Meaning of 'AMBIGUOUS'?", "o": ["Clear", "Uncertain", "Huge", "Bright"], "a": "Uncertain"},
    {"q": "Synonym of 'METICULOUS'?", "o": ["Careless", "Precise", "Fast", "Noisy"], "a": "Precise"},
]

# ---------- FUNCTIONS ----------
def total_xp(email):
    c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (email,))
    return c.fetchone()[0] or 0

def add_xp(email, amount):
    c.execute("INSERT INTO progress VALUES (?, ?, ?)", (email, str(date.today()), amount))
    c.execute("UPDATE users SET xp = xp + ? WHERE email=?", (amount, email))
    conn.commit()

# ---------- UI ----------
st.set_page_config("English Guru Pro", "🎓", "wide")

st.markdown("""
<style>
.stApp { background: radial-gradient(circle,#1a1a2e,#020205); color:white }
button { border-radius:10px !important }
</style>
""", unsafe_allow_html=True)

# ---------- APP ----------
if st.session_state.logged_in:
    xp = total_xp(st.session_state.email)
    level = 1 + xp // 100

    with st.sidebar:
        st.header(st.session_state.user)
        st.write(f"🎖 Level: {level}")
        st.write(f"💰 XP: {xp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss", "🛒 Shop", "🏆 Leaderboard"])

    # ---------- BASE ----------
    if page == "🏠 Base":
        st.title("COMMAND CENTER")
        today = str(date.today())
        c.execute("SELECT * FROM daily_tasks WHERE email=? AND task_date=?", (st.session_state.email, today))
        if not c.fetchone():
            if st.button("CLAIM DAILY 50 XP"):
                c.execute("INSERT INTO daily_tasks VALUES (?, ?, 1)", (st.session_state.email, today))
                add_xp(st.session_state.email, 50)
                st.success("+50 XP")
                st.rerun()

    # ---------- TRAINING ----------
    elif page == "🎓 Training":
        st.title("TRAINING ZONE")

        if "q" not in st.session_state:
            st.session_state.q = random.choice(TRAINING_DATA)

        q = st.session_state.q
        st.subheader(q["q"])
        for opt in q["o"]:
            if st.button(opt):
                if opt == q["a"]:
                    st.session_state.combo += 1
                    gain = 10 if st.session_state.combo < 3 else 20
                    add_xp(st.session_state.email, gain)
                    st.success(f"+{gain} XP")
                else:
                    st.session_state.combo = 0
                    st.error("Wrong!")
                del st.session_state.q
                st.rerun()

    # ---------- BOSS ----------
    elif page == "⚔️ Boss":
        max_hp = 100 + level * 25
        if st.session_state.boss_hp > max_hp:
            st.session_state.boss_hp = max_hp

        st.title("BOSS ARENA")
        st.write(f"❤️ Player: {st.session_state.player_hp}")
        st.write(f"💀 Boss: {st.session_state.boss_hp}/{max_hp}")

        if "boss_q" not in st.session_state:
            st.session_state.boss_q = random.choice(BOSS_POOL)

        bq = st.session_state.boss_q
        ans = st.radio(bq["q"], bq["o"])

        if st.button("ATTACK"):
            if ans == bq["a"]:
                st.session_state.boss_hp -= 40
            else:
                st.session_state.player_hp -= 20

            del st.session_state.boss_q

            if st.session_state.boss_hp <= 0:
                add_xp(st.session_state.email, 100)
                st.balloons()
                st.success("+100 XP")
                st.session_state.boss_hp = max_hp
                st.session_state.player_hp = 100

            if st.session_state.player_hp <= 0:
                st.error("DEFEATED")
                st.session_state.player_hp = 100

            st.rerun()

    # ---------- SHOP ----------
    elif page == "🛒 Shop":
        st.title("SHOP")
        if st.button("Buy Shield (50 XP)"):
            if xp >= 50:
                add_xp(st.session_state.email, -50)
                c.execute("""
                INSERT INTO inventory VALUES (?, '🛡️ Shield', 1)
                ON CONFLICT(email,item) DO UPDATE SET count=count+1
                """, (st.session_state.email,))
                conn.commit()
                st.success("Purchased!")
                st.rerun()
            else:
                st.warning("Not enough XP")

    # ---------- LEADERBOARD ----------
    elif page == "🏆 Leaderboard":
        st.title("LEADERBOARD")
        rows = c.execute("""
        SELECT username, xp FROM users ORDER BY xp DESC
        """).fetchall()

        for i, r in enumerate(rows):
            st.write(f"#{i+1} {r[0]} - {r[1]} XP")
