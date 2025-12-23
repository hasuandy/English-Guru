import streamlit as st
import datetime
import time

# --- 1. SESSION STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'level' not in st.session_state: st.session_state.level = None
if 'streak' not in st.session_state: st.session_state.streak = 1

# --- 2. THEME & STYLING ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    /* Pure Black Background */
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #ffffff !important; }
    
    /* Modern Card UI */
    .card { 
        background-color: #111111; padding: 20px; border-radius: 12px; 
        border: 1px solid #333; margin-bottom: 15px; 
    }
    
    /* Buttons Styling */
    .stButton>button { 
        background: linear-gradient(45deg, #6c5ce7, #00ffcc) !important; 
        color: black !important; font-weight: bold !important;
        height: 50px; width: 100%; border: none !important; border-radius: 10px !important;
    }
    
    /* Metric Colors */
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-weight: bold; }
    
    /* Tabs Visibility */
    .stTabs [data-baseweb="tab"] { color: #888 !important; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PLACEMENT TEST (First Run) ---
if st.session_state.level is None:
    st.markdown("<h1 style='text-align:center;'>🎯 Start Your Journey</h1>", unsafe_allow_html=True)
    st.info("Pehle ek chota test dein taaki hum aapka level samajh sakein.")
    
    with st.form("test_form"):
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        q1 = st.radio("1. 'She ____ to the gym every day.'", ["go", "goes", "going"])
        q2 = st.radio("2. 'I have been working here ____ 2010.'", ["for", "since", "from"])
        q3 = st.radio("3. Meaning of 'Resilient':", ["Weak", "Able to recover quickly", "Angry"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.form_submit_button("Submit Test"):
            score = 0
            if q1 == "goes": score += 1
            if q2 == "since": score += 1
            if q3 == "Able to recover quickly": score += 1
            
            if score == 0: st.session_state.level = "Beginner"
            elif score <= 2: st.session_state.level = "Intermediate"
            else: st.session_state.level = "Advanced"
            st.rerun()
    st.stop()

# --- 4. MAIN APP INTERFACE ---
st.markdown(f"<h1 style='text-align:center;'>🚀 ENGLISH GURU: {st.session_state.level}</h1>", unsafe_allow_html=True)

# Top Bar Metrics
c1, c2, c3 = st.columns(3)
c1.metric("🏆 XP", st.session_state.xp)
c2.metric("🔥 Streak", f"{st.session_state.streak} Days")
c3.metric("🎖️ Level", st.session_state.level)

st.write("---")
tabs = st.tabs(["📚 MODULES", "📝 SRS PRACTICE", "📖 VAULT", "📊 STATS"])

# --- MODULES TAB ---
with tabs[0]:
    st.subheader(f"Current Path: {st.session_state.level}")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if st.session_state.level == "Beginner":
        st.write("### Lesson: Basic Sentence Structure")
        st.write("Focus on: Subject + Verb + Object")
    else:
        st.write("### Lesson: Advanced Contextual Usage")
        st.write("Focus on: Idioms and Phrasal Verbs")
    
    if st.button("Complete & Earn 50 XP"):
        st.session_state.xp += 50
        st.success("Module Finished!")
        time.sleep(1)
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PRACTICE (SRS LOGIC) TAB ---
with tabs[1]:
    st.subheader("Smart Review (SRS)")
    today = datetime.date.today()
    due_words = [w for w in st.session_state.vault if w['review_date'] <= today]
    
    if not due_words:
        st.info("Aaj ke liye revision complete hai! Naye words add karein.")
    else:
        word_to_test = due_words[0]
        st.markdown(f"<div class='card'>Define this word: <b>{word_to_test['word']}</b></div>", unsafe_allow_html=True)
        ans = st.text_input("Enter meaning:")
        if st.button("Verify Answer"):
            if ans.lower() in word_to_test['meaning'].lower():
                st.success("Sahi! Mastery increased.")
                st.session_state.xp += 20
                word_to_test['review_date'] = today + datetime.timedelta(days=3) # Next review in 3 days
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Wrong. Correct meaning was: {word_to_test['meaning']}")

# --- VAULT TAB ---
with tabs[2]:
    st.subheader("Add Word with Context")
    with st.form("vault_add"):
        new_w = st.text_input("Word")
        new_m = st.text_input("Meaning & Context")
        if st.form_submit_button("Add to Flashcards"):
            if new_w and new_m:
                st.session_state.vault.append({
                    "word": new_w, 
                    "meaning": new_m, 
                    "review_date": datetime.date.today() + datetime.timedelta(days=1)
                })
                st.success("Saved for review tomorrow!")
                st.rerun()
    
    st.write("---")
    for item in reversed(st.session_state.vault):
        st.markdown(f"<div class='card'><b>{item['word']}</b>: {item['meaning']} <br><small>Review on: {item['review_date']}</small></div>", unsafe_allow_html=True)

# --- STATS TAB ---
with tabs[3]:
    st.subheader("Progress Analytics")
    st.markdown(f"<div class='card'>Words Learned: {len(st.session_state.vault)}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>Current XP: {st.session_state.xp}</div>", unsafe_allow_html=True)
    st.bar_chart({"Activity": [10, 20, 5, 40, st.session_state.xp % 100]})

# Sidebar Reset
if st.sidebar.button("Reset Everything"):
    st.session_state.clear()
    st.rerun()
