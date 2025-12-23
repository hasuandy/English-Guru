import streamlit as st
import datetime
import time

# --- 1. INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'quiz_step' not in st.session_state: st.session_state.quiz_step = 1

# --- 2. THEME & STYLING (Extra Contrast) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Neon Boxes for High Visibility */
    .quiz-box { 
        background-color: #0d0d0d; border: 3px solid #00ffcc; 
        padding: 25px; border-radius: 20px; margin-bottom: 25px; 
        box-shadow: 0 0 15px #00ffcc;
    }
    
    .instruction-text { color: #ffcc00; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
    .neon-label { color: #00ffcc; font-weight: bold; font-size: 24px; }
    
    /* Buttons */
    .stButton>button { 
        background: #00ffcc !important; color: #000 !important; 
        font-weight: 900 !important; height: 55px; border-radius: 12px;
    }
    
    /* Input Fields Visibility */
    input { 
        background-color: #1a1a1a !important; color: #00ffcc !important; 
        border: 2px solid #00ffcc !important; font-size: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. TOP DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🌟 INTERACTIVE LEARNING HUB</h1>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
c1.metric("🏆 TOTAL XP", st.session_state.xp)
c2.metric("📖 WORDS SAVED", len(st.session_state.vault))
st.write("---")

# --- 4. NAVIGATION ---
tabs = st.tabs(["⚡ ACTIVE QUIZ", "📚 WORD VAULT", "📊 PROGRESS"])

# --- TAB 1: INTERACTIVE QUIZ (Fill in Blanks & Correction) ---
with tabs[0]:
    st.markdown("<p class='instruction-text'>Niche diye gaye sawalon ko dhyan se padhein aur solve karein:</p>", unsafe_allow_html=True)

    # --- SECTION A: FILL IN THE BLANK (TYPING) ---
    st.markdown("<div class='quiz-box'>", unsafe_allow_html=True)
    st.markdown("<p class='neon-label'>Task 1: Fill in the Blank (Type Karo)</p>", unsafe_allow_html=True)
    st.write("### Question: 'She has been working here ____ 2018.'")
    
    # Typing box for user
    user_typed = st.text_input("Apna jawab yahan type karein (since / for):", placeholder="Type here...", key="fill_type_box")
    
    if st.button("Jawab Check Karein 🔍"):
        if user_typed.lower().strip() == "since":
            st.session_state.xp += 50
            st.success("Correct! 'Since' is used for a fixed point in time. +50 XP")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Incorrect! Correct answer is 'since' because 2018 is a fixed year.")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- SECTION B: SENTENCE CORRECTION (RADIO BUTTONS) ---
    st.markdown("<div class='quiz-box'>", unsafe_allow_html=True)
    st.markdown("<p class='neon-label'>Task 2: Sentence Correction (Option Chuno)</p>", unsafe_allow_html=True)
    st.write("### Choose the grammatically correct sentence:")
    
    # Radio buttons for selection
    options = [
        "He don't has any money.",
        "He doesn't has any money.",
        "He doesn't have any money."
    ]
    user_choice = st.radio("Sahi option par click karein:", options, key="radio_correction_box")
    
    if st.button("Option Submit Karein ✅"):
        if user_choice == "He doesn't have any money.":
            st.session_state.xp += 50
            st.success("Perfect! 'Does' ke saath hamesha base form 'have' lagta hai. +50 XP")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Wrong! Focus on 'Does' + 'Have' rule.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: WORD VAULT ---
with tabs[1]:
    st.subheader("Add Vocabulary with Context")
    with st.form("vault_form"):
        w = st.text_input("Word")
        m = st.text_input("Meaning")
        if st.form_submit_button("Vault mein Save karein"):
            if w and m:
                st.session_state.vault.append({"word": w, "meaning": m})
                st.success("Word saved!")
                st.rerun()
    
    for item in reversed(st.session_state.vault):
        st.markdown(f"<div class='quiz-box'><b>{item['word']}</b> : {item['meaning']}</div>", unsafe_allow_html=True)

# --- TAB 3: PROGRESS ---
with tabs[2]:
    st.subheader("Your Growth Chart")
    st.bar_chart({"XP Progress": [10, 30, 70, st.session_state.xp]})
