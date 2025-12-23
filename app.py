import streamlit as st
import pandas as pd
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# --- 2. QUESTIONS ---
questions = [
    {"q": "Choose the correct: 'She ____ English.'", "a": ["speak", "speaks", "speaking"], "c": "speaks"},
    {"q": "Past tense of 'Go' is:", "a": ["Goes", "Went", "Gone"], "c": "Went"},
    {"q": "I ____ a student.", "a": ["am", "is", "are"], "c": "am"},
    {"q": "They ____ playing.", "a": ["is", "am", "are"], "c": "are"}
]

# --- 3. UI STYLING ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    h1 { color: #4B39EF; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ English Guru")
    menu = st.radio("Navigation", ["Dashboard", "Battle Arena", "Word Vault"])
    st.write("---")
    if st.button("Reset Game"):
        st.session_state.clear()
        st.rerun()

# --- 5. PAGES ---

if menu == "Dashboard":
    st.title("🚀 Hero Dashboard")
    
    # Hero Stats Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Current XP", f"{st.session_state.xp} pts")
    c2.metric("Boss Health", f"{st.session_state.boss_hp} HP", delta="-100" if st.session_state.xp > 0 else "0")
    c3.metric("Words Learned", f"{len(st.session_state.vault)}")

    st.write("---")
    st.subheader("🏅 Your Badges")
    cols = st.columns(4)
    if len(st.session_state.vault) >= 1: cols[0].success("📖 Scholar")
    if st.session_state.xp >= 200: cols[1].success("⚔️ Warrior")
    if st.session_state.xp >= 500: cols[2].success("👑 Master")
    if not st.session_state.vault: st.info("Start learning to unlock badges!")

elif menu == "Battle Arena":
    st.title("👹 Grammar Battle")
    st.progress(st.session_state.boss_hp / 500)
    
    q = questions[st.session_state.q_idx % len(questions)]
    with st.container():
        st.markdown(f"### MISSION: {q['q']}")
        ans = st.radio("Select Weapon:", q['a'], key=f"battle_{st.session_state.q_idx}")
        
        if st.button("STRIKE! 💥"):
            if ans == q['c']:
                st.session_state.xp += 50
                st.session_state.boss_hp -= 100
                st.success("Correct Answer! Damage Dealt!")
                if st.session_state.boss_hp <= 0:
                    st.balloons()
                    st.session_state.boss_hp = 500
            else:
                st.error(f"Wrong! The correct answer was: {q['c']}")
            
            st.session_state.q_idx += 1
            time.sleep(1)
            st.rerun()

elif menu == "Word Vault":
    st.title("📖 Intel Vault (Words)")
    
    # Add Word Section
    with st.expander("➕ Add New Discovery", expanded=True):
        col1, col2 = st.columns(2)
        w = col1.text_input("New Word")
        m = col2.text_input("Meaning")
        if st.button("Lock Intel"):
            if w and m:
                st.session_state.vault.append({"Word": w, "Meaning": m})
                st.success("Word Encrypted into Vault!")
                st.rerun()

    st.write("---")
    
    # Display Section
    if st.session_state.vault:
        # Converting to DataFrame for a clean table look
        df = pd.DataFrame(st.session_state.vault)
        st.table(df) # Isse saare words ek saath saaf dikhenge
    else:
        st.info("Vault is empty. Go find some words!")
