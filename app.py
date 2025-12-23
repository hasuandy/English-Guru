import streamlit as st
import random
import time

# --- 1. SESSION INITIALIZATION (Error Fix) ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []

# --- 2. THE 200+ QUESTION BANK ---
# Yahan maine questions ki categories banayi hain
questions_bank = [
    # Grammar (Tenses)
    {"q": "I ____ to the gym every day.", "options": ["go", "goes", "going", "went"], "a": "go"},
    {"q": "She ____ been studying for 3 hours.", "options": ["has", "have", "is", "was"], "a": "has"},
    {"q": "If I ____ rich, I would travel the world.", "options": ["am", "was", "were", "be"], "a": "were"},
    # Idioms & Phrases
    {"q": "Meaning of 'Piece of cake':", "options": ["Very easy", "Very tasty", "Expensive", "Heavy"], "a": "Very easy"},
    {"q": "Meaning of 'Under the weather':", "options": ["Feeling sick", "Enjoying rain", "Travelling", "Angry"], "a": "Feeling sick"},
    # Advanced Grammar
    {"q": "Neither of the candidates ____ qualified.", "options": ["is", "are", "were", "have"], "a": "is"},
    {"q": "I prefer tea ____ coffee.", "options": ["than", "to", "from", "over"], "a": "to"},
    {"q": "The sun ____ in the east.", "options": ["rise", "rises", "rising", "rose"], "a": "rises"},
    {"q": "Hardly ____ I started when it rained.", "options": ["did", "had", "have", "was"], "a": "had"},
    {"q": "I look forward to ____ you soon.", "options": ["see", "seeing", "saw", "seen"], "a": "seeing"}
]
# Note: Real app mein hum is list ko 200+ tak expand kar sakte hain.

# Error Handling for current question
if 'current_q' not in st.session_state or st.session_state.current_q is None:
    st.session_state.current_q = random.choice(questions_bank)

# --- 3. STYLING (Neon Visuals) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .slide-card { 
        background-color: #0d0d0d; border: 3px solid #6c5ce7; 
        padding: 40px; border-radius: 20px; text-align: center;
        box-shadow: 0 0 25px #6c5ce766; margin-top: 20px;
    }
    .neon-q { color: #00ffcc; font-size: 30px; font-weight: bold; margin-bottom: 25px; }
    .stButton>button { 
        background: linear-gradient(45deg, #6c5ce7, #00ffcc) !important; 
        color: #000 !important; font-weight: 900 !important; font-size: 20px !important;
        height: 60px; border-radius: 15px; border: none !important;
    }
    .stRadio [data-testid="stMarkdownContainer"] { font-size: 22px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION TABS ---
st.markdown("<h1 style='text-align:center; color:#6c5ce7;'>⚡ MASTER ENGLISH HUB</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🚀 START SLIDE QUIZ", "📚 VAULT", "📈 STATS"])

with tab1:
    # --- SLIDE SYSTEM ---
    st.markdown("<div class='slide-card'>", unsafe_allow_html=True)
    
    # Question Display (Safe Access)
    q_data = st.session_state.current_q
    st.markdown(f"<p class='neon-q'>{q_data['q']}</p>", unsafe_allow_html=True)
    
    # MCQ UI
    choice = st.radio("Choose the correct option:", q_data['options'], key=f"quiz_{q_data['q']}")
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer ✅"):
            if choice == q_data['a']:
                st.session_state.xp += 50
                st.success("Correct! +50 XP")
                time.sleep(1)
                st.session_state.current_q = random.choice(questions_bank)
                st.rerun()
            else:
                st.error(f"Wrong! The correct answer is: {q_data['a']}")
                
    with col2:
        if st.button("Skip to Next ⏭️"):
            st.session_state.current_q = random.choice(questions_bank)
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.subheader("Vocabulary Storage")
    # Simple add word form
    with st.form("vault_v65"):
        w = st.text_input("New Word")
        m = st.text_input("Meaning")
        if st.form_submit_button("Add to Vault"):
            if w and m:
                st.session_state.vault.append(f"{w}: {m}")
                st.rerun()
    for item in reversed(st.session_state.vault):
        st.write(f"📖 {item}")

with tab3:
    st.metric("Total Experience (XP)", st.session_state.xp)
    st.bar_chart({"Progress": [20, 50, 80, 100, st.session_state.xp % 500]})

# Sidebar
st.sidebar.title("App Settings")
if st.sidebar.button("Reset All Data"):
    st.session_state.clear()
    st.rerun()
