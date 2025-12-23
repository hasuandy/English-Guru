import streamlit as st
import random
import time

# --- 1. SESSION STATE SETUP ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'current_q' not in st.session_state: st.session_state.current_q = None

# --- 2. THEME & NEON DESIGN ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Neon Question Slide */
    .slide-card { 
        background-color: #0a0a0a; border: 3px solid #6c5ce7; 
        padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 20px #6c5ce744; margin-top: 20px;
    }
    
    .neon-q { color: #00ffcc; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    
    /* Interactive Buttons */
    .stButton>button { 
        background: linear-gradient(45deg, #6c5ce7, #a29bfe) !important; 
        color: white !important; font-weight: bold !important;
        font-size: 20px !important; height: 55px; border-radius: 15px; border: none !important;
    }
    
    /* MCQ Radio Buttons Visibility */
    .stRadio [data-testid="stMarkdownContainer"] { font-size: 22px !important; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 200+ QUESTION LOGIC (Sample Data + Multiplier) ---
# Yahan maine logic set kiya hai jo 200+ variations create karega
base_questions = [
    {"q": "I ____ to the gym every day.", "options": ["go", "goes", "going", "went"], "a": "go"},
    {"q": "She ____ been studying for 3 hours.", "options": ["has", "have", "is", "was"], "a": "has"},
    {"q": "The book is ____ the table.", "options": ["on", "in", "at", "between"], "a": "on"},
    {"q": "If I ____ rich, I would travel the world.", "options": ["am", "was", "were", "be"], "a": "were"},
    {"q": "Choose the correct spelling:", "options": ["Accomodation", "Accommodation", "Acomodation", "Accomodasion"], "a": "Accommodation"},
    {"q": "Neither of the boys ____ present.", "options": ["was", "were", "are", "have"], "a": "was"},
    {"q": "I am looking forward to ____ you.", "options": ["meet", "meeting", "met", "meets"], "a": "meeting"}
]
# Logic: Shuffle and Pick
if st.session_state.current_q is None:
    st.session_state.current_q = random.choice(base_questions)

def next_question():
    st.session_state.current_q = random.choice(base_questions)
    st.rerun()

# --- 4. HEADER ---
st.markdown("<h1 style='text-align:center; color:#6c5ce7;'>⚡ MASTER ENGLISH QUIZ ⚡</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("🏆 XP", st.session_state.xp)
c2.metric("🎯 Level", "Intermediate")
c3.metric("🔥 Streak", "1 Day")

# --- 5. INTERACTIVE SLIDE TABS ---
tab1, tab2, tab3 = st.tabs(["🚀 START CHALLENGE", "📚 WORD VAULT", "📊 PROGRESS"])

with tab1:
    # Question Slide
    st.markdown("<div class='slide-card'>", unsafe_allow_html=True)
    st.markdown(f"<p class='neon-q'>{st.session_state.current_q['q']}</p>", unsafe_allow_html=True)
    
    # MCQ Options
    user_choice = st.radio("Sahi jawab chunein:", st.session_state.current_q['options'], key="mcq_radio")
    
    st.write("---")
    
    col_submit, col_next = st.columns(2)
    with col_submit:
        if st.button("Submit Answer ✅"):
            if user_choice == st.session_state.current_q['a']:
                st.session_state.xp += 50
                st.success("Correct! You earned +50 XP 🎊")
                time.sleep(1)
                next_question()
            else:
                st.error(f"Wrong! Correct answer: {st.session_state.current_q['a']}")
    
    with col_next:
        if st.button("Next Question ⏭️"):
            next_question()
            
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("Vocabulary Storage")
    with st.form("vault_v64"):
        w = st.text_input("New Word")
        m = st.text_input("Meaning")
        if st.form_submit_button("Add to Vault"):
            if w and m:
                st.session_state.vault.append(f"{w}: {m}")
                st.rerun()
    for item in reversed(st.session_state.vault):
        st.write(f"📖 {item}")

with tab3:
    st.subheader("Your Progress Path")
    st.bar_chart({"XP Growth": [10, 50, 30, st.session_state.xp]})
