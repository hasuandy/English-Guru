import streamlit as st
import random
import time

# ==========================================
# 1. 🧠 SMART STATE MANAGEMENT (No Database Needed)
# ==========================================
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'user' not in st.session_state: st.session_state.user = "Hero Warrior"
if 'avatar' not in st.session_state: st.session_state.avatar = "Ninja"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'history' not in st.session_state: st.session_state.history = []

# ==========================================
# 🎨 GRAPHICS & ASSETS
# ==========================================
AVATARS = {
    "Ninja": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    "Robot": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    "Monster": "https://cdn-icons-png.flaticon.com/512/616/616412.png"
}

# ==========================================
# ✨ PRO GAMING UI
# ==========================================
st.set_page_config(page_title="English Guru V43", layout="wide", page_icon="🎮")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }}
    .gaming-card {{ 
        background: rgba(255,255,255,0.05); 
        border: 2px solid #00f2ff; 
        border-radius: 15px; 
        padding: 25px; 
        text-align: center;
        box-shadow: 0 0 20px rgba(0,242,255,0.2);
    }}
    .stButton>button {{ 
        width: 100%; 
        border-radius: 12px; 
        background: linear-gradient(45deg, #00f2ff, #7000ff); 
        color: white !important; 
        font-family: 'Bungee';
        border: none;
        height: 50px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: scale(1.02); box-shadow: 0 0 15px #00f2ff; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🎮 SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image(AVATARS[st.session_state.avatar], width=120)
    st.markdown(f"<h2 style='color:#00f2ff; font-family:Bungee;'>{st.session_state.user}</h2>", unsafe_allow_html=True)
    st.divider()
    st.metric("🎖️ TOTAL XP", st.session_state.xp)
    st.divider()
    page = st.selectbox("CHOOSE MISSION", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "⚙️ Settings"])
    
    st.write("---")
    if st.button("🔄 EMERGENCY RESET"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 🏠 PAGE: BASE
# ==========================================
if page == "🏠 Base":
    st.markdown("<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class='gaming-card'>
            <h3>Welcome Commander</h3>
            <p>Master English to gain power.</p>
            <h2 style='color:#00f2ff;'>LVL {1 + (st.session_state.xp // 100)}</h2>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.image("https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif", width=200)

# ==========================================
# 🎓 PAGE: TRAINING
# ==========================================
elif page == "🎓 Training":
    st.markdown("<h1 style='font-family:Bungee;'>TRAINING ZONE</h1>", unsafe_allow_html=True)
    
    # Fast Question Logic
    questions = [
        {"q": "Meaning of 'VIBRANT'?", "o": ["Dull", "Energetic", "Lazy", "Small"], "a": "Energetic"},
        {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Eating", "Ate", "Eats"], "a": "Ate"}
    ]
    
    q = random.choice(questions)
    st.markdown(f"<div class='gaming-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
    
    ans = st.radio("Select Correct Option:", q["o"])
    
    if st.button("SUBMIT ANSWER"):
        if ans == q["a"]:
            st.session_state.xp += 20
            st.success("🔥 EXCELLENT! +20 XP")
            st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ WRONG! Keep practicing.")

# ==========================================
# ⚔️ PAGE: BOSS BATTLE
# ==========================================
elif page == "⚔️ Boss Battle":
    st.markdown("<h1 style='font-family:Bungee; color:#ff4b4b;'>BOSS ARENA</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: st.metric("Player Health", f"{st.session_state.player_hp}%")
    with c2: st.metric("Boss Health", f"{st.session_state.boss_hp}%")
    
    st.progress(st.session_state.boss_hp / 100)
    
    if st.button("💥 LAUNCH MEGA ATTACK"):
        damage = random.randint(20, 40)
        st.session_state.boss_hp -= damage
        if st.session_state.boss_hp <= 0:
            st.success("🏆 BOSS DEFEATED! You earned 100 XP!")
            st.session_state.xp += 100
            st.session_state.boss_hp = 100
        st.rerun()

# ==========================================
# ⚙️ PAGE: SETTINGS
# ==========================================
elif page == "⚙️ Settings":
    st.markdown("<h1 style='font-family:Bungee;'>PROFILE SETTINGS</h1>", unsafe_allow_html=True)
    
    new_name = st.text_input("Change Hero Name", value=st.session_state.user)
    if st.button("SAVE NAME"):
        st.session_state.user = new_name
        st.rerun()
        
    st.divider()
    st.write("### Choose Your Avatar")
    cols = st.columns(3)
    for i, (name, url) in enumerate(AVATARS.items()):
        with cols[i]:
            st.image(url, width=80)
            if st.button(f"SELECT {name.upper()}"):
                st.session_state.avatar = name
                st.rerun()
