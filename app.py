import streamlit as st
import random
import time

# --- INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'energy' not in st.session_state: st.session_state.energy = 100
if 'gems' not in st.session_state: st.session_state.gems = 0

# --- NEON UI ---
st.set_page_config(page_title="Neon English Warrior", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Roboto:wght@300;700&display=swap');
    
    .stApp { background: radial-gradient(circle, #1a1a2e, #16213e, #0f3460); color: #e94560; }
    h1, h2, h3 { font-family: 'Bungee', cursive; color: #00f2ff; text-shadow: 2px 2px #ff0055; }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid #00f2ff;
        border-radius: 20px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px #00f2ff;
    }
    .question-box {
        background: #16213e;
        border-left: 10px solid #e94560;
        padding: 30px;
        font-size: 24px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stButton>button {
        background: #e94560 !important;
        color: white !important;
        font-family: 'Bungee';
        font-size: 20px !important;
        transition: 0.3s;
        border: none !important;
        width: 100%;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 20px #e94560; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER STATS ---
st.title("⚡ NEON ENGLISH WARRIOR")
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"<div class='stat-box'><h3>🏆 XP</h3><h1>{st.session_state.xp}</h1></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='stat-box'><h3>⚡ ENERGY</h3><h1>{st.session_state.energy}%</h1></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='stat-box'><h3>💎 GEMS</h3><h1>{st.session_state.gems}</h1></div>", unsafe_allow_html=True)

st.write("---")

# --- MAIN GAMEPLAY ---
tab1, tab2, tab3 = st.tabs(["🔥 FIGHT", "🏪 SHOP", "🏆 LEADERBOARD"])

with tab1:
    if st.session_state.energy <= 0:
        st.error("Energy Khatam! Shop se energy drink lo.")
    else:
        st.subheader("👾 Monster is attacking! Solve to Hit!")
        
        words = [
            {"word": "GIGANTIC", "options": ["Small", "Huge", "Weak"], "answer": "Huge"},
            {"word": "CURIOUS", "options": ["Bored", "Eager to know", "Angry"], "answer": "Eager to know"},
            {"word": "ANXIOUS", "options": ["Happy", "Worried", "Sleepy"], "answer": "Worried"}
        ]
        
        current = random.choice(words)
        st.markdown(f"<div class='question-box'>What is the meaning of: <b>{current['word']}</b>?</div>", unsafe_allow_html=True)
        
        choice = st.radio("Choose your weapon:", current['options'], horizontal=True)
        
        if st.button("💥 LAUNCH ATTACK"):
            with st.spinner('Attacking...'):
                time.sleep(0.5)
                if choice == current['answer']:
                    st.session_state.xp += 50
                    st.session_state.energy -= 10
                    st.session_state.gems += 1
                    st.balloons()
                    st.success(f"CRITICAL HIT! +50 XP | +1 Gem")
                else:
                    st.session_state.energy -= 20
                    st.error("MISS! Monster ne aapko hit kiya. -20 Energy")
            st.rerun()

with tab2:
    st.subheader("🏪 Neon Shop")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("🧪 Energy Potion (Cost: 2 Gems)")
        if st.button("Buy Energy"):
            if st.session_state.gems >= 2:
                st.session_state.gems -= 2
                st.session_state.energy = 100
                st.success("Energy Full!")
            else:
                st.warning("Gems kam hain!")

with tab3:
    st.subheader("🏆 Global Warriors")
    st.table([{"Rank": "1", "Name": "Rohan", "XP": "5500"}, {"Rank": "2", "Name": "You", "XP": st.session_state.xp}])
