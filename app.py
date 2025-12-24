import streamlit as st
import random
import time

# --- 1. SESSION STATE (Game Data) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'user' not in st.session_state: st.session_state.user = "Hero Warrior"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'level' not in st.session_state: st.session_state.level = 1

# --- 2. UI & STYLING ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; font-family: 'Segoe UI', sans-serif; }
    .gaming-card { 
        background: rgba(0, 242, 255, 0.05); 
        border: 2px solid #00f2ff; 
        border-radius: 15px; padding: 25px; text-align: center;
        box-shadow: 0px 0px 15px #00f2ff;
    }
    .stButton>button { 
        background: linear-gradient(45deg, #00f2ff, #7000ff); 
        color: white !important; font-weight: bold; border-radius: 10px; border: none; height: 50px;
    }
    .stMetric { background: #1a1c24; padding: 10px; border-radius: 10px; border-left: 5px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🎮 GURU MENU")
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=100)
    st.header(f"Level: {st.session_state.level}")
    st.metric("Total XP", st.session_state.xp)
    st.divider()
    page = st.radio("Chose Your Mission:", ["🏠 Base", "🎓 Training", "⚔️ Boss Battle", "⚙️ Profile"])

# --- 4. PAGE: BASE ---
if page == "🏠 Base":
    st.title("🏠 Command Center")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class='gaming-card'>
            <h1>Welcome Back, {st.session_state.user}!</h1>
            <p>Aapka mission hai English seekhna aur Boss ko harana.</p>
            <h2 style='color:#00f2ff;'>Rank: Elite Learner</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.info("💡 Tip: Training karke XP kamao, tabhi Boss se lad paoge!")

# --- 5. PAGE: TRAINING (QUIZ) ---
elif page == "🎓 Training":
    st.title("🎓 Vocabulary Training")
    questions = [
        {"q": "Meaning of 'VIBRANT'?", "o": ["Dull", "Energetic", "Small"], "a": "Energetic"},
        {"q": "Past tense of 'RUN'?", "o": ["Runned", "Running", "Ran"], "a": "Ran"},
        {"q": "Opposite of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy"], "a": "Modern"}
    ]
    
    q = random.choice(questions)
    st.markdown(f"<div class='gaming-card'><h3>QUESTION: {q['q']}</h3></div>", unsafe_allow_html=True)
    
    ans = st.radio("Choose correct answer:", q["o"])
    
    if st.button("Submit Answer"):
        if ans == q["a"]:
            st.session_state.xp += 20
            st.success("🔥 Sahi Jawab! +20 XP")
            st.balloons()
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Galat! Phir se koshish karo.")

# --- 6. PAGE: BOSS BATTLE ---
elif page == "⚔️ Boss Battle":
    st.title("⚔️ Final Boss Fight")
    
    col1, col2 = st.columns(2)
    with col1: st.metric("Your Health", "100%")
    with col2: st.metric("Boss Health", f"{st.session_state.boss_hp}%")
    
    st.progress(st.session_state.boss_hp / 100)
    
    if st.button("🔥 POWER ATTACK (Requires XP)"):
        if st.session_state.xp >= 10:
            damage = random.randint(20, 35)
            st.session_state.boss_hp -= damage
            st.session_state.xp -= 10
            st.warning(f"Aapne Boss ko {damage} ka damage diya!")
            
            if st.session_state.boss_hp <= 0:
                st.success("🏆 VICTORY! Boss ko hara diya!")
                st.session_state.boss_hp = 100
                st.session_state.level += 1
            st.rerun()
        else:
            st.error("Nahi! Aapke paas kam se kam 10 XP hone chahiye attack karne ke liye.")

# --- 7. PAGE: PROFILE ---
elif page == "⚙️ Profile":
    st.title("⚙️ Profile Settings")
    new_name = st.text_input("Hero Name Badlo:", st.session_state.user)
    if st.button("Save Name"):
        st.session_state.user = new_name
        st.success("Naam badal gaya!")
        st.rerun()
