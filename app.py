import streamlit as st
import random
import time
from datetime import date

# --- 1. SESSION STATE (The Brain) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'player_name' not in st.session_state: st.session_state.player_name = "Warrior"
if 'last_login' not in st.session_state: st.session_state.last_login = None
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'achievements' not in st.session_state: st.session_state.achievements = []

# --- 2. ACHIEVEMENT LOGIC ---
def check_achievements():
    new_badge = False
    # 1. First Word Badge
    if len(st.session_state.vault) >= 1 and "📖 Scholar" not in st.session_state.achievements:
        st.session_state.achievements.append("📖 Scholar")
        new_badge = True
    # 2. XP Milestone
    if st.session_state.xp >= 500 and "⚔️ Veteran" not in st.session_state.achievements:
        st.session_state.achievements.append("⚔️ Veteran")
        new_badge = True
    # 3. Boss Slayer (Hypothetical)
    if st.session_state.xp >= 1000 and "👑 Titan Slayer" not in st.session_state.achievements:
        st.session_state.achievements.append("👑 Titan Slayer")
        new_badge = True
    
    if new_badge:
        st.toast("🌟 NEW ACHIEVEMENT UNLOCKED!")

check_achievements()

# --- 3. RANK CALCULATOR ---
def get_rank(xp):
    if xp < 200: return "🟢 TRAINEE", "#00ff00"
    elif xp < 500: return "🔵 ELITE WARRIOR", "#00f2ff"
    elif xp < 1000: return "🟣 SHADOW KNIGHT", "#8800ff"
    else: return "👑 IMMORTAL LEGEND", "#ffd700"

rank_name, rank_color = get_rank(st.session_state.xp)

# --- 4. UI STYLING ---
st.set_page_config(page_title="English Guru V37", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #050505; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }}
    .brand-title {{
        font-family: 'Bungee'; font-size: 3.5rem; text-align: center;
        background: linear-gradient(90deg, #ff0055, {rank_color});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .achievement-card {{
        background: rgba(255, 215, 0, 0.1); border: 1px solid #ffd700;
        border-radius: 10px; padding: 10px; display: inline-block; margin: 5px;
    }}
    .stat-card {{
        background: rgba(255, 255, 255, 0.05); border-left: 5px solid {rank_color};
        padding: 20px; border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{rank_color}; font-family:Bungee;'>{st.session_state.player_name}</h2>", unsafe_allow_html=True)
    page = st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Boss Arena", "🏆 Leaderboard", "📚 Word Vault"])
    st.write("---")
    st.write("### 🏅 Achievements")
    for badge in st.session_state.achievements:
        st.markdown(f"<div class='achievement-card'>{badge}</div>", unsafe_allow_html=True)

st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# --- 6. PAGE CONTENT ---

if page == "🏰 Home Base":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"<div class='stat-card'><h2>Rank: {rank_name}</h2><h3>Total XP: {st.session_state.xp}</h3></div>", unsafe_allow_html=True)
        st.write("### 📊 Power Evolution")
        st.line_chart({"Level": [5, 15, 10, 25, st.session_state.xp]})
    
    with c2:
        st.write("### 🏆 UNLOCKED BADGES")
        if not st.session_state.achievements:
            st.write("No badges yet. Start training!")
        for badge in st.session_state.achievements:
            st.success(badge)

elif page == "👹 Boss Arena":
    st.write("### 👹 BOSS FIGHT")
    st.progress(st.session_state.boss_hp / 500)
    
    q = "Select the correct sentence: 'Each of the students ____ (has/have) a book.'"
    ans = st.radio(q, ["has", "have"])
    
    if st.button("💥 STRIKE"):
        if ans == "has":
            dmg = random.randint(150, 250)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.xp += 70
            st.success(f"CRITICAL HIT! {dmg} Damage!")
            if st.session_state.boss_hp <= 0:
                st.balloons(); st.session_state.boss_hp = 500
        else:
            st.error("MISS! The Titan struck back.")
        time.sleep(1); st.rerun()

elif page == "📚 Word Vault":
    w = st.text_input("New Word")
    m = st.text_input("Meaning")
    if st.button("Save to Vault"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            st.success("Knowledge Saved!")
            st.rerun()

    st.write("---")
    for item in st.session_state.vault:
        st.info(f"**{item['w']}**: {item['m']}")
