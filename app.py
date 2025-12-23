import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'achievements' not in st.session_state: st.session_state.achievements = set() # Duplicate rokne ke liye set
if 'current_q' not in st.session_state:
    st.session_state.current_q = random.randint(0, 4) # Random question start

# --- 2. QUESTIONS DATA BANK ---
questions = [
    {"q": "He ____ a doctor.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "They ____ to the park yesterday.", "a": ["go", "went", "going"], "c": "went"},
    {"q": "She ____ like apples.", "a": ["don't", "doesn't", "isn't"], "c": "doesn't"},
    {"q": "Neither of us ____ ready.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "I have ____ my lunch.", "a": ["eat", "ate", "eaten"], "c": "eaten"}
]

# --- 3. ACHIEVEMENT LOGIC ---
def sync_badges():
    if len(st.session_state.vault) >= 1:
        st.session_state.achievements.add("📖 Scholar")
    if st.session_state.xp >= 200:
        st.session_state.achievements.add("⚔️ Warrior")
    if st.session_state.xp >= 500:
        st.session_state.achievements.add("👑 Master")

sync_badges()

# --- 4. UI STYLING ---
st.set_page_config(page_title="English Guru V39", layout="wide")
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

# --- 6. MAIN TABS ---
st.markdown("<h1 class='main-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🏰 DASHBOARD", "👹 BOSS ARENA", "📚 WORD VAULT"])

with tab1:
    st.header("Welcome back!")
    st.write(f"Aapne ab tak {len(st.session_state.vault)} words seekhe hain.")
    st.area_chart({"Progress": [0, 20, 50, st.session_state.xp]})

with tab2:
    st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp} / 500")
    st.progress(st.session_state.boss_hp / 500)
    
    # Current Question logic
    idx = st.session_state.current_q
    q_data = questions[idx]
    
    st.markdown(f"#### Question: {q_data['q']}")
    ans = st.radio("Choose your weapon:", q_data['a'], key="battle_radio")
    
    if st.button("💥 FIRE ATTACK"):
        if ans == q_data['c']:
            dmg = 100
            st.session_state.xp += 100
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.success(f"CRITICAL HIT! +100 XP")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error("MISS! Wrong grammar.")
        
        # Attack ke baad naya question set karna
        st.session_state.current_q = (st.session_state.current_q + 1) % len(questions)
        sync_badges()
        time.sleep(1)
        st.rerun()

with tab3:
    st.write("### 📖 Word Vault")
    w = st.text_input("New Word")
    m = st.text_input("Meaning")
    
    if st.button("🔒 SAVE TO VAULT"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            sync_badges()
            st.success(f"'{w}' saved! Badge check triggered.")
            time.sleep(1)
            st.rerun()
