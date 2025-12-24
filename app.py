import streamlit as st
import random
import time

# 1. 🧠 SESSION STATE (Data Storage)
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'user' not in st.session_state: st.session_state.user = "Hero"
if 'avatar' not in st.session_state: st.session_state.avatar = "Ninja"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

# 2. 🎨 ASSETS
AVATARS = {
    "Ninja": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
    "Robot": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
    "Monster": "https://cdn-icons-png.flaticon.com/512/616/616412.png"
}

# 3. ✨ UI SETUP
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background: radial-gradient(circle, #1a1a2e, #020205); color: white; font-family: 'Rajdhani', sans-serif; }
    .gaming-card { 
        background: rgba(255,255,255,0.05); 
        border: 2px solid #00f2ff; 
        border-radius: 15px; 
        padding: 20px; 
        text-align: center;
        box-shadow: 0 0 15px rgba(0,242,255,0.2);
    }
    .stButton>button { 
        background: linear-gradient(45deg, #00f2ff, #7000ff); 
        color: white !important; 
        font-family: 'Bungee';
        border-radius: 10px;
        border: none;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 🎮 SIDEBAR
with st.sidebar:
    st.image(AVATARS[st.session_state.avatar], width=100)
    st.markdown(f"<h2 style='color:#00f2ff; font-family:Bungee;'>{st.session_state.user}</h2>", unsafe_allow_html=True)
    st.write(f"🎖️ XP: {st.session_state.xp}")
    st.divider()
    page = st.radio("SELECT MISSION", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "⚙️ Settings"])
    
    if st.button("🔄 Reset Game"):
        st.session_state.clear()
        st.rerun()

# 5. 🏠 PAGE: BASE
if page == "🏠 Base":
    st.markdown("<h1 style='font-family:Bungee;'>COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='gaming-card'>
            <h2>Welcome Back, {st.session_state.user}!</h2>
            <p>Master English vocabulary to defeat the final boss.</p>
            <h1 style='color:#00f2ff;'>LEVEL {1 + (st.session_state.xp // 100)}</h1>
        </div>
    """, unsafe_allow_html=True)

# 6. 🎓 PAGE: TRAINING
elif page == "🎓 Training":
    st.markdown("<h1 style='font-family:Bungee;'>TRAINING ZONE</h1>", unsafe_allow_html=True)
    
    q_pool = [
        {"q": "Meaning of 'ENORMOUS'?", "o": ["Very Small", "Huge", "Weak"], "a": "Huge"},
        {"q": "Plural of 'Tooth'?", "o": ["Tooths", "Teeth", "Teeths"], "a": "Teeth"}
    ]
    
    # Simple Question Logic
    if 't_idx' not in st.session_state: st.session_state.t_idx = random.randint(0, len(q_pool)-1)
    tq = q_pool[st.session_state.t_idx]
    
    st.markdown(f"<div class='gaming-card'><h3>{tq['q']}</h3></div>", unsafe_allow_html=True)
    ans = st.radio("Choose correct answer:", tq["o"])
    
    if st.button("SUBMIT"):
        if ans == tq["a"]:
            st.session_state.xp += 20
            st.success("Correct! +20 XP")
            st.balloons()
            del st.session_state.t_idx
            time.sleep(1)
            st.rerun()
        else:
            st.error("Wrong! Try again.")

# 7. ⚔️ PAGE: BOSS BATTLE
elif page == "⚔️ Boss Battle":
    st.markdown("<h1 style='font-family:Bungee; color:#ff4b4b;'>BOSS ARENA</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: st.metric("Player Health", f"{st.session_state.player_hp}%")
    with col2: st.metric("Boss Health", f"{st.session_state.boss_hp}%")
    
    st.progress(st.session_state.boss_hp / 100)
    
    if st.button("🔥 ATTACH BOSS"):
        st.session_state.boss_hp -= 25
        if st.session_state.boss_hp <= 0:
            st.success("Victory! You defeated the Boss!")
            st.session_state.xp += 50
            st.session_state.boss_hp = 100
        st.rerun()

# 8. ⚙️ PAGE: SETTINGS
elif page == "⚙️ Settings":
    st.markdown("<h1 style='font-family:Bungee;'>SETTINGS</h1>", unsafe_allow_html=True)
    new_n = st.text_input("New Name", value=st.session_state.user)
    if st.button("Save Name"):
        st.session_state.user = new_n
        st.rerun()
    
    st.write("### Choose Avatar")
    cols = st.columns(3)
    for i, (name, url) in enumerate(AVATARS.items()):
        with cols[i]:
            st.image(url, width=70)
            if st.button(f"Pick {name}"):
                st.session_state.avatar = name
                st.rerun()
