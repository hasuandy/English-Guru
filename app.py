import streamlit as st
import random
import time

# --- 1. SESSION STATE (The Brain) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'quest_done' not in st.session_state: st.session_state.quest_done = False

# --- 2. RANK CALCULATOR ---
def get_rank(xp):
    if xp < 200: return "🟢 TRAINEE", "#00ff00"
    elif xp < 500: return "🔵 ELITE WARRIOR", "#00f2ff"
    elif xp < 1000: return "🟣 SHADOW KNIGHT", "#8800ff"
    else: return "👑 IMMORTAL LEGEND", "#ffd700"

rank_name, rank_color = get_rank(st.session_state.xp)

# --- 3. RPG UI STYLING ---
st.set_page_config(page_title="English Guru V34", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #050505; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }}
    .brand-title {{
        font-family: 'Bungee'; font-size: 3.5rem; text-align: center;
        background: linear-gradient(90deg, #ff0055, {rank_color});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: -50px;
    }}
    .stat-box {{
        background: rgba(255, 255, 255, 0.03); border: 1px solid {rank_color};
        border-radius: 15px; padding: 20px; text-align: center;
    }}
    .badge {{
        padding: 5px 15px; border-radius: 50px; background: {rank_color};
        color: black; font-weight: bold; font-family: 'Bungee'; font-size: 1.2rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{rank_color}; font-family:Bungee;'>RANK: {rank_name.split(' ')[1]}</h2>", unsafe_allow_html=True)
    page = st.selectbox("SELECT MISSION", ["🏰 Home Base", "👹 Boss Arena", "📚 Word Vault", "🎯 Daily Quests"])
    st.write("---")
    if st.button("RESET PROGRESS"):
        st.session_state.clear()
        st.rerun()

st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# --- 5. PAGE CONTENT ---

if page == "🏰 Home Base":
    st.markdown(f"<div style='text-align:center;'><span class='badge'>{rank_name}</span></div><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='stat-box'><h3>🏆 TOTAL XP</h3><h1>{st.session_state.xp}</h1></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='stat-box'><h3>❤️ HP</h3><h1>{st.session_state.hp}%</h1></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='stat-box'><h3>🔥 NEXT RANK</h3><p>{max(0, 200 - st.session_state.xp if st.session_state.xp < 200 else 500 - st.session_state.xp)} XP to go</p></div>", unsafe_allow_html=True)
    
    st.write("### 📊 Power Chart")
    st.area_chart({"Power": [0, 50, 20, 100, st.session_state.xp]})

elif page == "👹 Boss Arena":
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### 👹 TITAN HP: {st.session_state.boss_hp}")
        st.progress(st.session_state.boss_hp / 500)
    with col2:
        st.write(f"### 🛡️ YOUR HP: {st.session_state.hp}")
        st.progress(st.session_state.hp / 100)

    st.write("---")
    q = "Battle Task: 'I ____ (have/has) already finished my work.'"
    ans = st.radio(q, ["have", "has"])
    
    if st.button("💥 LAUNCH STRIKE"):
        if ans == "have":
            dmg = random.randint(100, 250)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.xp += 40
            st.success(f"CRITICAL HIT! {dmg} Damage dealt!")
            if st.session_state.boss_hp <= 0:
                st.balloons(); st.session_state.boss_hp = 500
        else:
            st.session_state.hp = max(0, st.session_state.hp - 20)
            st.error("MISS! You took 20 damage.")
        time.sleep(1); st.rerun()

elif page == "🎯 Daily Quests":
    st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
    st.write("### 📜 ACTIVE MISSIONS")
    q1 = f"1. Save 1 Word in Vault ({len(st.session_state.vault)}/1)"
    st.write(q1)
    if len(st.session_state.vault) >= 1 and not st.session_state.quest_done:
        if st.button("CLAIM QUEST REWARD"):
            st.session_state.xp += 100
            st.session_state.quest_done = True
            st.success("+100 XP Claimed!"); time.sleep(1); st.rerun()
    elif st.session_state.quest_done:
        st.write("✅ **QUEST COMPLETED**")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📚 Word Vault":
    word = st.text_input("New Intel")
    mean = st.text_input("Meaning")
    if st.button("LOCK IN VAULT"):
        if word and mean:
            st.session_state.vault.append({"word": word, "mean": mean})
            st.success("Intel Secured!")
    
    for item in st.session_state.vault:
        st.info(f"**{item['word']}**: {item['mean']}")
