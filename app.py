import streamlit as st
import random
import time
import pandas as pd
from datetime import date, timedelta

# --- 1. SESSION STATE (Initialization) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'theme' not in st.session_state: st.session_state.theme = "#00f2ff"
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100
if 'battle_log' not in st.session_state: st.session_state.battle_log = "Monster is approaching! 👹"
if 'combo' not in st.session_state: st.session_state.combo = 0
if 'q_index' not in st.session_state: st.session_state.q_index = 0

# --- 2. 200+ QUESTIONS DATASET ---
MCQ_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Past tense of 'EAT'?", "o": ["Eaten", "Ate", "Eats", "Eating"], "a": "Ate"},
    {"q": "Spell 'Mausam'?", "o": ["Wether", "Weather", "Whether", "Waether"], "a": "Weather"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Heavy"], "a": "Quick"},
    {"q": "If I ____ rich, I would travel.", "o": ["am", "was", "were", "be"], "a": "were"},
    {"q": "Neither of the boys ____ here.", "o": ["is", "are", "were", "have"], "a": "is"},
    {"q": "She prefers tea ____ coffee.", "o": ["than", "to", "over", "from"], "a": "to"},
    {"q": "Correct spelling?", "o": ["Receive", "Recieve", "Receve", "Riceive"], "a": "Receive"}
] # Note: Aap is list mein 200+ questions add kar sakte hain.

# --- 3. UI & STYLING ---
st.set_page_config(page_title="English Guru Pro", page_icon="⚡", layout="wide")
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(135deg, #0d0d1a 0%, #1a1a2e 100%); color: white; }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px;
        border: 2px solid {st.session_state.theme}; text-align: center; margin-bottom: 20px;
        box-shadow: 0 0 15px {st.session_state.theme}55;
    }
    .hp-bar {{ height: 20px; border-radius: 10px; background: #333; overflow: hidden; margin: 10px 0; }}
    .hp-fill {{ height: 100%; transition: width 0.5s ease; }}
    .stButton>button {{
        background: linear-gradient(45deg, #00dbde 0%, {st.session_state.theme} 100%);
        color: white; border-radius: 15px; font-weight: bold; border:none; height: 50px; width: 100%;
    }}
    h1, h2, h3 {{ color: {st.session_state.theme}; text-shadow: 0 0 10px {st.session_state.theme}55; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1>⚡ GURU ARENA</h1>", unsafe_allow_html=True)
    page = st.radio("MISSIONS:", ["🏠 Dashboard", "🚀 MCQ Slides", "⚔️ Boss Battle", "🗂️ Word Vault"])
    if st.button("Reset Progress"):
        st.session_state.clear()
        st.rerun()

# --- 5. APP PAGES ---

if page == "🏠 Dashboard":
    st.markdown("<h1>MISSION CONTROL</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'>🏆<br>TOTAL XP<h3>{st.session_state.xp}</h3></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'>🎖️<br>RANK<h3>{'LEGEND' if st.session_state.xp > 500 else 'WARRIOR'}</h3></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'>🔥<br>STREAK<h3>1 Day</h3></div>", unsafe_allow_html=True)

    st.write("### 📈 Visual Progress Chart")
    chart_data = pd.DataFrame({"XP": [10, 40, 25, 60, st.session_state.xp % 100]})
    st.area_chart(chart_data, color=st.session_state.theme)

elif page == "🚀 MCQ Slides":
    st.markdown("<h1>🎓 ACADEMY SLIDES</h1>", unsafe_allow_html=True)
    
    # Slide Logic
    q_idx = st.session_state.q_index % len(MCQ_DATA)
    q = MCQ_DATA[q_idx]
    
    st.markdown(f"<div class='metric-card'><h2 style='color:white;'>{q['q']}</h2></div>", unsafe_allow_html=True)
    
    # Multi-Column MCQ
    ans = st.radio("Choose carefully:", q['o'], key=f"slide_{st.session_state.q_index}")
    
    col_sub, col_next = st.columns(2)
    with col_sub:
        if st.button("Submit Answer ✅"):
            if ans == q['a']:
                st.session_state.xp += 20
                st.balloons()
                st.success("Correct! +20 XP")
                time.sleep(1)
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.error("Wrong! Try again.")
    with col_next:
        if st.button("Skip Slide ⏭️"):
            st.session_state.q_index += 1
            st.rerun()

elif page == "⚔️ Boss Battle":
    st.markdown("<h1 style='color:red;'>⚔️ BOSS BATTLE</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.write(f"🦸 Player: {st.session_state.player_hp}%"); st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.player_hp}%; background:#2ecc71;'></div></div>", unsafe_allow_html=True)
    with c2: st.write(f"👹 Boss: {st.session_state.boss_hp}%"); st.markdown(f"<div class='hp-bar'><div class='hp-fill' style='width:{st.session_state.boss_hp}%; background:#e74c3c;'></div></div>", unsafe_allow_html=True)
    
    if st.session_state.boss_hp <= 0:
        st.success("BOSS DEFEATED! 🎊"); st.session_state.xp += 100
        if st.button("Spawn New Boss"): st.session_state.boss_hp = 100; st.rerun()
    else:
        q = random.choice(MCQ_DATA)
        st.write(f"### CHALLENGE: {q['q']}")
        atk = st.selectbox("Select Attack Power:", q['o'])
        if st.button("💥 STRIKE"):
            if atk == q['a']:
                st.session_state.boss_hp -= 25
                st.session_state.battle_log = "CRITICAL HIT! -25 HP to Boss"
            else:
                st.session_state.player_hp -= 20
                st.session_state.battle_log = "BOSS COUNTERED! -20 HP to You"
            st.rerun()
    st.info(st.session_state.battle_log)

elif page == "🗂️ Word Vault":
    st.title("🗂️ WORD VAULT")
    col1, col2 = st.columns(2)
    with col1: w = st.text_input("New Word")
    with col2: m = st.text_input("Meaning")
    if st.button("💾 Lock in Vault"):
        if w and m: st.session_state.vault.append(f"{w} : {m}"); st.rerun()
    
    for item in reversed(st.session_state.vault):
        st.markdown(f"<div class='metric-card'>{item}</div>", unsafe_allow_html=True)
