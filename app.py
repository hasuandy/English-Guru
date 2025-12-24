import streamlit as st
import random
import time

# ==========================================
# 1. SESSION STATE (Database ki jagah ye use hoga)
# ==========================================
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'user' not in st.session_state: st.session_state.user = "Hero Warrior"
if 'avatar' not in st.session_state: st.session_state.avatar = "Ninja"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'combo' not in st.session_state: st.session_state.combo = 0

# ==========================================
# 🎨 ASSETS
# ==========================================
AVATARS = {
    "Ninja": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    "Robot": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    "Monster": "https://cdn-icons-png.flaticon.com/512/616/616412.png"
}

# ==========================================
# ✨ STYLING
# ==========================================
st.set_page_config(page_title="English Guru V42", layout="wide")
st.markdown(f"""
    <style>
    .stApp {{ background: #0e1117; color: white; }}
    .gaming-card {{ 
        background: rgba(255,255,255,0.05); 
        border: 2px solid #00f2ff; 
        border-radius: 15px; 
        padding: 20px; 
        text-align: center; 
    }}
    .stButton>button {{ width: 100%; border-radius: 10px; background: #00f2ff; color: black; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🎮 NAVIGATION
# ==========================================
with st.sidebar:
    st.image(AVATARS[st.session_state.avatar], width=100)
    st.title(st.session_state.user)
    st.metric("Total XP", st.session_state.xp)
    page = st.radio("Menu", ["Base", "Training", "Boss Battle", "Settings"])
    
    if st.button("🔄 FULL RESET"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# 🏠 PAGE: BASE
# ==========================================
if page == "Base":
    st.header("🏠 Home Base")
    st.markdown(f"<div class='gaming-card'><h1>Welcome {st.session_state.user}</h1><p>Start training to earn XP and defeat the Boss!</p></div>", unsafe_allow_html=True)

# ==========================================
# 🎓 PAGE: TRAINING
# ==========================================
elif page == "Training":
    st.header("🎓 Fast Training")
    q = {"q": "Opposite of 'BIG'?", "o": ["Large", "Small", "Tall", "Wide"], "a": "Small"}
    
    st.markdown(f"<div class='gaming-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)
    ans = st.selectbox("Select Answer:", q["o"])
    
    if st.button("Submit"):
        if ans == q["a"]:
            st.session_state.xp += 10
            st.success("✅ Correct! +10 XP added.")
            st.balloons()
        else:
            st.error("❌ Wrong! Try again.")

# ==========================================
# ⚔️ PAGE: BOSS BATTLE
# ==========================================
elif page == "Boss Battle":
    st.header("⚔️ Boss Fight")
    
    col1, col2 = st.columns(2)
    with col1: st.metric("Player HP", f"{st.session_state.player_hp}%")
    with col2: st.metric("Boss HP", f"{st.session_state.boss_hp}%")
    
    if st.button("🔥 SUPER ATTACK"):
        st.session_state.boss_hp -= 25
        if st.session_state.boss_hp <= 0:
            st.success("🏆 YOU WON! Boss Defeated!")
            st.session_state.boss_hp = 100
            st.session_state.xp += 50
        st.rerun()

# ==========================================
# ⚙️ PAGE: SETTINGS
# ==========================================
elif page == "Settings":
    st.header("⚙️ Profile Settings")
    
    new_name = st.text_input("Change Name", value=st.session_state.user)
    if st.button("Update Name"):
        st.session_state.user = new_name
        st.rerun()
        
    st.divider()
    st.write("### Choose Avatar")
    acols = st.columns(3)
    for i, (name, url) in enumerate(AVATARS.items()):
        with acols[i]:
            st.image(url, width=60)
            if st.button(f"Pick {name}"):
                st.session_state.avatar = name
                st.rerun()
