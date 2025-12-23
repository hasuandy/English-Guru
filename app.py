import streamlit as st
import random
import time

# --- 1. SESSION STATE INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_index' not in st.session_state: st.session_state.q_index = 0

# --- 2. THE 200+ QUESTION ENGINE ---
# Aap is list mein 200 questions tak add kar sakte hain, format same rakhein
questions_bank = [
    {"q": "I ____ to the gym every day.", "options": ["go", "goes", "going", "went"], "a": "go"},
    {"q": "She ____ been studying for 3 hours.", "options": ["has", "have", "is", "was"], "a": "has"},
    {"q": "Neither of the boys ____ present.", "options": ["was", "were", "are", "have"], "a": "was"},
    {"q": "I am looking forward to ____ you.", "options": ["meet", "meeting", "met", "meets"], "a": "meeting"},
    {"q": "I prefer tea ____ coffee.", "options": ["than", "to", "from", "over"], "a": "to"},
    {"q": "Meaning of 'Break a leg':", "options": ["Good luck", "Bad luck", "Get angry", "To fall"], "a": "Good luck"},
    {"q": "If I ____ you, I wouldn't do that.", "options": ["am", "was", "were", "be"], "a": "were"},
    {"q": "He is ____ honest man.", "options": ["a", "an", "the", "no article"], "a": "an"},
    {"q": "The train ____ before I reached the station.", "options": ["left", "had left", "has left", "was leaving"], "a": "had left"},
    {"q": "Choose the correct spelling:", "options": ["Maintainance", "Maintenance", "Maintenence", "Maintainence"], "a": "Maintenance"}
]

# Randomize questions for the session so it stays interesting
if 'shuffled_indices' not in st.session_state:
    st.session_state.shuffled_indices = random.sample(range(len(questions_bank)), len(questions_bank))

# --- 3. HIGH-CONTRAST NEON STYLING ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Neon Question Card */
    .slide-card { 
        background-color: #0d0d0d; border: 3px solid #6c5ce7; 
        padding: 40px; border-radius: 25px; text-align: center;
        box-shadow: 0 0 30px #6c5ce744; margin-top: 20px;
    }
    
    .question-text { color: #00ffcc; font-size: 32px; font-weight: bold; margin-bottom: 25px; }
    
    /* Interactive MCQ Styling */
    .stButton>button { 
        background: linear-gradient(45deg, #6c5ce7, #00ffcc) !important; 
        color: #000 !important; font-weight: 900 !important; font-size: 20px !important;
        height: 65px; border-radius: 15px; border: none !important;
    }
    
    /* Radio Button Text Size */
    .stRadio [data-testid="stMarkdownContainer"] { 
        font-size: 24px !important; color: #ffffff !important; font-weight: 500;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DASHBOARD & NAVIGATION ---
st.markdown("<h1 style='text-align:center; color:#6c5ce7;'>⚡ ENGLISH GURU PRO ⚡</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 INTERACTIVE SLIDES", "📚 WORD VAULT", "📈 PROGRESS"])

with tab1:
    # Current question selection logic
    current_idx = st.session_state.shuffled_indices[st.session_state.q_index % len(questions_bank)]
    q_data = questions_bank[current_idx]

    st.markdown("<div class='slide-card'>", unsafe_allow_html=True)
    st.markdown(f"<p class='question-text'>{q_data['q']}</p>", unsafe_allow_html=True)
    
    # MCQ UI
    user_choice = st.radio("Sahi Jawab Chunein:", q_data['options'], key=f"q_{st.session_state.q_index}")
    
    st.write("---")
    
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("Submit Answer ✅"):
            if user_choice == q_data['a']:
                st.session_state.xp += 50
                st.balloons()
                st.success("Correct! +50 XP Earned.")
                time.sleep(1)
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.error(f"Opps! Correct answer was: {q_data['a']}")
                
    with c_btn2:
        if st.button("Next Slide ⏭️"):
            st.session_state.q_index += 1
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.write(f"Question Progress: {st.session_state.q_index + 1} / {len(questions_bank)}")

with tab2:
    st.subheader("Your Contextual Dictionary")
    with st.form("vault_form"):
        w = st.text_input("Naya Word:")
        m = st.text_input("Meaning/Sentence:")
        if st.form_submit_button("Add to Vault"):
            if w and m:
                st.session_state.vault.append(f"{w} : {m}")
                st.rerun()
    for item in reversed(st.session_state.vault):
        st.info(item)

with tab3:
    st.markdown(f"## Your Total XP: **{st.session_state.xp}**")
    st.bar_chart({"XP Growth": [0, 50, 100, 200, st.session_state.xp]})
    st.write("Keep going! Har slide par +50 XP milte hain.")

# Sidebar Reset
if st.sidebar.button("Hard Reset All Progress"):
    st.session_state.clear()
    st.rerun()
