import streamlit as st
import random

# --- SESSION STATE (Data Storage) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'user' not in st.session_state: st.session_state.user = "Hero Warrior"
if 'avatar' not in st.session_state: st.session_state.avatar = "Ninja"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100

# --- ASSETS ---
AVATARS = {
    "Ninja": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    "Robot": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    "Monster": "https://cdn-icons-png.flaticon.com/512/616/616412.png"
}

# --- UI SETUP ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .gaming-card { 
        background: rgba(255,255,255,0.05); 
        border: 2px solid #00f2ff; 
        border-radius: 15px; padding: 20px; text-align: center;
    }
    .stButton>button { background: #00f2ff; color: black !important; font-weight: bold; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image(AVATARS[st.session_state.avatar], width=100)
    st.title(st.session_state.user)
    st.write(f"🎖️ XP: {st.session_state.xp}")
    st.divider()
    page = st.radio("Missions", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "⚙️ Settings"])

# --- PAGES ---
if page == "🏠 Base":
    st.header("🏠 Command Center")
    st.markdown(f"<div class='gaming-card'><h2>Welcome {st.session_state.user}</h2><p>Master English and Level Up!</p></div>", unsafe_allow_html=True)

elif page == "🎓 Training":
    st.header("🎓 Vocabulary Training")
    q = {"q": "Opposite of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy"], "a": "Modern"}
    st.subheader(q["q"])
    ans = st.radio("Pick one:", q["o"])
    if st.button("Submit"):
        if ans == q["a"]:
            st.session_state.xp += 10
            st.success("Correct! +10 XP")
            st.balloons()
        else:
            st.error("Wrong! Try again.")

elif page == "⚔️ Boss Battle":
    st.header("⚔️ Boss Fight")
    st.write(f"Boss HP: {st.session_state.boss_hp}%")
    st.progress(st.session_state.boss_hp / 100)
    if st.button("🔥 ATTACK"):
        st.session_state.boss_hp -= 20
        if st.session_state.boss_hp <= 0:
            st.success("Boss Defeated!")
            st.session_state.boss_hp = 100
            st.session_state.xp += 50
        st.rerun()

elif page == "⚙️ Settings":
    st.header("⚙️ Settings")
    new_name = st.text_input("Change Name", st.session_state.user)
    if st.button("Save Name"):
        st.session_state.user = new_name
        st.rerun()
    st.write("### Choose Avatar")
    cols = st.columns(3)
    for i, (name, url) in enumerate(AVATARS.items()):
        with cols[i]:
            st.image(url, width=60)
            if st.button(f"Pick {name}"):
                st.session_state.avatar = name
                st.rerun()
