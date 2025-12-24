import streamlit as st
import sqlite3
import random
from datetime import date

# =====================
DEV_MODE = True
# =====================

# ---------- DB ----------
conn = sqlite3.connect("english_guru_fun.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)")
conn.commit()

# ---------- SESSION ----------
for k, v in {
    "logged_in": False,
    "combo": 0,
    "boss_hp": 120,
    "player_hp": 100,
    "power": 3,
    "chest": None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- DEV LOGIN ----------
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.email = "test@guru.com"
    st.session_state.user = "Hero_Yashi"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?)",
              (st.session_state.email, st.session_state.user))
    conn.commit()

# ---------- DATA ----------
QUESTIONS = [
    ("Antonym of ANCIENT?", ["Old", "Modern", "Heavy"], "Modern"),
    ("Plural of Mouse?", ["Mouses", "Mice", "Mouse"], "Mice"),
    ("Past tense of Go?", ["Gone", "Went", "Going"], "Went"),
]

BOSS_Q = [
    ("Meaning of AMBIGUOUS?", ["Clear", "Uncertain", "Big"], "Uncertain"),
    ("Synonym of METICULOUS?", ["Careless", "Precise", "Lazy"], "Precise"),
]

# ---------- FUNCTIONS ----------
def add_xp(x):
    c.execute("INSERT INTO progress VALUES (?,?,?)",
              (st.session_state.email, str(date.today()), x))
    conn.commit()

def total_xp():
    c.execute("SELECT COALESCE(SUM(xp),0) FROM progress WHERE email=?",
              (st.session_state.email,))
    return c.fetchone()[0]

# ---------- UI ----------
st.set_page_config("English Guru – FUN MODE", "🎮", "wide")
st.title("🎮 English Guru – FUN MODE")

xp = total_xp()
level = 1 + xp // 100

with st.sidebar:
    st.header(st.session_state.user)
    st.write(f"⭐ Level: {level}")
    st.write(f"💰 XP: {xp}")
    page = st.radio("MENU", ["🎓 Training", "⚔️ Boss Fight", "🏆 Leaderboard"])

# ================= TRAINING =================
if page == "🎓 Training":
    st.subheader("🔥 Training Arena")

    if "q" not in st.session_state:
        q = random.choice(QUESTIONS)
        lucky = random.choice([True, False, False])
        st.session_state.q = q
        st.session_state.lucky = lucky

    q, opts, ans = st.session_state.q
    st.markdown(f"### {q}")
    if st.session_state.lucky:
        st.info("🍀 LUCKY QUESTION → DOUBLE XP!")

    for o in opts:
        if st.button(o):
            if o == ans:
                st.session_state.combo += 1
                gain = 20 if st.session_state.lucky else 10
                add_xp(gain)
                st.success(f"+{gain} XP")

                if st.session_state.combo % 3 == 0:
                    st.session_state.chest = random.choice(
                        ["🟤 Bronze Chest", "🟡 Gold Chest", "💎 Diamond Chest"]
                    )
            else:
                st.session_state.combo = 0
                st.error("Wrong!")

            del st.session_state.q
            st.rerun()

    st.write("🔥 Combo:", st.session_state.combo)

    if st.session_state.chest:
        st.balloons()
        chest = st.session_state.chest
        st.success(f"🎁 You unlocked {chest}")

        if chest == "🟤 Bronze Chest":
            add_xp(20)
        elif chest == "🟡 Gold Chest":
            st.session_state.power += 1
        else:
            add_xp(50)

        st.session_state.chest = None

# ================= BOSS =================
elif page == "⚔️ Boss Fight":
    st.subheader("😈 Boss Arena")

    st.write(f"❤️ Player HP: {st.session_state.player_hp}")
    st.write(f"💀 Boss HP: {st.session_state.boss_hp}")
    st.write(f"🔥 Power Attacks Left: {st.session_state.power}")

    if "bq" not in st.session_state:
        st.session_state.bq = random.choice(BOSS_Q)

    q, opts, ans = st.session_state.bq
    choice = st.radio(q, opts)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⚔️ ATTACK"):
            if choice == ans:
                st.session_state.boss_hp -= 30
            else:
                st.session_state.player_hp -= 20
            del st.session_state.bq
            st.rerun()

    with col2:
        if st.button("🔥 POWER ATTACK") and st.session_state.power > 0:
            if choice == ans:
                st.session_state.boss_hp -= 70
            else:
                st.session_state.player_hp -= 30
            st.session_state.power -= 1
            del st.session_state.bq
            st.rerun()

    if st.session_state.boss_hp <= 0:
        st.balloons()
        add_xp(100)
        st.success("🏆 Boss Defeated! +100 XP")
        st.session_state.boss_hp = 120
        st.session_state.player_hp = 100
        st.session_state.power = 3

    if st.session_state.player_hp <= 0:
        st.error("💀 You Died! Revived.")
        st.session_state.player_hp = 100

# ================= LEADERBOARD =================
elif page == "🏆 Leaderboard":
    st.subheader("🏆 Leaderboard")

    rows = c.execute("""
    SELECT u.username, COALESCE(SUM(p.xp),0)
    FROM users u
    LEFT JOIN progress p ON u.email=p.email
    GROUP BY u.email
    ORDER BY 2 DESC
    """).fetchall()

    for i, r in enumerate(rows):
        st.write(f"#{i+1} 🏅 {r[0]} — {r[1]} XP")
