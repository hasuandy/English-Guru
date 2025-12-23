import streamlit as st
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'streak' not in st.session_state: st.session_state.streak = 1
if 'level' not in st.session_state: st.session_state.level = "Beginner"

# --- 2. THEME & STYLING ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .nav-btn { background: #6c5ce7 !important; color: white !important; border-radius: 10px !important; }
    .badge-icon { font-size: 40px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Progress Tracker & Gamification) ---
with st.sidebar:
    st.title("👤 My Profile")
    st.metric("Total XP", st.session_state.xp)
    st.metric("🔥 Daily Streak", f"{st.session_state.streak} Days")
    st.write(f"**Current Rank:** {st.session_state.level}")
    st.progress(min(st.session_state.xp / 1000, 1.0))
    st.write("Next Goal: 1000 XP")
    
    st.write("---")
    st.subheader("🏅 Badges")
    if st.session_state.xp >= 100: st.write("✅ Early Bird")
    if len(st.session_state.vault) >= 5: st.write("✅ Word Master")
    
    if st.button("Reset All Progress", type="secondary"):
        st.session_state.clear()
        st.rerun()

# --- 4. MAIN NAVIGATION ---
st.title("🚀 English Guru Learning Path")
tabs = st.tabs(["📚 Lessons", "⚔️ Practice", "📖 Vocabulary", "📈 Dashboard"])

# --- TAB 1: STRUCTURED LESSONS (Grammar & Reading) ---
with tabs[0]:
    st.subheader("Choose Your Module")
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📝 Grammar: Tenses (Present Simple)", expanded=True):
            st.write("Rule: Subject + V1 (s/es) + Object")
            st.code("Example: He drinks water.")
            if st.button("Mark as Completed"):
                st.session_state.xp += 20
                st.success("+20 XP Earned!")
                
    with col2:
        with st.expander("📖 Reading: Short Story"):
            st.write("*The brave lion lived in a big forest...*")
            st.write("**New Word:** Forest (Jungle)")
            if st.button("Finish Reading"):
                st.session_state.xp += 15
                st.rerun()

# --- TAB 2: INTERACTIVE PRACTICE (Speaking & Listening) ---
with tabs[1]:
    st.subheader("Interactive Practice")
    choice = st.selectbox("Select Activity", ["Listening (Audio)", "Speaking (Bypass AI)", "Daily Quiz"])
    
    if choice == "Listening (Audio)":
        st.info("Listen to the dialogue and repeat.")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder Audio
        st.write("Speed: 1x (Standard)")
        
    elif choice == "Speaking (Bypass AI)":
        st.warning("AI Pronunciation Feedback: [BYPASSED]")
        st.write("Try saying: 'I want to improve my English.'")
        st.button("Start Recording (Simulation)")
        
    elif choice == "Daily Quiz":
        q = st.radio("Correct this: 'They ___ my friends.'", ["is", "am", "are"])
        if st.button("Submit Quiz"):
            if q == "are":
                st.session_state.xp += 50
                st.success("Correct! +50 XP")
            else:
                st.error("Wrong! Feedback: 'They' is plural, so we use 'are'.")

# --- TAB 3: VOCABULARY BUILDER (SRS System) ---
with tabs[2]:
    st.subheader("Interactive Flashcards")
    c1, c2 = st.columns(2)
    with c1:
        new_w = st.text_input("New English Word")
        new_m = st.text_input("Meaning/Context")
        if st.button("Add to Flashcards"):
            if new_w and new_m:
                st.session_state.vault.append({"w": new_w, "m": new_m, "review": "Today"})
                st.success("Added!")

    st.write("---")
    st.subheader("Your Flashcards (Spaced Repetition)")
    if not st.session_state.vault:
        st.write("No words yet.")
    else:
        for item in st.session_state.vault:
            with st.container():
                st.markdown(f"<div class='main-card'><b>{item['w']}</b>: {item['m']} <br><small>Next Review: {item['review']}</small></div>", unsafe_allow_html=True)

# --- TAB 4: VISUAL DASHBOARD ---
with tabs[3]:
    st.subheader("Learning Analytics")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Words Mastered", len(st.session_state.vault))
    col_b.metric("Lessons Completed", st.session_state.xp // 50)
    col_c.metric("Goal Progress", f"{(st.session_state.xp / 1000) * 100}%")
    
    # Simple Progress Chart
    st.write("### Weekly Activity")
    st.bar_chart({"XP": [10, 20, 5, 40, st.session_state.xp % 100]})
