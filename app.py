import streamlit as st
import time

# --- 1. SESSION STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'level' not in st.session_state: st.session_state.level = None  # Placement Test check

# --- 2. HIGH CONTRAST DARK THEME ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    /* Dark Background & White Text */
    .stApp { background-color: #050505; color: #ffffff; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #ffffff !important; }
    
    /* Highlight Cards */
    .main-card { 
        background-color: #111111; 
        padding: 20px; 
        border-radius: 15px; 
        border: 2px solid #6c5ce7; 
        margin-bottom: 20px;
    }
    
    /* Custom Metric Visibility */
    [data-testid="stMetricValue"] { color: #00d1b2 !important; font-size: 30px !important; }
    
    /* Action Buttons */
    .stButton>button { 
        background: linear-gradient(45deg, #6c5ce7, #a29bfe) !important; 
        color: white !important; 
        font-weight: bold !important;
        height: 50px; width: 100%; border: none !important;
    }

    /* Input Fields */
    input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #444 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PLACEMENT TEST LOGIC ---
if st.session_state.level is None:
    st.markdown("<h1 style='text-align: center; color: #6c5ce7;'>🎯 English Placement Test</h1>", unsafe_allow_html=True)
    st.write("Welcome! Chaliye pehle aapka level check karte hain.")
    
    with st.form("placement_test"):
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        q1 = st.radio("1. 'They ___ already left the party.'", ["has", "have", "is"])
        q2 = st.radio("2. 'If I ____ rich, I would buy a car.'", ["am", "was", "were"])
        q3 = st.radio("3. Meaning of 'Elated':", ["Sad", "Very Happy", "Angry"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.form_submit_button("Result Dekhein 🚀"):
            score = 0
            if q1 == "have": score += 1
            if q2 == "were": score += 1
            if q3 == "Very Happy": score += 1
            
            if score == 0: st.session_state.level = "Beginner"
            elif score <= 2: st.session_state.level = "Intermediate"
            else: st.session_state.level = "Advanced"
            st.rerun()
    st.stop()

# --- 4. MAIN NAVIGATION AFTER TEST ---
st.markdown(f"<h1 style='text-align: center;'>🚀 ENGLISH GURU: {st.session_state.level.upper()}</h1>", unsafe_allow_html=True)

# Top Dashboard
c1, c2, c3 = st.columns(3)
c1.metric("🏆 TOTAL XP", st.session_state.xp)
c2.metric("🔥 STREAK", f"{st.session_state.streak} Days")
c3.metric("🎖️ LEVEL", st.session_state.level)

st.markdown("---")
tabs = st.tabs(["📚 LESSONS", "⚔️ PRACTICE", "📖 VAULT", "📊 PROGRESS"])

# --- TAB 1: CURRICULUM ---
with tabs[0]:
    st.markdown("### Structured Modules")
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if st.session_state.level == "Beginner":
        st.subheader("Lesson 1: Introduction & Greetings")
        st.write("Learn: Hello, Thank You, Excuse Me.")
    elif st.session_state.level == "Intermediate":
        st.subheader("Lesson 1: Conditional Sentences")
        st.write("Learn: 'If' clauses and hypothetical situations.")
    else:
        st.subheader("Lesson 1: Professional Writing")
        st.write("Learn: Business Etiquette and Formal Emails.")
    
    if st.button("Complete Lesson ✅"):
        st.session_state.xp += 30
        st.toast("Lesson Mastered! +30 XP")
        time.sleep(1)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: PRACTICE (Speaking/Listening) ---
with tabs[1]:
    st.markdown("### Skills Training")
    act = st.selectbox("Action:", ["Speaking Practice (Simulation)", "Listening Comprehension"])
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if "Speaking" in act:
        st.write(f"Repeat this: **'I am determined to master the English language.'**")
        st.button("🎙️ Start Recording (Bypass AI)")
    else:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
        st.write("Listen carefully and write down the context below.")
        st.text_area("Your Notes:")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 3: VOCABULARY VAULT (SRS Logic) ---
with tabs[2]:
    st.markdown("### Vocabulary Builder")
    col_w, col_m = st.columns(2)
    new_word = col_w.text_input("New Word")
    new_mean = col_m.text_input("Meaning")
    
    if st.button("Save to Vault 🔒"):
        if new_word and new_mean:
            st.session_state.vault.append({"w": new_word, "m": new_mean})
            st.success("Word Saved!")
            st.rerun()
    
    st.markdown("---")
    st.subheader("Flashcards")
    for item in reversed(st.session_state.vault):
        st.markdown(f"<div class='main-card'><b>{item['w']}</b> : {item['m']}</div>", unsafe_allow_html=True)

# --- TAB 4: PROGRESS ---
with tabs[3]:
    st.markdown("### Learning Analytics")
    st.write(f"Words Collected: **{len(st.session_state.vault)}**")
    st.write(f"Lessons Finished: **{st.session_state.xp // 30}**")
    st.bar_chart({"XP Growth": [0, 10, 20, 30, st.session_state.xp]})

# Sidebar Reset
if st.sidebar.button("Reset All Data"):
    st.session_state.clear()
    st.rerun()
