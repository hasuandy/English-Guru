import streamlit as st
import datetime
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'daily_goal' not in st.session_state: st.session_state.daily_goal = 500
if 'q_index' not in st.session_state: st.session_state.q_index = 0

# --- 2. QUESTION BANK (Grammar & Correction) ---
questions = [
    {"type": "fill", "q": "I have been waiting ___ two hours.", "a": "for", "hint": "Duration ke liye 'for' use karein."},
    {"type": "fill", "q": "She ___ (work) in this office since 2015.", "a": "has been working", "hint": "Present Perfect Continuous use karein."},
    {"type": "correct", "q": "Incorrect: 'Every students like the teacher.'", "options": ["Every student likes the teacher.", "Every student like the teacher.", "Every students likes the teacher."], "a": "Every student likes the teacher."},
    {"type": "fill", "q": "If I ___ you, I would go there.", "a": "were", "hint": "Imaginary situations mein 'were' lagta hai."},
    {"type": "correct", "q": "Incorrect: 'She is more taller than me.'", "options": ["She is taller than me.", "She is more tall than me.", "She is more tallest than me."], "a": "She is taller than me."}
]

# --- 3. HIGH-VISIBILITY NEON THEME ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .card { 
        background-color: #0d0d0d; border: 2px solid #00ffcc; 
        padding: 20px; border-radius: 15px; margin-bottom: 20px; 
    }
    .neon-text { color: #00ffcc; font-weight: bold; font-size: 22px; }
    .stButton>button { 
        background: linear-gradient(45deg, #00ffcc, #6c5ce7) !important; 
        color: #000 !important; font-weight: 900 !important;
        height: 45px; width: 100%; border-radius: 10px; border: none !important;
    }
    input { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VISUAL DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🚀 ENGLISH GURU DASHBOARD</h1>", unsafe_allow_html=True)

col_stats, col_graph = st.columns([1, 2])
with col_stats:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.metric("Total XP", st.session_state.xp)
    prog = min(st.session_state.xp / st.session_state.daily_goal, 1.0)
    st.write(f"Goal: {st.session_state.xp}/{st.session_state.daily_goal} XP")
    st.progress(prog)
    st.markdown("</div>", unsafe_allow_html=True)

with col_graph:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### Weekly Performance")
    st.line_chart({"XP": [50, 80, 40, 150, st.session_state.xp]})
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. NAVIGATION ---
tabs = st.tabs(["⚡ PRACTICE QUIZ", "🧠 SRS REVIEW", "📚 WORD VAULT"])

# --- TAB 1: INTERACTIVE QUIZ ---
with tabs[0]:
    curr_q = questions[st.session_state.q_index % len(questions)]
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<p class='neon-text'>Question Type: {curr_q['type'].upper()}</p>", unsafe_allow_html=True)
    st.write(f"### {curr_q['q']}")
    
    if curr_q['type'] == "fill":
        user_ans = st.text_input("Apna jawab likhein:", key=f"q_{st.session_state.q_index}")
        if st.button("Check Answer ✅"):
            if user_ans.lower().strip() == curr_q['a'].lower():
                st.session_state.xp += 50
                st.success(f"Sahi! +50 XP. {curr_q['hint']}")
                st.session_state.q_index += 1
                time.sleep(1)
                st.rerun()
            else:
                st.error("Galat jawab! Phir se koshish karein.")
    
    else: # Correct the sentence type
        user_choice = st.radio("Sahi option chunein:", curr_q['options'], key=f"r_{st.session_state.q_index}")
        if st.button("Submit Correction"):
            if user_choice == curr_q['a']:
                st.session_state.xp += 50
                st.success("Bilkul Sahi! +50 XP")
                st.session_state.q_index += 1
                time.sleep(1)
                st.rerun()
            else:
                st.error("Ye galat hai. Grammar par dhyan dein.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- TAB 2: SRS REVIEW ---
with tabs[1]:
    st.subheader("Smart Vocabulary Review")
    
    due_words = [w for w in st.session_state.vault if w['review_date'] <= datetime.date.today()]
    
    if not due_words:
        st.info("Revision ke liye abhi koi word nahi hai.")
    else:
        for i, item in enumerate(due_words):
            with st.expander(f"Recall: {item['word']}"):
                if st.button(f"Meaning Dekhein", key=f"sh_{i}"):
                    st.write(f"**Matlab:** {item['meaning']}")
                if st.button(f"Yaad hai! ✅", key=f"ok_{i}"):
                    st.session_state.xp += 20
                    item['review_date'] = datetime.date.today() + datetime.timedelta(days=4)
                    st.rerun()

# --- TAB 3: WORD VAULT ---
with tabs[2]:
    st.subheader("Naya Word Add Karein")
    with st.form("vault_form"):
        w = st.text_input("English Word")
        m = st.text_input("Hindi Meaning")
        if st.form_submit_button("Vault mein Dalein"):
            if w and m:
                st.session_state.vault.append({"word": w, "meaning": m, "review_date": datetime.date.today()})
                st.success("Word save ho gaya!")
                st.rerun()
    
    st.write("---")
    for item in reversed(st.session_state.vault):
        st.markdown(f"<div class='card'><b>{item['word']}</b> : {item['meaning']}</div>", unsafe_allow_html=True)

# RESET
if st.sidebar.button("Clear All Progress"):
    st.session_state.clear()
    st.rerun()
