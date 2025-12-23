import streamlit as st
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'level' not in st.session_state: st.session_state.level = "Beginner"

# --- 2. THEME & STYLING (For Best Visibility) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    /* Main Background: Dark Navy Blue */
    .stApp { 
        background-color: #0e1117; 
        color: #ffffff; 
    }
    
    /* Headers and Text Visibility */
    h1, h2, h3, p, span, label {
        color: #ffffff !important;
    }

    /* Cards for Content: Darker Grey/Blue */
    .main-card { 
        background-color: #1c2128; 
        padding: 20px; 
        border-radius: 15px; 
        border: 2px solid #30363d; 
        margin-bottom: 20px;
        color: white;
    }

    /* Input Boxes Visibility */
    input, textarea {
        background-color: #2d333b !important;
        color: white !important;
        border: 1px solid #6c5ce7 !important;
    }

    /* Buttons: Bright Purple */
    .stButton>button { 
        background-color: #6c5ce7 !important; 
        color: white !important; 
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100%;
        height: 50px;
    }
    
    /* Tabs visibility */
    .stTabs [data-baseweb="tab"] {
        color: #8b949e !important;
    }
    .stTabs [aria-selected="true"] {
        color: #6c5ce7 !important;
        border-bottom-color: #6c5ce7 !important;
    }
    
    /* Metric boxes */
    [data-testid="stMetricValue"] {
        color: #00d1b2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TOP NAVIGATION ---
st.markdown("<h1 style='text-align: center;'>🚀 ENGLISH GURU PRO</h1>", unsafe_allow_html=True)

# Dashboard Stats Row
c1, c2, c3 = st.columns(3)
with c1: st.metric("🏆 Total XP", st.session_state.xp)
with c2: st.metric("🔥 Streak", f"{st.session_state.streak} Days")
with c3: st.metric("🎖️ Rank", st.session_state.level)

st.markdown("---")

# --- 4. MAIN MODULES (Tabs) ---
tabs = st.tabs(["📚 LESSONS", "⚔️ PRACTICE", "📖 VAULT", "📊 PROGRESS"])

with tabs[0]:
    st.markdown("### 📝 Grammar & Reading")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("Tenses: Present Simple")
        st.write("Rule: Subject + V1(s/es) + Object")
        st.info("Example: 'She speaks English fluently.'")
        if st.button("Complete Lesson"):
            st.session_state.xp += 20
            st.toast("Lesson Finished! +20 XP")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        st.subheader("Reading: Daily News")
        st.write("*Technology is changing the world fast...*")
        st.write("**New Word:** Technology (Takneek)")
        if st.button("Read More"):
            st.session_state.xp += 10
        st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    st.markdown("### ⚔️ Interactive Challenges")
    act = st.selectbox("Choose Activity", ["Daily Quiz", "Speaking (Bypass AI)", "Listening"])
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if act == "Daily Quiz":
        q = st.radio("Correct: 'Neither of the boys ____ here.'", ["is", "are"])
        if st.button("Submit Answer"):
            if q == "is":
                st.session_state.xp += 50
                st.success("Correct! Singular subject logic.")
            else:
                st.error("Wrong! 'Neither' takes a singular verb.")
    
    elif act == "Speaking (Bypass AI)":
        st.write("Try Pronouncing: **'The weather is beautiful.'**")
        st.button("🎙️ Record Voice")
        st.caption("AI Feedback is bypassed for now.")

    elif act == "Listening":
        st.write("Listen and type what you hear:")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
        st.text_input("Your Answer...")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("### 📖 My Vocabulary Vault")
    c_a, c_b = st.columns(2)
    with c_a:
        w = st.text_input("English Word")
    with c_b:
        m = st.text_input("Meaning")
    
    if st.button("Save to Flashcards"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            st.success("Saved!")
            st.rerun()

    st.markdown("---")
    if st.session_state.vault:
        for item in reversed(st.session_state.vault):
            st.markdown(f"<div class='main-card'><b>{item['w']}</b> : {item['m']}</div>", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### 📊 Performance Dashboard")
    st.write(f"Words Mastered: **{len(st.session_state.vault)}**")
    st.write(f"Learning Streak: **{st.session_state.streak}**")
    st.bar_chart({"Progress": [10, 20, 30, 40, st.session_state.xp]})

# Sidebar Reset
if st.sidebar.button("Reset App Data"):
    st.session_state.clear()
    st.rerun()
