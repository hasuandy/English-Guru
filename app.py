import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="English Guru", page_icon="📝")

# Data save karne ke liye
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'name' not in st.session_state: st.session_state.name = "Warrior"

# --- SIMPLE STYLE ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        height: 3em;
        background-color: #007bff;
        color: white;
        border-radius: 10px;
    }
    .score-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("👤 Profile")
    st.session_state.name = st.text_input("Aapka Naam:", st.session_state.name)
    st.write(f"### ⭐ XP: {st.session_state.xp}")
    st.divider()
    page = st.radio("Kahan jana hai?", ["Home", "Practice Quiz"])

# --- PAGES ---
if page == "Home":
    st.title(f"Welcome, {st.session_state.name}! 👋")
    st.markdown(f"""
    <div class="score-box">
        <h3>Aapka Current Score</h3>
        <h1 style="color: #007bff;">{st.session_state.xp} XP</h1>
    </div>
    """, unsafe_allow_html=True)
    st.write("\n\nSide menu se **Practice Quiz** chuno aur points kamao!")

elif page == "Practice Quiz":
    st.title("✍️ Quick Quiz")
    
    # Simple Question
    st.subheader("What is the opposite of 'HAPPY'?")
    ans = st.radio("Sahi jawab chuno:", ["Angry", "Sad", "Funny"])
    
    if st.button("Check Jawab"):
        if ans == "Sad":
            st.session_state.xp += 10
            st.success("Bilkul Sahi! +10 XP mil gaye.")
            st.balloons()
        else:
            st.error("Galat jawab! Phir se koshish karo.")

    if st.button("Naya Sawal"):
        st.rerun()
