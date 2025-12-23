import streamlit as st
import random
import time

# --- 1. SYSTEM SETUP ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# --- 2. QUESTIONS ---
questions = [
    {"q": "I ____ a student.", "a": ["am", "is", "are"], "c": "am"},
    {"q": "They ____ playing football.", "a": ["is", "am", "are"], "c": "are"},
    {"q": "Apple is a ____.", "a": ["fruit", "animal", "bird"], "c": "fruit"},
    {"q": "Sun rises in the ____.", "a": ["West", "East", "North"], "c": "East"}
]

# --- 3. THE "INSTA-MODERN" CSS ---
st.set_page_config(page_title="English Guru", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background-color: #0e1117; }
    
    .main-title {
        font-size: 3rem; font-weight: 600; text-align: center;
        background: -webkit-linear-gradient(#00dbde, #fc00ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 40px;
    }
    
    .stat-card {
        background: #161b22; border-radius: 15px; padding: 20px;
        border: 1px solid #30363d; text-align: center; transition: 0.3s;
    }
    .stat-card:hover { border-color: #fc00ff; transform: translateY(-5px); }
    
    .question-box {
        background: #1c2128; border-radius: 20px; padding: 30px;
        margin: 20px 0; border-left: 5px solid #00dbde;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #00dbde, #fc00ff) !important;
        border: none !important; color: white !important; font-weight: 600 !important;
        border-radius: 10px !important; height: 3em !important; width: 100%;
    }
    
    .badge {
        display: inline-block; padding: 5px 15px; border-radius: 20px;
        background: rgba(252, 0, 255, 0.1); color: #fc00ff; font-weight: 600;
        margin: 5px; border: 1px solid #fc00ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TOP NAVIGATION ---
st.markdown("<h1 class='main-title'>English Guru</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='stat-card'>✨<br><small>TOTAL XP</small><br><b>{st.session_state.xp}</b></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='stat-card'>🔥<br><small>STREAK</small><br><b>{st.session_state.xp // 100}</b></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='stat-card'>👹<br><small>BOSS HP</small><br><b>{st.session_state.boss_hp}</b></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='stat-card'>📖<br><small>WORDS</small><br><b>{len(st.session_state.vault)}</b></div>", unsafe_allow_html=True)

st.write("---")

# --- 5. CONTENT AREA ---
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown("<div class='question-box'>", unsafe_allow_html=True)
    q = questions[st.session_state.q_idx % len(questions)]
    st.subheader("Challenge of the Moment")
    st.write(f"### {q['q']}")
    ans = st.radio("Pick the right one:", q['a'], key=f"q_{st.session_state.q_idx}")
    
    if st.button("Submit Answer 🚀"):
        if ans == q['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.balloons()
            st.success("Great job! -100 HP to Boss.")
        else:
            st.error("Oops! Wrong answer.")
        
        st.session_state.q_idx += 1
        time.sleep(1)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with c_right:
    st.write("### 🏅 Achievements")
    if len(st.session_state.vault) >= 1: st.markdown("<span class='badge'>📖 Word Learner</span>", unsafe_allow_html=True)
    if st.session_state.xp >= 200: st.markdown("<span class='badge'>⚔️ Warrior</span>", unsafe_allow_html=True)
    if not st.session_state.vault and st.session_state.xp < 200: st.write("No badges yet.")
    
    st.write("---")
    st.write("### 🔒 Word Vault")
    w = st.text_input("New Word")
    m = st.text_input("Meaning")
    if st.button("Add Word"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            st.rerun()

if st.sidebar.button("Reset Everything"):
    st.session_state.clear()
    st.rerun()
