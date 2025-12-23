import streamlit as st
import datetime
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'daily_goal' not in st.session_state: st.session_state.daily_goal = 500

# --- 2. HIGH-VISIBILITY NEON THEME ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Neon Cards */
    .card { 
        background-color: #0d0d0d; border: 2px solid #00ffcc; 
        padding: 20px; border-radius: 15px; margin-bottom: 20px; 
        box-shadow: 0 0 10px #00ffcc33;
    }
    
    .neon-text { color: #00ffcc; font-weight: bold; font-size: 22px; }
    
    /* Buttons */
    .stButton>button { 
        background: linear-gradient(45deg, #00ffcc, #6c5ce7) !important; 
        color: #000 !important; font-weight: 900 !important;
        height: 50px; width: 100%; border-radius: 12px; border: none !important;
    }
    
    /* Metrics and Inputs */
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-size: 40px !important; }
    input { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VISUAL PROGRESS DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>📊 MY LEARNING DASHBOARD</h1>", unsafe_allow_html=True)

col_stats, col_chart = st.columns([1, 2])

with col_stats:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.metric("Total XP Earned", st.session_state.xp)
    progress_val = min(st.session_state.xp / st.session_state.daily_goal, 1.0)
    st.write(f"Daily Goal: {st.session_state.xp} / {st.session_state.daily_goal} XP")
    st.progress(progress_val)
    if progress_val >= 1.0:
        st.success("🎯 Goal Reached! You are a Rockstar.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### 📈 Your XP Growth")
    # Generating a simple chart based on session XP
    st.bar_chart({"Day Activity": [20, 50, 100, 40, st.session_state.xp]})
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. NAVIGATION TABS ---
st.write("---")
tabs = st.tabs(["⚡ INTERACTIVE QUIZ", "🧠 SMART SRS REVIEW", "📚 WORD VAULT"])

# --- TAB 1: INTERACTIVE QUIZ (Fill + Correction) ---
with tabs[0]:
    st.subheader("Challenge Your Skills")
    
    # Fill in the Blanks
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='neon-text'>✍️ Fill in the Blank</p>", unsafe_allow_html=True)
    st.write("Question: 'Neither of the answers ____ correct.'")
    fill_input = st.text_input("Type 'is' or 'are':", key="fill_q")
    if st.button("Check My Answer"):
        if fill_input.lower().strip() == "is":
            st.session_state.xp += 50
            st.success("Correct! 'Neither' is singular. +50 XP")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Incorrect. Remember: Neither/Either take a singular verb.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Sentence Correction
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<p class='neon-text'>🛠️ Sentence Correction</p>", unsafe_allow_html=True)
    st.write("Incorrect: *'I have saw that movie yesterday.'*")
    correction = st.radio("Pick the correct version:", [
        "I saw that movie yesterday.",
        "I have seen that movie yesterday.",
        "I seen that movie yesterday."
    ])
    if st.button("Submit Correction ✅"):
        if correction == "I saw that movie yesterday.":
            st.session_state.xp += 50
            st.success("Perfect! Use Simple Past for finished time. +50 XP")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Wrong choice. Keep practicing tenses!")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: SRS REVIEW ---
with tabs[1]:
    st.subheader("Smart Spaced Repetition")
    
    today = datetime.date.today()
    due_words = [w for w in st.session_state.vault if w['review_date'] <= today]
    
    if not due_words:
        st.info("No words to review today! Add more words in the Vault.")
    else:
        for i, word_item in enumerate(due_words):
            with st.expander(f"Review: {word_item['word']}"):
                st.write("Think of the meaning...")
                if st.button(f"Show Result for {word_item['word']}", key=f"sr_{i}"):
                    st.markdown(f"<span style='color:#00ffcc; font-size:20px;'>{word_item['meaning']}</span>", unsafe_allow_html=True)
                if st.button(f"I Remembered! ✅", key=f"ok_{i}"):
                    st.session_state.xp += 30
                    # Update SRS date to 4 days later
                    word_item['review_date'] = today + datetime.timedelta(days=4)
                    st.rerun()

# --- TAB 3: WORD VAULT ---
with tabs[2]:
    st.subheader("Add Vocabulary with Context")
    with st.form("add_vocab"):
        w = st.text_input("New Word")
        m = st.text_input("Meaning or Sentence")
        if st.form_submit_button("Secure in Vault 🔒"):
            if w and m:
                st.session_state.vault.append({
                    "word": w, "meaning": m, "review_date": datetime.date.today()
                })
                st.success("Word added to SRS Practice!")
                st.rerun()
    
    st.write("---")
    st.subheader("My Saved Dictionary")
    for item in reversed(st.session_state.vault):
        st.markdown(f"<div class='card'><b>{item['word']}</b> : {item['meaning']} <br><small>Next Review: {item['review_date']}</small></div>", unsafe_allow_html=True)

# Sidebar Reset
if st.sidebar.button("Hard Reset Progress"):
    st.session_state.clear()
    st.rerun()
