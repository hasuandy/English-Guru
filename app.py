import streamlit as st
import random
import time

# --- 1. INITIALIZE SESSION (Crash-Proof Logic) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []

# --- 2. PREMIUM GAMING UI ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    
    .stApp { background: #050505; color: #00f2ff; font-family: 'Rajdhani', sans-serif; }
    
    /* Neon Glow Title */
    .brand-title {
        font-family: 'Bungee'; font-size: 4rem; text-align: center;
        background: linear-gradient(90deg, #ff0055, #00f2ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 0, 85, 0.5);
        margin-top: -50px;
    }

    /* Cyber Card Style */
    .cyber-card {
        background: rgba(20, 20, 40, 0.6);
        border: 1px solid #00f2ff;
        border-radius: 15px; padding: 20px;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        margin-bottom: 20px; text-align: center;
    }

    /* Gaming Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #ff0055, #8800ff) !important;
        color: white !important; font-family: 'Bungee' !important;
        border-radius: 10px !important; border: none !important;
        height: 50px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #ff0055; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#ff0055; font-family:Bungee;'>WARRIOR HUB</h2>", unsafe_allow_html=True)
    page = st.radio("SELECT MISSION", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault"])
    st.write("---")
    if st.button("🔴 RESET PROGRESS"):
        st.session_state.xp = 0
        st.session_state.hp = 100
        st.session_state.boss_hp = 500
        st.session_state.vault = []
        st.rerun()

st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# --- 4. PAGE LOGIC ---

if page == "🏰 Home Base":
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='cyber-card'><h3>🏆 XP</h3><h1 style='color:#ffd700;'>{st.session_state.xp}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='cyber-card'><h3>❤️ STAMINA</h3><h1 style='color:#ff0055;'>{st.session_state.hp}%</h1></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='cyber-card'><h3>🎖️ RANK</h3><h1 style='color:#00f2ff;'>WARRIOR</h1></div>", unsafe_allow_html=True)
    
    st.write("### 📈 Evolutionary Growth")
    st.area_chart({"Power": [10, 25, 15, 45, st.session_state.xp]})

elif page == "👹 Daily Boss":
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### 👹 TITAN HP: {st.session_state.boss_hp}")
        st.progress(st.session_state.boss_hp / 500)
    with col2:
        st.write(f"### 🛡️ YOUR HP: {st.session_state.hp}")
        st.progress(st.session_state.hp / 100)
    st.markdown("</div>", unsafe_allow_html=True)

    # Battle Quiz
    st.write("---")
    st.markdown("### ⚔️ ATTACK PHASE")
    q = "Select the correct sentence for 50 damage:"
    choice = st.selectbox(q, ["Choose...", "She don't know.", "She doesn't know.", "She doesn't knows."])
    
    # Hint System
    if st.checkbox("💡 Get Hint"):
        st.info("Hint: Third-person singular (She) always uses 'does' + base form of the verb.")

    if st.button("💥 LAUNCH ATTACK"):
        if choice == "She doesn't know.":
            dmg = random.randint(80, 150)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.xp += 50
            st.success(f"🔥 CRITICAL HIT! You dealt {dmg} damage!")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500 # Respawn boss
        elif choice == "Choose...":
            st.warning("Weapon not selected! Choose an answer.")
        else:
            st.session_state.hp = max(0, st.session_state.hp - 20)
            st.error("💀 MISSED! The Boss hit you for 20 damage!")
        time.sleep(1)
        st.rerun()

elif page == "📚 Word Vault":
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    w = st.text_input("New Intel (Word)")
    m = st.text_input("Data (Meaning)")
    if st.button("🔒 SEAL IN VAULT"):
        if w and m:
            st.session_state.vault.append({"word": w, "mean": m})
            st.success(f"Knowledge '{w}' Secured!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("### 📖 Stored Memory")
    for item in st.session_state.vault:
        with st.expander(f"🔹 {item['word']}"):
            st.write(item['mean'])
