import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# --- 2. QUESTIONS DATA ---
questions = [
    {"q": "I ____ eating an apple.", "a": ["am", "is", "are"], "c": "am"},
    {"q": "They ____ going to school.", "a": ["is", "am", "are"], "c": "are"},
    {"q": "She ____ a beautiful song.", "a": ["sing", "sings", "singing"], "c": "sings"},
    {"q": "Past tense of 'Run' is:", "a": ["Runned", "Ran", "Running"], "c": "Ran"}
]

# --- 3. PREMIUM UI STYLING (No Scroll Design) ---
st.set_page_config(page_title="English Guru", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Full Page Height Fix */
    .main { background-color: #f8f9fa; }
    .stApp { height: 100vh; overflow: hidden; } /* Prevents scrolling */
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #1e1e2f; border-right: 2px solid #6c5ce7; }
    [data-testid="stSidebar"] * { color: white !important; }

    /* Title Styling */
    .hero-title {
        font-family: 'Poppins', sans-serif; font-size: 2.5rem; font-weight: 800;
        color: #6c5ce7; text-align: center; margin-top: -50px;
    }

    /* Cards */
    .info-card {
        background: white; border-radius: 15px; padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 5px solid #6c5ce7;
        text-align: center; margin-bottom: 10px;
    }

    /* Custom Buttons */
    .stButton>button {
        background: #6c5ce7 !important; color: white !important;
        border-radius: 10px !important; width: 100%; border: none; height: 45px;
        font-weight: bold; transition: 0.3s;
    }
    .stButton>button:hover { background: #a29bfe !important; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>🎴 MENU</h1>", unsafe_allow_html=True)
    page = st.radio("CHOOSE ACTION:", ["🏠 HOME", "⚔️ BATTLE", "📚 VAULT", "🏅 BADGES"])
    st.write("---")
    st.markdown(f"**XP:** {st.session_state.xp}")
    st.markdown(f"**BOSS:** {st.session_state.boss_hp} HP")
    if st.button("RESET GAME"):
        st.session_state.clear()
        st.rerun()

# --- 5. PAGE LOGIC ---

if page == "🏠 HOME":
    st.markdown("<h1 class='hero-title'>Welcome, Warrior</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='info-card'><h3>🏆 XP POINTS</h3><h2>{st.session_state.xp}</h2></div>", unsafe_allow_html=True)
    with c2:
        rank = "ROOKIE" if st.session_state.xp < 200 else "EXPERT"
        st.markdown(f"<div class='info-card'><h3>🎖️ CURRENT RANK</h3><h2>{rank}</h2></div>", unsafe_allow_html=True)
    st.info("💡 Tip: Go to 'BATTLE' to earn XP and defeat the Boss!")

elif page == "⚔️ BATTLE":
    st.markdown("<h2 style='color:#6c5ce7;'>👹 BOSS BATTLE</h2>", unsafe_allow_html=True)
    st.progress(st.session_state.boss_hp / 500)
    
    st.markdown("<div class='info-card'>", unsafe_allow_html=True)
    q = questions[st.session_state.q_idx % len(questions)]
    st.write(f"### {q['q']}")
    ans = st.radio("Choose correct answer:", q['a'], key=f"q_{st.session_state.q_idx}")
    
    if st.button("STRIKE!"):
        if ans == q['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.success("BAM! -100 HP")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error("MISS! Correct answer was: " + q['c'])
        
        st.session_state.q_idx += 1
        time.sleep(1)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📚 VAULT":
    st.markdown("<h2 style='color:#6c5ce7;'>📖 WORD VAULT</h2>", unsafe_allow_html=True)
    with st.expander("➕ Add New Word", expanded=True):
        w = st.text_input("Word")
        m = st.text_input("Meaning")
        if st.button("Save Knowledge"):
            if w and m:
                st.session_state.vault.append({"w": w, "m": m})
                st.rerun()
    
    if st.session_state.vault:
        for item in st.session_state.vault[-3:]: # Sirf last 3 taaki scroll na ho
            st.write(f"✅ **{item['w']}**: {item['m']}")

elif page == "🏅 BADGES":
    st.markdown("<h2 style='color:#6c5ce7;'>🏅 YOUR ACHIEVEMENTS</h2>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    if len(st.session_state.vault) >= 1:
        col_a.markdown("<div class='info-card'>📖<br>Scholar</div>", unsafe_allow_html=True)
    if st.session_state.xp >= 200:
        col_b.markdown("<div class='info-card'>⚔️<br>Warrior</div>", unsafe_allow_html=True)
    if not st.session_state.vault and st.session_state.xp < 200:
        st.write("No badges earned yet. Go fight!")
