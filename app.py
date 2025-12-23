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

# Multiplayer Simulated Feed
if 'global_feed' not in st.session_state:
    st.session_state.global_feed = [
        "🛡️ ShadowHunter dealt 120 DMG to Boss!",
        "💎 CyberGamer reached Level 5!",
        "⚔️ DragonSlayer joined the Arena!"
    ]

# --- 2. DAILY LOGIN LOGIC ---
today = str(date.today())
if st.session_state.last_login != today:
    # Bonus logic
    st.session_state.streak += 1
    bonus_xp = st.session_state.streak * 50
    st.session_state.xp += bonus_xp
    st.session_state.last_login = today
    st.toast(f"🎁 Daily Bonus: +{bonus_xp} XP! Streak: {st.session_state.streak} Days")

# --- 3. RANK CALCULATOR ---
def get_rank(xp):
    if xp < 200: return "🟢 TRAINEE", "#00ff00"
    elif xp < 500: return "🔵 ELITE WARRIOR", "#00f2ff"
    elif xp < 1000: return "🟣 SHADOW KNIGHT", "#8800ff"
    else: return "👑 IMMORTAL LEGEND", "#ffd700"

rank_name, rank_color = get_rank(st.session_state.xp)

# --- 4. UI STYLING ---
st.set_page_config(page_title="English Guru V36", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #050505; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }}
    .brand-title {{
        font-family: 'Bungee'; font-size: 3.5rem; text-align: center;
        background: linear-gradient(90deg, #ff0055, {rank_color});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .reward-card {{
        background: linear-gradient(45deg, rgba(255,0,85,0.1), rgba(0,242,255,0.1));
        border: 2px solid {rank_color}; border-radius: 15px; padding: 20px; text-align: center;
    }}
    .feed-item {{ border-left: 3px solid {rank_color}; padding-left: 10px; margin-bottom: 5px; color: #00f2ff; font-size: 0.85rem; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{rank_color}; font-family:Bungee;'>{st.session_state.player_name}</h2>", unsafe_allow_html=True)
    page = st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Boss Arena", "🏆 Leaderboard", "📚 Word Vault"])
    st.write("---")
    st.markdown(f"🔥 **Streak:** {st.session_state.streak} Days")
    if st.button("RESET DATA"):
        st.session_state.clear()
        st.rerun()

st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# --- 6. PAGE CONTENT ---

if page == "🏰 Home Base":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"<div class='reward-card'><h2>Welcome back, {st.session_state.player_name}!</h2><p>Current Rank: {rank_name}</p></div>", unsafe_allow_html=True)
        st.write("### 📈 Your XP Journey")
        st.area_chart({"XP": [10, 50, 30, 80, st.session_state.xp]})
    
    with c2:
        st.write("### 🌐 Global Feed")
        for msg in st.session_state.global_feed[-8:]:
            st.markdown(f"<div class='feed-item'>{msg}</div>", unsafe_allow_html=True)

elif page == "👹 Boss Arena":
    st.write(f"### 👹 World Boss: GRAMMAR TITAN")
    st.progress(st.session_state.boss_hp / 500)
    
    q = "Battle Task: Choose the correct preposition - 'She is interested ____ music.'"
    ans = st.radio(q, ["at", "in", "on"])
    
    if st.button("💥 CO-OP STRIKE"):
        if ans == "in":
            dmg = random.randint(120, 220)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.xp += 60
            st.session_state.global_feed.append(f"⚔️ {st.session_state.player_name} hit for {dmg} DMG!")
            st.success(f"CRITICAL! {dmg} DMG dealt!")
            if st.session_state.boss_hp <= 0:
                st.balloons(); st.session_state.boss_hp = 500
        else:
            st.error("MISS! The Titan counter-attacks!")
        time.sleep(1); st.rerun()

elif page == "🏆 Leaderboard":
    st.write("### 🏆 Global Hall of Fame")
    # Simulated multiplayer ranks
    players = [
        {"n": "ShadowHunter", "x": 3200, "s": "Online 🟢"},
        {"n": st.session_state.player_name, "x": st.session_state.xp, "s": "You 🛡️"},
        {"n": "CyberGamer", "x": 800, "s": "Online 🟢"},
        {"n": "NoobMaster", "x": 150, "s": "Offline 🔴"}
    ]
    for p in sorted(players, key=lambda x: x['x'], reverse=True):
        st.markdown(f"**{p['n']}** — {p['x']} XP | `{p['s']}`")

elif page == "📚 Word Vault":
    st.write("### 📖 Word Vault")
    w = st.text_input("Word")
    m = st.text_input("Meaning")
    if st.button("Save"):
        st.session_state.vault.append({"w": w, "m": m})
        st.success("Knowledge Stored!")
    for item in st.session_state.vault:
        st.info(f"**{item['w']}**: {item['m']}")
