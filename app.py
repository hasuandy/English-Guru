import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION ---
if 'achievements' not in st.session_state or isinstance(st.session_state.achievements, list):
    st.session_state.achievements = set()
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 500
if 'vault' not in st.session_state: st.session_state.vault = []
if 'q_index' not in st.session_state: st.session_state.q_index = 0

# --- 2. MEGA QUESTION BANK (Expanded) ---
questions = [
    {"q": "He ____ a doctor.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "They ____ to the park yesterday.", "a": ["go", "went", "going"], "c": "went"},
    {"q": "She ____ like apples.", "a": ["don't", "doesn't", "isn't"], "c": "doesn't"},
    {"q": "Neither of us ____ ready.", "a": ["is", "are", "am"], "c": "is"},
    {"q": "I have ____ my lunch.", "a": ["eat", "ate", "eaten"], "c": "eaten"},
    {"q": "Choose the correct spelling:", "a": ["Recieve", "Receive", "Receve"], "c": "Receive"},
    {"q": "The sun ____ in the east.", "a": ["rise", "rises", "rising"], "c": "rises"},
    {"q": "I ____ English since 2010.", "a": ["learn", "am learning", "have been learning"], "c": "have been learning"},
    {"q": "She is the ____ girl in class.", "a": ["smart", "smarter", "smartest"], "c": "smartest"},
    {"q": "If it rains, I ____ at home.", "a": ["stay", "will stay", "stayed"], "c": "will stay"},
    {"q": "____ you like some tea?", "a": ["Will", "Would", "Shall"], "c": "Would"},
    {"q": "I'm busy ____ the moment.", "a": ["at", "on", "in"], "c": "at"},
    {"q": "The cat is hiding ____ the bed.", "a": ["under", "between", "through"], "c": "under"},
    {"q": "We ____ go to the party tonight.", "a": ["might", "must to", "can to"], "c": "might"},
    {"q": "He speaks English ____.", "a": ["good", "well", "best"], "c": "well"},
    {"q": "I haven't seen him ____ a long time.", "a": ["since", "for", "from"], "c": "for"},
    {"q": "Look! The baby ____.", "a": ["sleeps", "is sleeping", "sleep"], "c": "is sleeping"},
    {"q": "This book is ____ than that one.", "a": ["gooder", "better", "best"], "c": "better"},
    {"q": "I ____ a new car last week.", "a": ["buy", "bought", "buys"], "c": "bought"},
    {"q": "He is afraid ____ spiders.", "a": ["of", "from", "with"], "c": "of"},
    {"q": "We ____ dinner when the phone rang.", "a": ["have", "had", "were having"], "c": "were having"},
    {"q": "____ you ever been to Paris?", "a": ["Do", "Has", "Have"], "c": "Have"},
    {"q": "She ____ French fluently.", "a": ["speak", "speaks", "speaking"], "c": "speaks"},
    {"q": "I'm looking forward ____ meeting you.", "a": ["to", "for", "at"], "c": "to"},
    {"q": "Would you mind ____ the door?", "a": ["close", "closing", "to close"], "c": "closing"},
    {"q": "He's ____ engineer.", "a": ["a", "an", "the"], "c": "an"},
    {"q": "The movie was ____ boring.", "a": ["very", "too much", "enough"], "c": "very"},
    {"q": "I'll call you as soon as I ____.", "a": ["arrive", "will arrive", "arrived"], "c": "arrive"},
    {"q": "____ is your favorite color?", "a": ["What", "Which", "Who"], "c": "What"},
    {"q": "The children ____ in the garden now.", "a": ["play", "are playing", "plays"], "c": "are playing"}
]

# Randomize questions if not already shuffled
if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))

# --- 3. ACHIEVEMENT SYNC ---
def sync_badges():
    if not isinstance(st.session_state.achievements, set):
        st.session_state.achievements = set()
    if len(st.session_state.vault) >= 1: st.session_state.achievements.add("📖 Scholar")
    if st.session_state.xp >= 200: st.session_state.achievements.add("⚔️ Warrior")
    if st.session_state.xp >= 500: st.session_state.achievements.add("👑 Master")

sync_badges()

# --- 4. UI STYLING ---
st.set_page_config(page_title="English Guru V41", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap');
    .stApp { background: #050505; color: #00f2ff; }
    .main-title { font-family: 'Bungee'; font-size: 3rem; text-align: center; color: #ff0055; text-shadow: 0 0 15px #ff0055; }
    .badge-card { background: rgba(255, 215, 0, 0.2); border: 2px solid #ffd700; border-radius: 10px; padding: 10px; margin-bottom: 5px; text-align: center; font-family: 'Bungee'; color: gold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-family:Bungee; color:#ff0055;'>PLAYER PROFILE</h2>", unsafe_allow_html=True)
    st.metric("Total XP", st.session_state.xp)
    st.write("---")
    st.markdown("### 🏅 ACHIEVEMENTS")
    for a in st.session_state.achievements:
        st.markdown(f"<div class='badge-card'>{a}</div>", unsafe_allow_html=True)
    if st.button("🔴 Reset Game"):
        st.session_state.clear()
        st.rerun()

# --- 6. MAIN TABS ---
st.markdown("<h1 class='main-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🏰 HOME", "👹 BATTLE", "📚 VAULT"])

with tab2:
    st.write(f"### 👹 BOSS HP: {st.session_state.boss_hp} / 500")
    st.progress(max(st.session_state.boss_hp / 500, 0.0))
    
    # Get current question
    q_idx = st.session_state.q_index % len(st.session_state.shuffled_questions)
    curr_q = st.session_state.shuffled_questions[q_idx]
    
    st.subheader(f"Question {st.session_state.q_index + 1}:")
    st.write(f"### {curr_q['q']}")
    ans = st.radio("Choose the correct option:", curr_q['a'], key=f"q_{st.session_state.q_index}")
    
    if st.button("💥 ATTACK"):
        if ans == curr_q['c']:
            st.session_state.xp += 50
            st.session_state.boss_hp -= 100
            st.success("✅ CORRECT! -100 Boss HP | +50 XP")
            if st.session_state.boss_hp <= 0:
                st.balloons()
                st.session_state.boss_hp = 500
        else:
            st.error(f"❌ WRONG! The correct answer was: {curr_q['c']}")
        
        st.session_state.q_index += 1
        sync_badges()
        time.sleep(1)
        st.rerun()

with tab3:
    st.header("Word Vault")
    w = st.text_input("New Word")
    m = st.text_input("Meaning")
    if st.button("🔒 SAVE"):
        if w and m:
            st.session_state.vault.append({"w": w, "m": m})
            sync_badges()
            st.success("Word added to Vault!")
            st.rerun()

with tab1:
    st.header("Dashboard")
    st.write(f"Total XP: {st.session_state.xp}")
    st.write(f"Words in Vault: {len(st.session_state.vault)}")
    st.area_chart({"Progress": [0, 20, 50, 10, st.session_state.xp]})
