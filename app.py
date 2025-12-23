import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION (Anti-Crash Logic) ---
# Agar purani memory List hai, toh usey Set mein convert kar dega
if 'achievements' not in st.session_state or isinstance(st.session_state.achievements, list):
    st.session_state.achievements = set()

if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'current_q' not in st.session_state: st.session_state.current_q = 0

# --- 2. QUESTIONS DATA BANK ---
questions = [
    {"q": "He ____ a doctor.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "They ____ to the park yesterday.", "a": ["go", "went", "going"], "c": "went"},
    {"q": "She ____ like apples.", "a": ["don't", "doesn't", "isn't"], "c": "doesn't"},
    {"q": "Neither of us ____ ready.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "I have ____ my lunch.", "a": ["eat", "ate", "eaten"], "c": "eaten"},
    {"q": "Choose the correct spelling:", "a": ["Recieve", "Receive", "Receve"], "c": "Receive"},
    {"q": "Look! The sun ____.", "a": ["is rising", "rises", "rise"], "c": "is rising"}
]

# --- 3. ACHIEVEMENT LOGIC ---
def sync_badges():
    # Safety Check: Ensure achievements is a set
    if not isinstance(st.session_state.achievements, set):
        st.session_state.achievements = set()
        
    if len(st.session_state.vault) >= 1:
        st.session_state.achievements.add("📖 Scholar")
    if st.session_state.xp >= 200:
        st.session_state.achievements.add("⚔️ Warrior")
    if st.session_state.xp >= 500:
        st.session_state.achievements.add("👑 Master")

# Har baar refresh par badges sync honge
sync_badges()

# --- 4. UI STYLING ---
st.set_page_config(page_title="English Guru V40", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp { background: #050505; color: #00f2ff; }
    .main-title { font-family: 'Bungee'; font-size: 3rem; text-align: center; color: #ff0055; text-shadow: 0 0 15px #ff0055; }
    .badge-card {
        background: rgba(255, 215, 0, 0.2); border: 2px solid #ffd700;
        border-radius: 10px; padding: 10px; margin-bottom: 5px;
        text-align: center; font-family: 'Bungee'; color: gold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-family:Bungee; color:#ff0055;'>WARRIOR STATS</h2>", unsafe_allow_html=True)
    st.metric("Total XP", st.session_state.xp)
    st.write("---")
    st.markdown("### 🏅 ACHIEVEMENTS")
    if not st.session_state.achievements:
        st.write("Unlock badges by training!")
    else:
        for a in st.session_state.achievements:
            st.markdown(f"<div class='badge-card'>{a}</div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔴 Reset All Data"):
        st.session_state.clear()
        st.rerun()

# --- 6. MAIN TABS ---
st.markdown("<h1 class='main-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🏰 DASHBOARD", "👹 BOSS ARENA", "📚 WORD VAULT"])

with tab1:
    st.header("Hero Dashboard")
    st.write(f"Words Learned: {len(st.session_state.vault)}")
    st.progress(min(st.session_state.xp / 1000, 1.0))
    st.write("Next Milestone at 1000 XP")

with tab2:
    st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp} / 500")
    st.progress(max(st.session_state.boss_hp / 500, 0.0))
    
    idx = st.session_state.current_q % len(questions)
    q_data = questions[idx]
    
    st.markdown(f"#### Question: {q_data['q']}")
    ans = st.radio("Choose your weapon:", q_data['a'], key=f"q_{idx}")
    
    if st.button("💥 FIRE ATTACK"):
        if ans == q_data['c']:
            st.session_state.xp += 100
            st.session_state.boss_hp -= 100
            st.success("CRITICAL HIT! +100 XP")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error("MISS! Your grammar failed you.")
        
        st.session_state.current_q += 1 # Next question logic
        sync_badges()
        time.sleep(1)
        st.rerun()

with tab3:
    st.write("### 📖 Store Knowledge")
    w = st.text_input("New Word")
    m = st.text_input("Meaning")
    if st.button("🔒 SAVE"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            sync_badges()
            st.success("Intel stored in Vault!")
            time.sleep(1)
            st.rerun()
