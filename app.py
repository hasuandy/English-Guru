import streamlit as st
import random
import time

# --- 1. SYSTEM INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'achievements' not in st.session_state: st.session_state.achievements = set()

# --- 2. MEGA QUESTION BANK ---
questions = [
    {"q": "He ____ a doctor.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "They ____ to the park yesterday.", "a": ["go", "went", "going"], "c": "went"},
    {"q": "She ____ like apples.", "a": ["don't", "doesn't", "isn't"], "c": "doesn't"},
    {"q": "Neither of us ____ ready.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "I have ____ my lunch.", "a": ["eat", "ate", "eaten"], "c": "eaten"},
    {"q": "Choose the correct spelling:", "a": ["Recieve", "Receive", "Receve"], "c": "Receive"},
    {"q": "Look! The baby ____.", "a": ["sleeps", "is sleeping", "sleep"], "c": "is sleeping"}
]

# --- 3. STYLING (The "Pro" Gaming Look) ---
st.set_page_config(page_title="English Guru V43", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Share+Tech+Mono&display=swap');
    
    .stApp { background-color: #0d0d0d; color: #00ff41; font-family: 'Share Tech Mono', monospace; }
    
    .terminal-box {
        border: 2px solid #00ff41;
        padding: 20px;
        border-radius: 5px;
        background: rgba(0, 255, 65, 0.05);
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
        margin-bottom: 20px;
    }
    
    .main-title {
        font-family: 'Bungee';
        font-size: 4rem;
        text-align: center;
        color: #00ff41;
        text-shadow: 2px 2px #ff0055;
    }
    
    .stat-label { color: #ff0055; font-family: 'Bungee'; font-size: 1.2rem; }
    .stat-value { color: #00ff41; font-size: 2.5rem; font-weight: bold; }
    
    /* Hide Streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER & STATS ---
st.markdown("<h1 class='main-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# Top Bar Stats
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='terminal-box'><span class='stat-label'>XP</span><br><span class='stat-value'>{st.session_state.xp}</span></div>", unsafe_allow_html=True)
with c2: 
    rank = "NOOB" if st.session_state.xp < 200 else "PRO" if st.session_state.xp < 500 else "LEGEND"
    st.markdown(f"<div class='terminal-box'><span class='stat-label'>RANK</span><br><span class='stat-value'>{rank}</span></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='terminal-box'><span class='stat-label'>WORDS</span><br><span class='stat-value'>{len(st.session_state.vault)}</span></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='terminal-box'><span class='stat-label'>BOSS HP</span><br><span class='stat-value'>{st.session_state.boss_hp}</span></div>", unsafe_allow_html=True)

# --- 5. BATTLE & VAULT SIDE-BY-SIDE ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown("<div class='terminal-box'>", unsafe_allow_html=True)
    st.subheader("👹 ACTIVE MISSION: BOSS BATTLE")
    
    q_data = questions[st.session_state.q_index % len(questions)]
    st.write(f"### > {q_data['q']}")
    ans = st.radio("SELECT WEAPON:", q_data['a'], key="battle_radio")
    
    if st.button("EXECUTE ATTACK 💥"):
        if ans == q_data['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.success("SUCCESS: 100 DMG DEALT")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error("ERROR: ATTACK FAILED")
        
        st.session_state.q_index += 1
        time.sleep(0.5)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("<div class='terminal-box'>", unsafe_allow_html=True)
    st.subheader("📚 WORD VAULT")
    w = st.text_input("INPUT WORD:")
    m = st.text_input("INPUT MEANING:")
    if st.button("ENCRYPT & SAVE"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            st.success("SAVED")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Achievements Section
    st.markdown("<div class='terminal-box'>", unsafe_allow_html=True)
    st.subheader("🏅 BADGES")
    if len(st.session_state.vault) >= 1: st.write("✅ SCHOLAR")
    if st.session_state.xp >= 200: st.write("✅ WARRIOR")
    if st.session_state.xp >= 500: st.write("✅ MASTER")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer Reset
if st.button("RESET SYSTEM"):
    st.session_state.clear()
    st.rerun()
