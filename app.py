import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'achievements' not in st.session_state: st.session_state.achievements = []

# --- 2. ACHIEVEMENT ENGINE (Fix for "Open nahi ho raha") ---
def update_achievements():
    # Scholar Badge: Jab 1 word save ho jaye
    if len(st.session_state.vault) >= 1 and "📖 Scholar" not in st.session_state.achievements:
        st.session_state.achievements.append("📖 Scholar")
        st.toast("🌟 NEW ACHIEVEMENT: Scholar unlocked!")
        
    # Warrior Badge: Jab 200 XP cross ho jaye
    if st.session_state.xp >= 200 and "⚔️ Warrior" not in st.session_state.achievements:
        st.session_state.achievements.append("⚔️ Warrior")
        st.toast("🌟 NEW ACHIEVEMENT: Warrior unlocked!")

    # Master Badge: Jab 500 XP cross ho jaye
    if st.session_state.xp >= 500 and "👑 Master" not in st.session_state.achievements:
        st.session_state.achievements.append("👑 Master")
        st.toast("🌟 NEW ACHIEVEMENT: Master unlocked!")

# --- 3. DYNAMIC UI & THEME ---
st.set_page_config(page_title="English Guru Pro", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Rajdhani:wght@600&display=swap');
    .stApp { background: #050505; color: #00f2ff; font-family: 'Rajdhani', sans-serif; }
    .main-title { font-family: 'Bungee'; font-size: 3.5rem; text-align: center; color: #ff0055; text-shadow: 0 0 15px #ff0055; }
    .badge-card {
        background: rgba(255, 0, 85, 0.1); border: 2px solid #ff0055;
        border-radius: 10px; padding: 15px; margin-bottom: 10px;
        text-align: center; font-family: 'Bungee'; color: white;
    }
    .cyber-card { background: rgba(255, 255, 255, 0.05); border: 1px solid #333; border-radius: 15px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR (Achievements & Stats) ---
with st.sidebar:
    st.markdown("<h2 style='font-family:Bungee; color:#ff0055;'>WARRIOR PROFILE</h2>", unsafe_allow_html=True)
    st.write(f"🏆 **Total XP:** {st.session_state.xp}")
    st.write(f"📖 **Words Learned:** {len(st.session_state.vault)}")
    st.write("---")
    
    st.markdown("### 🏅 YOUR BADGES")
    if not st.session_state.achievements:
        st.write("No achievements yet. Complete tasks to unlock!")
    else:
        for a in st.session_state.achievements:
            st.markdown(f"<div class='badge-card'>{a}</div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 REFRESH SYSTEM"):
        st.rerun()

# --- 5. MAIN CONTENT ---
st.markdown("<h1 class='main-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏰 DASHBOARD", "👹 BOSS ARENA", "📚 WORD VAULT"])

with tab1:
    st.markdown("<div class='cyber-card'>", unsafe_allow_html=True)
    st.header("Welcome, Hero!")
    st.write("Train hard in the Arena and store knowledge in the Vault to unlock legendary badges.")
    st.area_chart({"Power Level": [0, 50, 20, 100, st.session_state.xp]})
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp} / 500")
    st.progress(st.session_state.boss_hp / 500)
    
    st.markdown("---")
    st.write("### ⚔️ ATTACK STAGE")
    q = "Select the correct sentence for 100 XP:"
    choice = st.radio(q, ["They has a car.", "They have a car.", "They having a car."])
    
    if st.button("💥 FIRE ATTACK"):
        if choice == "They have a car.":
            st.session_state.xp += 100
            st.session_state.boss_hp = max(0, st.session_state.boss_hp - 100)
            st.success("CRITICAL HIT! +100 XP")
            update_achievements() # Force Check
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error("MISS! You took a hit from the Boss.")
        time.sleep(0.5)
        st.rerun()

with tab3:
    st.write("### 📖 Word Vault")
    col_w, col_m = st.columns(2)
    w = col_w.text_input("New Word")
    m = col_m.text_input("Meaning")
    
    if st.button("🔒 SAVE TO VAULT"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            update_achievements() # Force Check
            st.success(f"'{w}' saved! Check your badges.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.warning("Please enter both word and meaning.")

    st.write("---")
    for item in st.session_state.vault:
        st.info(f"**{item['w']}**: {item['m']}")
