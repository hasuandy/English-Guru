import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'achievements' not in st.session_state or isinstance(st.session_state.achievements, list):
    st.session_state.achievements = set()
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_index' not in st.session_state: st.session_state.q_index = 0

# --- 2. MEGA QUESTION BANK ---
questions = [
    {"q": "He ____ a doctor.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "They ____ to the park yesterday.", "a": ["go", "went", "going"], "c": "went"},
    {"q": "She ____ like apples.", "a": ["don't", "doesn't", "isn't"], "c": "doesn't"},
    {"q": "Neither of us ____ ready.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "I have ____ my lunch.", "a": ["eat", "ate", "eaten"], "c": "eaten"},
    {"q": "Choose the correct spelling:", "a": ["Recieve", "Receive", "Receve"], "c": "Receive"},
    {"q": "The sun ____ in the east.", "a": ["rise", "rises", "rising"], "c": "rises"},
    {"q": "Look! The baby ____.", "a": ["sleeps", "is sleeping", "sleep"], "c": "is sleeping"},
    {"q": "This book is ____ than that one.", "a": ["gooder", "better", "best"], "c": "better"},
    {"q": "He is afraid ____ spiders.", "a": ["of", "from", "with"], "c": "of"}
]

if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))

# --- 3. ACHIEVEMENT SYNC ---
def sync_badges():
    if not isinstance(st.session_state.achievements, set):
        st.session_state.achievements = set()
    if len(st.session_state.vault) >= 1: st.session_state.achievements.add("📖 Scholar")
    if st.session_state.xp >= 200: st.session_state.achievements.add("⚔️ Warrior")
    if st.session_state.xp >= 500: st.session_state.achievements.add("👑 Master")

sync_badges()

# --- 4. UI STYLING ---
st.set_page_config(page_title="English Guru V42", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Rajdhani', sans-serif; }
    .main-title { font-family: 'Bungee'; font-size: 3.5rem; text-align: center; color: #ff0055; text-shadow: 0 0 15px #ff0055; }
    .stat-card {
        background: rgba(255, 255, 255, 0.05); border: 2px solid #ff0055;
        border-radius: 15px; padding: 25px; text-align: center; margin-bottom: 20px;
    }
    .badge-card {
        background: rgba(255, 215, 0, 0.2); border: 1px solid #ffd700;
        border-radius: 10px; padding: 10px; margin-bottom: 5px;
        text-align: center; font-family: 'Bungee'; color: gold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-family:Bungee; color:#ff0055;'>WARRIOR HUB</h2>", unsafe_allow_html=True)
    st.metric("TOTAL XP", st.session_state.xp)
    st.write("---")
    st.markdown("### 🏅 ACHIEVEMENTS")
    for a in st.session_state.achievements:
        st.markdown(f"<div class='badge-card'>{a}</div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔴 RESET ALL PROGRESS"):
        st.session_state.clear()
        st.rerun()

# --- 6. MAIN CONTENT ---
st.markdown("<h1 class='main-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🏰 DASHBOARD", "👹 BOSS ARENA", "📚 WORD VAULT"])

with tab1:
    st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
    st.subheader("🔥 Current Standing")
    rank = "TRAINEE"
    if st.session_state.xp >= 500: rank = "MASTER"
    elif st.session_state.xp >= 200: rank = "WARRIOR"
    
    col1, col2 = st.columns(2)
    col1.metric("YOUR RANK", rank)
    col2.metric("XP EARNED", st.session_state.xp)
    
    st.write("---")
    st.write(f"📖 Words Collected in Vault: **{len(st.session_state.vault)}**")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp} / 500")
    st.progress(max(st.session_state.boss_hp / 500, 0.0))
    
    # Get current question
    q_idx = st.session_state.q_index % len(st.session_state.shuffled_questions)
    curr_q = st.session_state.shuffled_questions[q_idx]
    
    st.markdown(f"#### MISSION {st.session_state.q_index + 1}:")
    st.info(f"**{curr_q['q']}**")
    ans = st.radio("Choose your weapon:", curr_q['a'], key=f"q_{st.session_state.q_index}")
    
    if st.button("💥 ATTACK BOSS"):
        if ans == curr_q['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.success("✅ CRITICAL HIT! -100 Boss HP | +50 XP")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error(f"❌ MISSED! Correct answer was: {curr_q['c']}")
        
        st.session_state.q_index += 1
        sync_badges()
        time.sleep(1)
        st.rerun()

with tab3:
    st.header("Word Vault")
    w = st.text_input("New Intel (Word)")
    m = st.text_input("Meaning")
    if st.button("🔒 SEAL WORD"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            sync_badges()
            st.success("Knowledge Secured!")
            st.rerun()
    
    st.write("---")
    for item in st.session_state.vault:
        st.write(f"🔹 **{item['w']}**: {item['m']}")
