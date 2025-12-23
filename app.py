import streamlit as st
import random
import time

# --- 1. SESSION STATE ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# --- 2. QUESTIONS ---
questions = [
    {"q": "Choose the correct: 'She ____ English very well.'", "a": ["speak", "speaks", "speaking"], "c": "speaks"},
    {"q": "Past tense of 'Buy' is:", "a": ["Bought", "Buyed", "Buying"], "c": "Bought"},
    {"q": "Opposite of 'Success' is:", "a": ["Winner", "Failure", "Victory"], "c": "Failure"},
    {"q": "Correct spelling:", "a": ["Believe", "Beleive", "Belive"], "c": "Believe"},
    {"q": "I ____ a movie now.", "a": ["watch", "am watching", "watched"], "c": "am watching"}
]

# --- 3. PREMIUM CSS (Modern & Sleek) ---
st.set_page_config(page_title="English Guru Pro", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&family=Bungee&display=swap');
    
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; font-family: 'Poppins', sans-serif; }
    
    .main-header { font-family: 'Bungee'; font-size: 3.5rem; text-align: center; color: #FFD700; text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); margin-bottom: 30px; }
    
    .card { background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); margin-bottom: 20px; }
    
    .stat-text { font-size: 1.1rem; color: #b0b0b0; text-transform: uppercase; letter-spacing: 2px; }
    .stat-val { font-size: 2.2rem; font-weight: 700; color: #FFD700; }
    
    .stButton>button { background: linear-gradient(90deg, #FFD700, #FFA500) !important; color: black !important; font-weight: bold !important; border-radius: 30px !important; border: none !important; padding: 10px 30px !important; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TOP BAR (STATS) ---
st.markdown("<h1 class='main-header'>ENGLISH GURU</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='card'><span class='stat-text'>🏆 XP</span><br><span class='stat-val'>{st.session_state.xp}</span></div>", unsafe_allow_html=True)
with c2: 
    rank = "Trainee" if st.session_state.xp < 250 else "Elite"
    st.markdown(f"<div class='card'><span class='stat-text'>🎖️ Rank</span><br><span class='stat-val'>{rank}</span></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='card'><span class='stat-text'>👹 Boss</span><br><span class='stat-val'>{st.session_state.boss_hp}</span></div>", unsafe_allow_html=True)

# --- 5. MAIN ACTION AREA ---
col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚔️ Battle Arena")
    q = questions[st.session_state.q_idx % len(questions)]
    st.write(f"### {q['q']}")
    ans = st.radio("Choose your answer:", q['a'], key=f"q_{st.session_state.q_idx}")
    
    if st.button("STRIKE NOW!"):
        if ans == q['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.success("Correct Strike! +50 XP")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error("Missed! Try again.")
        
        st.session_state.q_idx += 1
        time.sleep(0.5)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📚 Vault")
    w = st.text_input("New Word")
    m = st.text_input("Meaning")
    if st.button("Save Knowledge"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            st.toast("Saved!")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Simple Achievement Badges
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏅 Badges")
    if len(st.session_state.vault) >= 1: st.write("✅ Scholar")
    if st.session_state.xp >= 200: st.write("✅ Warrior")
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("Reset Game"):
    st.session_state.clear()
    st.rerun()
