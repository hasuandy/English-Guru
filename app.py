import streamlit as st
import random
import time

# --- 1. RESET & INITIALIZE SESSION ---
# Yeh section app ko crash hone se bachayega
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'user_page' not in st.session_state: st.session_state.user_page = "🏰 Home Base"

# --- 2. THEME & UI ---
st.set_page_config(page_title="English Guru", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background: #0a0a0a; color: #00f2ff; font-family: 'Rajdhani', sans-serif; }
    .brand-title { font-family: 'Bungee'; font-size: 3.5rem; text-align: center; color: #ff0055; text-shadow: 0 0 10px #ff0055; }
    .card { background: #1a1a1a; border: 1px solid #333; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 15px; }
    .stButton>button { background: #ff0055 !important; color: white !important; font-family: 'Bungee' !important; width: 100%; border-radius: 10px; border:none; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#ff0055; font-family:Bungee;'>MENU</h2>", unsafe_allow_html=True)
    page = st.radio("CHOOSE MISSION", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault"])
    st.write("---")
    if st.button("RESET ALL PROGRESS"):
        st.session_state.xp = 0
        st.session_state.hp = 100
        st.session_state.boss_hp = 500
        st.session_state.vault = []
        st.rerun()

st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# --- 4. PAGES ---

if page == "🏰 Home Base":
    c1, c2 = st.columns(2)
    with c1: st.markdown(f"<div class='card'><h3>🏆 YOUR XP</h3><h1>{st.session_state.xp}</h1></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='card'><h3>❤️ STAMINA</h3><h1>{st.session_state.hp}%</h1></div>", unsafe_allow_html=True)
    
    st.write("### 📈 Recent Progress")
    # Simple Area Chart
    st.area_chart({"Level": [10, 20, 15, 40, st.session_state.xp]})

elif page == "👹 Daily Boss":
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp}")
        st.progress(st.session_state.boss_hp / 500)
    with col2:
        st.write(f"### 🛡️ YOUR HP: {st.session_state.hp}")
        st.progress(st.session_state.hp / 100)

    st.write("---")
    st.markdown("### ⚔️ ATTACK STAGE")
    q = "Select the correct word: 'Neither of the answers ____ correct.'"
    ans = st.selectbox(q, ["Choose...", "is", "are"])

    if st.button("💥 FIRE ATTACK"):
        if ans == "is":
            dmg = random.randint(70, 150)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.xp += 50
            st.success(f"CRITICAL HIT! You dealt {dmg} damage!")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        elif ans == "Choose...":
            st.warning("Please select an answer first!")
        else:
            st.session_state.hp = max(0, st.session_state.hp - 25)
            st.error("MISS! The boss hit you for 25 damage!")
        time.sleep(1)
        st.rerun()

elif page == "📚 Word Vault":
    st.write("### 🔒 Save New Vocabulary")
    w = st.text_input("Word")
    m = st.text_input("Meaning")
    if st.button("ADD TO VAULT"):
        if w and m:
            st.session_state.vault.append({"word": w, "mean": m})
            st.success(f"'{w}' saved!")
    
    st.write("---")
    st.write("### 📖 My Collection")
    for item in st.session_state.vault:
        st.info(f"**{item['word']}**: {item['mean']}")
