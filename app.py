import streamlit as st
import sqlite3
from datetime import date
import random

# =====================
# DEV MODE
DEV_MODE = True
# =====================

# ---------- DATABASE ----------
conn = sqlite3.connect("english_guru_final.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    username TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS progress (
    email TEXT,
    date TEXT,
    xp INTEGER
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

# ---------- DEV AUTO LOGIN ----------
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.email = "test@guru.com"
    st.session_state.user = "Tester_Hero"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?)",
              (st.session_state.email, st.session_state.user))
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
def add_xp(amount):
    c.execute("INSERT INTO progress VALUES (?, ?, ?)",
              (st.session_state.email, str(date.today()), amount))
    conn.commit()

def total_xp():
    c.execute("SELECT COALESCE(SUM(xp),0) FROM progress WHERE email=?",
              (st.session_state.email,))
    return c.fetchone()[0]

# ---------- UI ----------
st.set_page_config("English Guru Pro", "🎓", "wide")
st.title("🎓 English Guru Pro")

# ---------- APP ----------
if st.session_state.logged_in:
    xp = total_xp()
    level = 1 + xp // 100

    with st.sidebar:
        st.header(st.session_state.user)
        st.write(f"🎖 Level: {level}")
        st.write(f"💰 XP: {xp}")
        page = st.radio("MENU", ["🏠 Base", "🎓 Training", "⚔️ Boss", "🏆 Leaderboard"])

    # ---------- BASE ----------
    if page == "🏠 Base":
        st.subheader("Command Center")
        today = str(date.today())
        c.execute("SELECT * FROM daily_tasks WHERE email=? AND task_date=?",
                  (st.session_state.email, today))
        if not c.fetchone():
            if st.button("Claim Daily 50 XP"):
                c.execute("INSERT INTO daily_tasks VALUES (?, ?, 1)",
                          (st.session_state.email, today))
                add_xp(50)
                st.success("+50 XP")
                st.rerun()
        else:
            st.info("Daily reward already claimed")

    # ---------- TRAINING ----------
    elif page == "🎓 Training":
        st.subheader("Training Zone")

        if "q" not in st.session_state:
            st.session_state.q = random.choice(TRAINING_DATA)

        q = st.session_state.q
        st.write("🔥 Combo:", st.session_state.combo)
        st.markdown(f"### {q['q']}")

        for opt in q["o"]:
            if st.button(opt):
                if opt == q["a"]:
                    st.session_state.combo += 1
                    gain = 10 if st.session_state.combo < 3 else 20
                    add_xp(gain)
                    st.success(f"+{gain} XP")
                else:
                    st.session_state.combo = 0
                    st.error("Wrong Answer")

                del st.session_state.q
                st.rerun()

    # ---------- BOSS ----------
    elif page == "⚔️ Boss":
        max_hp = 100 + level * 25
        if st.session_state.boss_hp > max_hp:
            st.session_state.boss_hp = max_hp

        st.subheader("Boss Battle")
        st.write(f"❤️ Player HP: {st.session_state.player_hp}")
        st.write(f"💀 Boss HP: {st.session_state.boss_hp}/{max_hp}")

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
                add_xp(100)
                st.balloons()
                st.success("Boss Defeated! +100 XP")
                st.session_state.boss_hp = max_hp
                st.session_state.player_hp = 100

            if st.session_state.player_hp <= 0:
                st.error("You Died! Revived.")
                st.session_state.player_hp = 100

            st.rerun()

    # ---------- LEADERBOARD (FIXED) ----------
    elif page == "🏆 Leaderboard":
        st.subheader("Leaderboard")

        rows = c.execute("""
        SELECT u.username, COALESCE(SUM(p.xp),0) AS total_xp
        FROM users u
        LEFT JOIN progress p ON u.email = p.email
        GROUP BY u.email
        ORDER BY total_xp DESC
        """).fetchall()

        if not rows:
            st.info("No players yet")
        else:
            for i, r in enumerate(rows):
                st.write(f"#{i+1} 🏅 {r[0]} — {r[1]} XP")
