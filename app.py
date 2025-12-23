import streamlit as st
import random
import time

# --- 1. SESSION STATE (The Brain) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'hp' not in st.session_state: st.session_state.hp = 100
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'player_name' not in st.session_state: st.session_state.player_name = "Warrior"

# Dummy Data for Multiplayer Feel
if 'global_feed' not in st.session_state:
    st.session_state.global_feed = [
        "🛡️ ShadowHunter dealt 120 DMG to Boss!",
        "💎 CyberGamer reached Level 5!",
        "⚔️ DragonSlayer joined the Arena!"
    ]

# --- 2. RANK CALCULATOR ---
def get_rank(xp):
    if xp < 200: return "🟢 TRAINEE", "#00ff00"
    elif xp < 500: return "🔵 ELITE WARRIOR", "#00f2ff"
    elif xp < 1000: return "🟣 SHADOW KNIGHT", "#8800ff"
    else: return "👑 IMMORTAL LEGEND", "#ffd700"

rank_name, rank_color = get_rank(st.session_state.xp)

# --- 3. UI STYLING ---
st.set_page_config(page_title="English Guru V35 - Multiplayer", layout="wide")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp {{ background: #050505; color: #e0e0e0; font-family: 'Rajdhani', sans-serif; }}
    .brand-title {{
        font-family: 'Bungee'; font-size: 3.5rem; text-align: center;
        background: linear-gradient(90deg, #ff0055, {rank_color});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .multiplayer-box {{
        background: rgba(0, 242, 255, 0.05); border: 1px solid #00f2ff;
        border-radius: 10px; padding: 15px; margin-top: 10px;
    }}
    .feed-text {{ color: #00f2ff; font-size: 0.9rem; font-family: 'Courier New'; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
with st.sidebar:
    st.markdown(f"<h2 style='color:{rank_color}; font-family:Bungee;'>{st.session_state.player_name}</h2>", unsafe_allow_html=True)
    page = st.selectbox("MISSION SELECT", ["🏰 Home Base", "👹 Boss Arena", "🏆 Leaderboard", "📚 Word Vault"])
    
    # Custom Name Feature
    new_name = st.text_input("Change Hero Name", st.session_state.player_name)
    if st.button("Update ID"):
        st.session_state.player_name = new_name
        st.rerun()

st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

# --- 5. PAGE CONTENT ---

if page == "🏰 Home Base":
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.markdown(f"### Welcome, {st.session_state.player_name}!")
        st.write(f"Your Current Rank: **{rank_name}**")
        st.area_chart({"Your Power": [10, 30, 25, 60, st.session_state.xp]})
    
    with c2:
        st.write("### 🌐 Live Arena Feed")
        for msg in st.session_state.global_feed[-5:]:
            st.markdown(f"<p class='feed-text'>{msg}</p>", unsafe_allow_html=True)

elif page == "👹 Boss Arena":
    st.write(f"### 👹 World Boss: GRAMMAR TITAN")
    st.progress(st.session_state.boss_hp / 500)
    
    q = "Battle Question: 'Which one is a collective noun?'"
    ans = st.radio(q, ["Table", "Team", "Tall"])
    
    if st.button("💥 CO-OP ATTACK"):
        if ans == "Team":
            dmg = random.randint(100, 200)
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - dmg)
            st.session_state.xp += 50
            st.session_state.global_feed.append(f"⚔️ {st.session_state.player_name} dealt {dmg} DMG!")
            st.success(f"BOOM! You dealt {dmg} damage!")
            if st.session_state.boss_hp <= 0:
                st.balloons(); st.session_state.boss_hp = 500
        else:
            st.error("MISS! Boss hit you back!")
        time.sleep(1); st.rerun()

elif page == "🏆 Leaderboard":
    st.markdown("### 🏆 Top Warriors (Global)")
    # Multiplayer Structure (Simulated)
    leaderboard_data = [
        {"Rank": 1, "Name": "ShadowHunter", "XP": 2500, "Status": "Online 🟢"},
        {"Rank": 2, "Name": st.session_state.player_name, "XP": st.session_state.xp, "Status": "You 🛡️"},
        {"Rank": 3, "Name": "CyberGamer", "XP": 450, "Status": "Away 🟡"},
        {"Rank": 4, "Name": "NoobMaster", "XP": 120, "Status": "Offline 🔴"}
    ]
    
    for player in leaderboard_data:
        color = "#00f2ff" if player["Name"] == st.session_state.player_name else "#ffffff"
        st.markdown(f"<div style='padding:10px; border-bottom:1px solid #333; color:{color}'>"
                    f"#{player['Rank']} | {player['Name']} — {player['XP']} XP ({player['Status']})</div>", 
                    unsafe_allow_html=True)

elif page == "📚 Word Vault":
    # (Same vault code as before)
    word = st.text_input("New Word")
    mean = st.text_input("Meaning")
    if st.button("Save Word"):
        st.session_state.vault.append({"word": word, "mean": mean})
        st.toast("Saved to Vault!")
    for item in st.session_state.vault:
        st.info(f"**{item['word']}**: {item['mean']}")
