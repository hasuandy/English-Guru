import streamlit as st
import datetime
import time

# --- 1. INITIALIZATION ---
if 'xp' not in st.session_state: st.session_state.xp = 0
if 'vault' not in st.session_state: st.session_state.vault = []
if 'streak' not in st.session_state: st.session_state.streak = 1

# --- 2. THEME (Deep Black & Neon) ---
st.set_page_config(page_title="English Guru Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .card { 
        background-color: #0a0a0a; border: 2px solid #00ffcc; 
        padding: 20px; border-radius: 15px; margin-bottom: 15px; 
    }
    .neon-text { color: #00ffcc; font-weight: bold; font-size: 20px; }
    .stButton>button { background: #00ffcc !important; color: black !important; font-weight: bold; border-radius: 10px; }
    input { background-color: #1a1a1a !important; color: white !important; border: 1px solid #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CORE SRS FUNCTION ---
def add_to_vault(word, meaning):
    # Review set to Today for testing (taaki turant option dikhe)
    review_date = datetime.date.today()
    st.session_state.vault.append({
        "word": word, 
        "meaning": meaning, 
        "review_date": review_date,
        "mastery": 0
    })

# --- 4. UI HEADER ---
st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🛡️ ENGLISH GURU PRO</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
col1.metric("🏆 TOTAL XP", st.session_state.xp)
col2.metric("🔥 STREAK", f"{st.session_state.streak} Days")

tabs = st.tabs(["🏠 Dashboard", "📝 Practice (SRS)", "📚 Word Vault"])

# --- TAB: DASHBOARD ---
with tabs[0]:
    st.subheader("Your Progress")
    st.markdown(f"<div class='card'>Words in Vault: {len(st.session_state.vault)}</div>", unsafe_allow_html=True)
    st.progress(min(st.session_state.xp / 1000, 1.0))

# --- TAB: PRACTICE (SRS logic yahan dikhega) ---
with tabs[1]:
    st.subheader("🧠 Smart Review Challenges")
    
    # Sirf wahi words jo aaj review karne hain
    today = datetime.date.today()
    due_words = [w for w in st.session_state.vault if w['review_date'] <= today]
    
    if not due_words:
        st.info("Abhi koi word review ke liye nahi hai. Pehle Vault mein word add karein!")
    else:
        word_data = due_words[0] # Pehla word uthao test ke liye
        st.markdown(f"<div class='card'>Aapne ye word save kiya tha: <span class='neon-text'>{word_data['word']}</span></div>", unsafe_allow_html=True)
        
        user_input = st.text_input("Iska matlab (meaning) kya hai?", key="quiz_input")
        
        if st.button("Check Answer ✅"):
            if user_input.lower() in word_data['meaning'].lower():
                st.session_state.xp += 30
                # SRS: Agla review 3 din baad
                word_data['review_date'] = today + datetime.timedelta(days=3)
                st.success("Sahi Jawab! +30 XP. Ye word ab 3 din baad dikhega.")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Galat! Sahi matlab hai: {word_data['meaning']}")

# --- TAB: WORD VAULT (Add Words Here) ---
with tabs[2]:
    st.subheader("Add Knowledge to Vault")
    with st.form("add_form"):
        w = st.text_input("New English Word")
        m = st.text_input("Hindi Meaning / Context")
        if st.form_submit_button("Lock into Vault 🔒"):
            if w and m:
                add_to_vault(w, m)
                st.success(f"'{w}' save ho gaya! Practice tab mein check karein.")
                st.rerun()
    
    st.write("---")
    st.subheader("Your Collection")
    for item in reversed(st.session_state.vault):
        st.markdown(f"""
            <div class='card'>
                <span class='neon-text'>{item['word']}</span> : {item['meaning']}<br>
                <small>Next Review: {item['review_date']}</small>
            </div>
        """, unsafe_allow_html=True)
