import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# --- 2. QUESTIONS DATA ---
questions = [
    {"q": "He ____ to the market yesterday.", "a": ["go", "goes", "went"], "c": "went"},
    {"q": "This is ____ apple.", "a": ["a", "an", "the"], "c": "an"},
    {"q": "Dogs ____ barking loudly.", "a": ["is", "am", "are"], "c": "are"},
    {"q": "Opposite of 'Hot' is:", "a": ["Ice", "Cold", "Warm"], "c": "Cold"}
]

# --- 3. CLEAN UI STYLING ---
st.set_page_config(page_title="English Guru", layout="wide")

st.markdown("""
    <style>
    /* Modern Light Theme */
    .stApp { background-color: #F0F2F6; color: #1E1E2F; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #6c5ce7; }
    [data-testid="stSidebar"] * { color: white !important; }

    /* Custom Card Style */
    .word-card {
        background: white; padding: 15px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px;
        border-left: 5px solid #6c5ce7;
    }
    
    .stButton>button {
        background: #6c5ce7 !important; color: white !important;
        border-radius: 8px !important; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR MENU ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3426/3426653.png", width=80)
    st.title("GURU MENU")
    page = st.selectbox("GO TO:", ["🏠 Dashboard", "⚔️ Battle Arena", "📚 My Word Vault", "🏅 Badges"])
    st.write("---")
    st.metric("Your XP", st.session_state.xp)
    st.metric("Boss HP", st.session_state.boss_hp)

# --- 5. PAGES ---

if page == "🏠 Dashboard":
    st.title("Welcome back, Warrior! 🏆")
    st.write("Aapne ab tak **{}** words seekhe hain.".format(len(st.session_state.vault)))
    st.info("Battle Arena mein jao aur Boss ko hara kar XP kamao!")
    
    # Quick Stats
    c1, c2 = st.columns(2)
    with c1: st.success(f"Current Rank: {'Expert' if st.session_state.xp > 200 else 'Beginner'}")
    with c2: st.warning(f"Words in Vault: {len(st.session_state.vault)}")

elif page == "⚔️ Battle Arena":
    st.title("👹 Fight the Grammar Boss")
    st.progress(st.session_state.boss_hp / 500)
    
    q = questions[st.session_state.q_idx % len(questions)]
    st.markdown(f"### Q: {q['q']}")
    ans = st.radio("Choose correct answer:", q['a'], key=f"q_{st.session_state.q_idx}")
    
    if st.button("🔥 RELEASE ATTACK"):
        if ans == q['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.success("Correct! Boss took 100 DMG!")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error("Oops! Wrong grammar. Correct: " + q['c'])
        
        st.session_state.q_idx += 1
        time.sleep(1)
        st.rerun()

elif page == "📚 My Word Vault":
    st.title("📖 Your Personal Dictionary")
    
    # Word Input
    with st.container():
        c1, c2 = st.columns(2)
        new_w = c1.text_input("New Word")
        new_m = c2.text_input("Meaning")
        if st.button("Save to Vault"):
            if new_w and new_m:
                st.session_state.vault.append({"w": new_w, "m": new_m})
                st.success("Word Saved!")
                st.rerun()

    st.write("---")
    st.subheader("Your Saved Knowledge:")
    
    # YAHAN AB WORDS DIKHENGE SAHI SE
    if not st.session_state.vault:
        st.write("Vault khali hai. Kuch naya add karo!")
    else:
        # Table format for better visibility
        for item in reversed(st.session_state.vault):
            st.markdown(f"""
                <div class='word-card'>
                    <b style='color:#6c5ce7; font-size:1.2rem;'>{item['w']}</b> : {item['m']}
                </div>
            """, unsafe_allow_html=True)

elif page == "🏅 Badges":
    st.title("🏅 Achievements")
    if len(st.session_state.vault) >= 1:
        st.success("📖 Scholar: You saved your first word!")
    if st.session_state.xp >= 200:
        st.success("⚔️ Warrior: You crossed 200 XP!")
    if not st.session_state.vault and st.session_state.xp < 200:
        st.write("Abhi koi badge nahi mila. Kaam shuru karo!")
