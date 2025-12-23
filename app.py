import streamlit as st
import datetime
import time

# --- 1. SESSION STATE ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []

# --- 2. THEME & STYLING (Sabse Sharp Contrast) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Neon Boxes for each Task */
    .task-container { 
        background-color: #111111; 
        border: 3px solid #00ffcc; 
        padding: 25px; 
        border-radius: 15px; 
        margin-top: 20px;
    }
    
    /* Buttons Visibility */
    .stButton>button { 
        background: #00ffcc !important; 
        color: #000 !important; 
        font-weight: bold !important;
        font-size: 18px !important;
        height: 50px;
        border-radius: 10px;
    }
    
    /* Input Boxes (Typing) */
    input { 
        background-color: #222 !important; 
        color: #00ffcc !important; 
        border: 2px solid #ffffff !important;
        font-size: 20px !important;
    }

    /* Tab Text Color */
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-size: 20px !important; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom-color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛡️ ENGLISH GURU PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center;'>Current XP: {st.session_state.xp}</h3>", unsafe_allow_html=True)

# --- 4. TABS SYSTEM ---
tab1, tab2, tab3 = st.tabs(["📝 ACTIVE QUIZ", "📚 WORD VAULT", "📊 PROGRESS"])

# --- TAB 1: INTERACTIVE QUIZ (Sabse Main Section) ---
with tab1:
    st.markdown("### ⚡ Challenges Unlock")
    
    # Task 1: Typing Wala
    st.markdown("<div class='task-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#00ffcc;'>1. Typing Challenge (Fill in the Blank)</h2>", unsafe_allow_html=True)
    st.write("Question: **'I am ____ (go) to the market now.'**")
    
    user_type = st.text_input("Yahan sahi form type karein (go/went/going):", key="t_box")
    
    if st.button("Check Typing Answer 🔍"):
        if user_type.lower().strip() == "going":
            st.session_state.xp += 50
            st.success("Sahi Jawab! +50 XP")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Galat! 'Am' ke saath 'ing' lagta hai.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Task 2: Radio Button Wala
    st.markdown("<div class='task-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#00ffcc;'>2. Selection Challenge (Sentence Correction)</h2>", unsafe_allow_html=True)
    st.write("Choose the correct sentence:")
    
    selection = st.radio("Pick one:", [
        "Neither of them are here.",
        "Neither of them is here.",
        "Neither of them been here."
    ], key="r_box")
    
    if st.button("Submit Selection ✅"):
        if selection == "Neither of them is here.":
            st.session_state.xp += 50
            st.success("Correct! 'Neither' singular hota hai. +50 XP")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Galat! Grammar check karein.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: WORD VAULT ---
with tab2:
    st.subheader("Vocabulary Storage")
    with st.form("vault_form"):
        w = st.text_input("Word")
        m = st.text_input("Meaning")
        if st.form_submit_button("Save Word"):
            if w and m:
                st.session_state.vault.append(f"{w} : {m}")
                st.rerun()
    
    for item in reversed(st.session_state.vault):
        st.info(item)

# --- TAB 3: PROGRESS ---
with tab3:
    st.subheader("Your XP Growth")
    st.bar_chart({"XP": [10, 40, 60, st.session_state.xp]})
