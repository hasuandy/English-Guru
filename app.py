import streamlit as st
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# --- 2. QUESTIONS DATA ---
questions = [
    {"q": "Choose correct: 'She ____ a song.'", "a": ["sing", "sings", "singing"], "c": "sings"},
    {"q": "Past tense of 'Eat' is:", "a": ["Eaten", "Ate", "Eats"], "c": "Ate"},
    {"q": "I ____ learning English.", "a": ["am", "is", "are"], "c": "am"},
    {"q": "Opposite of 'Easy' is:", "a": ["Simple", "Hard", "Fast"], "c": "Hard"},
    {"q": "Correct spelling:", "a": ["Tommorow", "Tomorrow", "Tomorow"], "c": "Tomorrow"}
]

# --- 3. CLEAN MODERN STYLE ---
st.set_page_config(page_title="English Guru", layout="centered")

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #f8f9fc; }
    
    /* Stats Header */
    .header-box {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;
        border-top: 5px solid #6c5ce7; margin-bottom: 20px;
    }
    
    /* Big Navigation Buttons */
    .stButton>button {
        height: 55px; width: 100%; border-radius: 12px !important;
        font-size: 18px !important; font-weight: bold !important;
        background: #6c5ce7 !important; color: white !important;
        border: none !important; transition: 0.3s;
    }
    .stButton>button:hover { background: #5849c4 !important; transform: translateY(-2px); }

    /* Word Card */
    .word-card {
        background: white; padding: 15px; border-radius: 10px;
        border-left: 5px solid #00b894; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. TOP STATS BAR ---
st.markdown("<h1 style='text-align:center; color:#1e1e2f;'>🛡️ English Guru</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='header-box'><small>MY XP</small><br><h2 style='color:#6c5ce7; margin:0;'>{st.session_state.xp}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='header-box'><small>BOSS HEALTH</small><br><h2 style='color:#ff4757; margin:0;'>{st.session_state.boss_hp}</h2></div>", unsafe_allow_html=True)

# --- 5. SIMPLE MENU ---
st.write("### 🕹️ Select Action:")
menu = st.selectbox("", ["🎮 Play Battle", "📖 View My Vault", "➕ Add New Word", "🏅 Badges"], label_visibility="collapsed")

st.write("---")

# --- 6. PAGE LOGIC ---

if menu == "🎮 Play Battle":
    st.subheader("Grammar Challenge")
    q_data = questions[st.session_state.q_idx % len(questions)]
    st.info(f"**Question:** {q_data['q']}")
    ans = st.radio("Choose your answer:", q_data['a'], key=f"bat_{st.session_state.q_idx}")
    
    if st.button("FIRE ATTACK 💥"):
        if ans == q_data['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.success("✅ SAHI JAWAB! Boss ko 100 DMG laga.")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500 # Respawn Boss
        else:
            st.error(f"❌ GALAT! Sahi jawab tha: {q_data['c']}")
        
        st.session_state.q_idx += 1
        time.sleep(1)
        st.rerun()

elif menu == "📖 View My Vault":
    st.subheader("Saved Words")
    if not st.session_state.vault:
        st.warning("Vault abhi khali hai. Kuch words add karein!")
    else:
        for item in reversed(st.session_state.vault):
            st.markdown(f"""
                <div class='word-card'>
                    <b style='color:#00b894; font-size:1.1rem;'>{item['word']}</b><br>
                    <span style='color:#636e72;'>Meaning: {item['meaning']}</span>
                </div>
            """, unsafe_allow_html=True)

elif menu == "➕ Add New Word":
    st.subheader("Add Knowledge")
    w = st.text_input("English Word:")
    m = st.text_input("Hindi Meaning:")
    if st.button("SAVE TO VAULT 🔒"):
        if w and m:
            st.session_state.vault.append({"word": w, "meaning": m})
            st.success(f"'{w}' save ho gaya!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.warning("Please fill both boxes!")

elif menu == "🏅 Badges":
    st.subheader("Your Achievements")
    c_a, c_b = st.columns(2)
    if len(st.session_state.vault) >= 1:
        c_a.success("📖 Scholar Unlocked")
    else:
        c_a.info("Locked: Save 1 Word")
        
    if st.session_state.xp >= 200:
        c_b.success("⚔️ Warrior Unlocked")
    else:
        c_b.info("Locked: Earn 200 XP")

# Reset Button (Sidebar)
if st.sidebar.button("Reset All Data"):
    st.session_state.clear()
    st.rerun()
