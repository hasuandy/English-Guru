import streamlit as st
import time

# --- 1. SESSION STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'level' not in st.session_state: st.session_state.level = None 

# --- 2. HIGH-CONTRAST DARK THEME ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    /* Dark Background */
    .stApp { background-color: #050505; color: #ffffff; }
    
    /* Global Text Color */
    h1, h2, h3, p, span, label, .stMarkdown { color: #ffffff !important; }
    
    /* Highlighted Cards */
    .main-card { 
        background-color: #121212; 
        padding: 20px; 
        border-radius: 15px; 
        border: 2px solid #6c5ce7; 
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.2);
    }
    
    /* Metrics Visibility */
    [data-testid="stMetricValue"] { color: #00d1b2 !important; font-size: 35px !important; font-weight: bold; }
    
    /* Buttons Styling */
    .stButton>button { 
        background: linear-gradient(45deg, #6c5ce7, #a29bfe) !important; 
        color: white !important; 
        font-weight: bold !important;
        height: 50px; width: 100%; border: none !important;
        border-radius: 12px !important;
    }

    /* Input Fields */
    input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #444 !important; }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-size: 16px !important; }
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #6c5ce7 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PLACEMENT TEST ---
if st.session_state.level is None:
    st.markdown("<h1 style='text-align: center; color: #6c5ce7;'>🎯 Placement Test</h1>", unsafe_allow_html=True)
    st.write("Aapka sahi learning path chunne ke liye ye test zaruri hai:")
    
    with st.form("placement_test"):
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        q1 = st.radio("1. 'Neither of the students ___ finished the work.'", ["has", "have"])
        q2 = st.radio("2. 'If it rains, we ___ at home.'", ["will stay", "would stay", "stayed"])
        q3 = st.radio("3. 'Antonym of 'Gigantic' is:'", ["Huge", "Tiny", "Strong"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.form_submit_button("Test Submit Karein"):
            score = 0
            if q1 == "has": score += 1
            if q2 == "will stay": score += 1
            if q3 == "Tiny": score += 1
            
            if score == 0: st.session_state.level = "Beginner"
            elif score <= 2: st.session_state.level = "Intermediate"
            else: st.session_state.level = "Advanced"
            st.rerun()
    st.stop()

# --- 4. MAIN INTERFACE ---
st.markdown(f"<h1 style='text-align: center;'>🚀 ENGLISH GURU: {st.session_state.level.upper()}</h1>", unsafe_allow_html=True)

# Dashboard Summary
c1, c2, c3 = st.columns(3)
c1.metric("🏆 XP", st.session_state.xp)
c2.metric("🔥 STREAK", f"{st.session_state.streak} Days")
c3.metric("🎖️ RANK", st.session_state.level)

st.markdown("---")
tabs = st.tabs(["📚 LESSONS", "⚔️ PRACTICE", "📖 VAULT", "📈 STATS"])

# --- TAB: LESSONS ---
with tabs[0]:
    st.markdown("### 🎓 Personalised Path")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if st.session_state.level == "Beginner":
        st.subheader("Module 1: Building Sentences")
        st.write("Concepts: Is/Am/Are, Nouns, and Pronouns.")
    elif st.session_state.level == "Intermediate":
        st.subheader("Module 1: Perfect Tenses")
        st.write("Concepts: Has/Have + V3, Been, and Duration.")
    else:
        st.subheader("Module 1: Complex Clauses")
        st.write("Concepts: Relative clauses and Phrasal Verbs.")
    
    if st.button("Complete & Earn 50 XP"):
        st.session_state.xp += 50
        st.success("Module Completed!")
        time.sleep(1)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB: PRACTICE ---
with tabs[1]:
    st.markdown("### 🎙️ Skills Arena")
    mode = st.selectbox("Practice Mode:", ["Speaking Immersion", "Listening Skills"])
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if "Speaking" in mode:
        st.write("Say this clearly: **'Consistency is the key to success.'**")
        st.button("🎙️ Record Voice (AI Bypassed)")
    else:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3")
        st.write("Listen to the conversation and take notes.")
        st.text_input("What was the main topic?")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB: VAULT ---
with tabs[2]:
    st.markdown("### 📖 My Contextual Dictionary")
    cw, cm = st.columns(2)
    new_w = cw.text_input("New English Word")
    new_m = cm.text_input("Meaning/Sentence")
    
    if st.button("Save to My Vault"):
        if new_w and new_m:
            st.session_state.vault.append({"w": new_w, "m": new_m})
            st.success("Secured in Vault!")
            st.rerun()
    
    st.markdown("---")
    if not st.session_state.vault:
        st.info("Aapka vault khali hai.")
    else:
        for item in reversed(st.session_state.vault):
            st.markdown(f"<div class='main-card'><b>{item['w']}</b> : {item['m']}</div>", unsafe_allow_html=True)

# --- TAB: STATS ---
with tabs[3]:
    st.markdown("### 📈 Your Growth Tracker")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.write(f"Total XP: **{st.session_state.xp}**")
    st.write(f"Words in Vault: **{len(st.session_state.vault)}**")
    st.progress(min(st.session_state.xp / 1000, 1.0))
    st.bar_chart({"XP Progress": [10, 50, 20, 100, st.session_state.xp]})
    st.markdown("</div>", unsafe_allow_html=True)

# SIDEBAR RESET
if st.sidebar.button("Hard Reset Progress"):
    st.session_state.clear()
    st.rerun()
