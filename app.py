import streamlit as st
import datetime
import time

# --- 1. INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'daily_goal' not in st.session_state: st.session_state.daily_goal = 200

# --- 2. THEME & STYLING (Neon High Contrast) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .card { 
        background-color: #0a0a0a; border: 2px solid #00ffcc; 
        padding: 20px; border-radius: 15px; margin-bottom: 15px; 
    }
    .goal-text { color: #ffcc00; font-weight: bold; font-size: 18px; }
    .neon-text { color: #00ffcc; font-weight: bold; font-size: 20px; }
    .stButton>button { background: #00ffcc !important; color: black !important; font-weight: bold; border-radius: 10px; height: 50px; }
    input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI HEADER ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛡️ ENGLISH GURU PRO</h1>", unsafe_allow_html=True)

# --- 4. DASHBOARD (Visual Progress & Daily Goals) ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 Visual Progress")
col1, col2 = st.columns(2)

with col1:
    st.metric("🏆 Your Total XP", st.session_state.xp)
    progress = min(st.session_state.xp / st.session_state.daily_goal, 1.0)
    st.write(f"Daily Goal: **{st.session_state.xp}/{st.session_state.daily_goal} XP**")
    st.progress(progress)
    if progress >= 1.0:
        st.success("🎉 Daily Goal Achieved!")

with col2:
    st.write("### Learning Activity")
    # Ek simple graph progress dikhane ke liye
    st.bar_chart({"XP": [10, 40, 25, st.session_state.xp]})
st.markdown("</div>", unsafe_allow_html=True)

# --- 5. MAIN NAVIGATION ---
tabs = st.tabs(["📝 EXPERT QUIZ", "🧠 SRS REVIEW", "📚 WORD VAULT"])

# --- TAB 1: INTERACTIVE QUIZ (Fill in the Blanks & Correction) ---
with tabs[0]:
    st.subheader("⚡ Expert Challenges")
    
    # 1. Fill in the Blanks
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("**1. Fill in the blank:**")
    st.write("I have been living here ____ five years.")
    blank_ans = st.text_input("Type your answer (for/since):", key="blank_1")
    if st.button("Check Blank"):
        if blank_ans.lower() == "for":
            st.session_state.xp += 20
            st.success("Sahi! Duration ke liye 'for' lagta hai. +20 XP")
        else:
            st.error("Galat! Fixed time ke liye 'since' aur duration ke liye 'for' lagta hai.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Sentence Correction
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("**2. Sentence Correction:**")
    st.write("Incorrect: *'He do not has a car.'*")
    correct_ans = st.radio("Choose the correct sentence:", [
        "He does not have a car.",
        "He do not have a car.",
        "He does not has a car."
    ])
    if st.button("Correct Sentence ✅"):
        if correct_ans == "He does not have a car.":
            st.session_state.xp += 30
            st.success("Excellent! 'Does' ke baad hamesha 'have' lagta hai. +30 XP")
        else:
            st.error("Try again! Negative sentences mein 'does not have' use hota hai.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: SRS REVIEW ---
with tabs[1]:
    st.subheader("🧠 Spaced Repetition Review")
    today = datetime.date.today()
    due_words = [w for w in st.session_state.vault if w['review_date'] <= today]
    
    if not due_words:
        st.info("No words due for review. Add more words in the Vault!")
    else:
        for i, word_data in enumerate(due_words):
            with st.expander(f"Review Word: {word_data['word']}"):
                st.write(f"What is the meaning?")
                if st.button("Show Meaning", key=f"show_{i}"):
                    st.write(f"**Meaning:** {word_data['meaning']}")
                if st.button("I Remembered This ✅", key=f"rem_{i}"):
                    st.session_state.xp += 15
                    word_data['review_date'] = today + datetime.timedelta(days=3)
                    st.rerun()

# --- TAB 3: WORD VAULT ---
with tabs[2]:
    st.subheader("Add New Word")
    with st.form("add_word_vault"):
        new_w = st.text_input("Word")
        new_m = st.text_input("Meaning")
        if st.form_submit_button("Save Word"):
            if new_w and new_m:
                st.session_state.vault.append({
                    "word": new_w, 
                    "meaning": new_m, 
                    "review_date": datetime.date.today()
                })
                st.success("Word added to SRS!")
                st.rerun()

    for item in reversed(st.session_state.vault):
        st.markdown(f"<div class='card'>{item['word']} : {item['meaning']}</div>", unsafe_allow_html=True)

# Reset Progress
if st.sidebar.button("Reset Everything"):
    st.session_state.clear()
    st.rerun()
