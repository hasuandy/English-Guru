import streamlit as st

# --- 1. SETUP ---
st.set_page_config(page_title="English Guru", layout="centered")

# Memory store karne ke liye
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []

# --- 2. STYLE (Clean White & Purple) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #f1f2f6; border-radius: 10px;
        padding: 10px 20px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #6c5ce7 !important; color: white !important; }
    .stat-box {
        text-align: center; padding: 15px; background: #6c5ce7;
        color: white; border-radius: 15px; font-size: 22px; font-weight: bold;
        margin-bottom: 20px; box-shadow: 0 4px 10px rgba(108, 92, 231, 0.2);
    }
    .word-card {
        padding: 15px; border-bottom: 2px solid #f1f2f6; font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TOP STATS ---
st.markdown(f"<div class='stat-box'>🏆 Total XP: {st.session_state.xp}</div>", unsafe_allow_html=True)

# --- 4. NAVIGATION TABS (No Scroll Needed) ---
tab1, tab2, tab3 = st.tabs(["🎮 PLAY GAME", "➕ ADD WORD", "📚 MY VAULT"])

# --- PAGE 1: GAME ---
with tab1:
    st.write("### Sahi Option Chuniye")
    q = "Question: 'They ____ playing cricket.'"
    ans = st.radio(q, ["is", "am", "are"], horizontal=True)
    
    if st.button("CHECK ANSWER ✅"):
        if ans == "are":
            st.session_state.xp += 10
            st.success("Sahi Jawab! +10 XP mil gaye.")
        else:
            st.error("Galat! Dobara koshish karein.")

# --- PAGE 2: ADD WORD ---
with tab2:
    st.write("### Naya Word Yaad Karein")
    w = st.text_input("English Word (Example: Happy)")
    m = st.text_input("Meaning (Example: Khush)")
    
    if st.button("SAVE WORD 🔒"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            st.balloons()
            st.success(f"'{w}' aapke Vault mein save ho gaya!")
        else:
            st.warning("Dono box bhariye!")

# --- PAGE 3: VAULT ---
with tab3:
    st.write("### Aapke Saare Words")
    if not st.session_state.vault:
        st.info("Abhi koi word nahi hai. 'ADD WORD' par jaakar naya word likhein.")
    else:
        # Latest word sabse upar dikhega
        for item in reversed(st.session_state.vault):
            st.markdown(f"<div class='word-card'><b>{item['w']}</b> : {item['m']}</div>", unsafe_allow_html=True)

# --- RESET OPTION ---
st.write("---")
if st.sidebar.button("Reset Game Data"):
    st.session_state.clear()
    st.rerun()
