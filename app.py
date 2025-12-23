import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'battle_log' not in st.session_state: st.session_state.battle_log = []

# --- 2. THEME & NEON UI ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Rajdhani', sans-serif; }
    .brand-title {
        font-family: 'Bungee'; font-size: 4rem; text-align: center;
        background: linear-gradient(90deg, #ff0055, #ffd700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: -50px;
    }
    .cyber-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid #00f2ff;
        border-radius: 15px; padding: 20px; box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        margin-bottom: 20px; text-align: center;
    }
    .battle-msg { color: #ff0055; font-weight: bold; font-family: 'Bungee'; }
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #8800ff) !important;
        color: white !important; font-family: 'Bungee' !important;
        border-radius: 12px !important; border: none !important; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='color:#ff0055; font-family:Bungee;'>🛡️ ARENA</h1>", unsafe_allow_html=True)
    page = st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Daily Boss", "📚 Word Vault", "🏆 Leaderboard"])
    st.write("---")
    if st.button("RESET PROGRESS"):
        st.session_state.clear()
        st.rerun()

st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# --- 4. PAGE LOGIC ---

if page == "🏰 Home Base":
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='cyber-card'><h3>🏆 XP</h3><h1>{st.session_state.xp}</h1></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='cyber-card'><h3>❤️ HP</h3><h1>{st.session_state.hp}%</h1></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='cyber-card'><h3>🔥 STREAK</h3><h1>{st.session_state.xp // 100}</h1></div>", unsafe_allow_html=True)
    
    st.write("### 📈 Evolutionary Progress")
    # Area chart with Instructed visual
    st.area_chart({"Power Level": [10, 40, 25, 60, st.session_state.xp]})

elif page == "👹 Daily Boss":
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp}")
        st.progress(st.session_state.boss_hp / 500)
    with col2:
        st.write(f"### 🛡️ YOUR HP: {st.session_state.hp}")
        st.progress(st.session_state.hp / 100)
    st.markdown("</div>", unsafe_allow_html=True)

    # Attack Module
    st.write("---")
    q = "Select the correct sentence:"
    choice = st.radio(q, ["He don't like coffee.", "He doesn't like coffee.", "He doesn't likes coffee."])
    
    col_a, col_h = st.columns([3, 1])
    with col_h:
        if st.checkbox("💡 Get Hint"):
            st.info("Remember: 'Does' already has the 's', so the main verb stays simple!")

    if col_a.button("💥 LAUNCH STRIKE"):
        if choice == "He doesn't like coffee.":
            dmg = random.randint(100, 200)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.xp += 50
            st.session_state.battle_log.append(f"✅ Hit Boss for {dmg} DMG!")
            st.success("CRITICAL HIT!")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.session_state.hp = max(0, st.session_state.hp - 20)
            st.session_state.battle_log.append("❌ Boss Counter-attacked! -20 HP")
            st.error("MISSED!")
        time.sleep(1)
        st.rerun()
    
    if st.session_state.battle_log:
        st.write("#### 📝 Battle Log")
        for log in st.session_state.battle_log[-3:]:
            st.write(log)

elif page == "📚 Word Vault":
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    w = st.text_input("New Intel (Word)")
    m = st.text_input("Meaning")
    if st.button("🔒 SEAL IN VAULT"):
        if w and m:
            st.session_state.vault.append({"word": w, "mean": m})
            st.success("Knowledge Stored!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    for item in st.session_state.vault:
        with st.expander(f"📖 {item['word']}"):
            st.write(item['mean'])

elif page == "🏆 Leaderboard":
    st.markdown("<div class='cyber-card'><h3>🏆 GLOBAL RANKINGS</h3>", unsafe_allow_html=True)
    st.write("1. 💎 Legendary Warrior - 5000 XP")
    st.write(f"2. 🛡️ **You** - {st.session_state.xp} XP")
    st.write("3. ⚔️ Cyber Ninja - 150 XP")
    st.markdown("</div>", unsafe_allow_html=True)
