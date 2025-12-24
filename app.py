import streamlit as st
import sqlite3
import random
from datetime import date
import base64

# =====================
DEV_MODE = True
# =====================

# ---------- DATABASE ----------
conn = sqlite3.connect("english_guru_story.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)")
conn.commit()

# ---------- SESSION ----------
defaults = {
    "logged_in": False,
    "level": 1,
    "xp": 0,
    "map_level": 1,
    "q": None
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- DEV LOGIN ----------
if DEV_MODE and not st.session_state.logged_in:
    st.session_state.logged_in = True
    st.session_state.email = "hero@guru.com"
    st.session_state.user = "Hero_Yashi"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?)",
              (st.session_state.email, st.session_state.user))
    conn.commit()

# ---------- SOUNDS (BASE64 SMALL BEEPS) ----------
def play_sound(kind):
    sounds = {
        "correct": "UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA=",
        "wrong": "UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA=",
        "win": "UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA="
    }
    audio = base64.b64decode(sounds[kind])
    st.audio(audio, format="audio/wav")

# ---------- DATA ----------
STORY_MAP = {
    1: {"name": "🌲 Forest of Words", "xp": 30},
    2: {"name": "🏰 Grammar Castle", "xp": 50},
    3: {"name": "🐉 Dragon of Vocabulary", "xp": 100}
}

QUESTIONS = [
    ("Plural of Mouse?", ["Mouses", "Mice", "Mouse"], "Mice"),
    ("Past tense of Go?", ["Gone", "Went", "Going"], "Went"),
    ("Antonym of Hot?", ["Cold", "Warm", "Heat"], "Cold")
]

# ---------- FUNCTIONS ----------
def add_xp(x):
    st.session_state.xp += x
    c.execute("INSERT INTO progress VALUES (?,?,?)",
              (st.session_state.email, str(date.today()), x))
    conn.commit()

# ---------- UI ----------
st.set_page_config("English Guru – Story Mode", "🗺️", "wide")
st.title("🗺️ English Guru – STORY MODE")

with st.sidebar:
    st.header(st.session_state.user)
    st.write(f"⭐ XP: {st.session_state.xp}")
    page = st.radio("MENU", ["🗺️ Story Map", "🎓 Mission", "🏆 Progress"])

# ================= MAP =================
if page == "🗺️ Story Map":
    st.subheader("🌍 World Map")

    for lvl, data in STORY_MAP.items():
        if st.session_state.map_level >= lvl:
            if st.button(f"{data['name']}"):
                st.session_state.current_stage = lvl
                st.session_state.q = random.choice(QUESTIONS)
                st.switch_page("app.py")
        else:
            st.write(f"🔒 {data['name']} (Locked)")

# ================= MISSION =================
elif page == "🎓 Mission":
    if "current_stage" not in st.session_state:
        st.info("Select a location from Map")
    else:
        q, opts, ans = st.session_state.q
        st.markdown(f"### {q}")

        for o in opts:
            if st.button(o):
                if o == ans:
                    reward = STORY_MAP[st.session_state.current_stage]["xp"]
                    add_xp(reward)
                    play_sound("correct")
                    st.success(f"Mission Clear! +{reward} XP")
                    st.session_state.map_level += 1
                    play_sound("win")
                else:
                    play_sound("wrong")
                    st.error("Wrong Answer!")

                del st.session_state.current_stage
                st.rerun()

# ================= PROGRESS =================
elif page == "🏆 Progress":
    st.subheader("🏆 Your Journey")
    st.progress(st.session_state.map_level / len(STORY_MAP))
    st.write(f"Unlocked Areas: {st.session_state.map_level}/{len(STORY_MAP)}")
    st.write(f"Total XP: {st.session_state.xp}")
