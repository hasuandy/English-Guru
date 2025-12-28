import streamlit as st
import sqlite3
from datetime import date
import random
import time

# --- DATABASE SETUP ---
DB_NAME = 'english_guru_pro_v37.db'
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS progress (email TEXT, date TEXT, xp INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dictionary (email TEXT, word TEXT, meaning TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_tasks (email TEXT, task_date TEXT, completed INTEGER)''')
    conn.commit()

init_db()

# --- Assets ---
CORRECT_SND = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
WRONG_SND = "https://www.soundjay.com/buttons/sounds/button-10.mp3"
BOSS_GIF = "https://i.pinimg.com/originals/8d/6d/21/8d6d214a1941d4f23b7b396b2d22b512.gif"

# --- BIG QUESTION POOL ---
TRAINING_DATA = [
    {"q": "Antonym of 'ANCIENT'?", "o": ["Old", "Modern", "Heavy", "Small"], "a": "Modern"},
    {"q": "Plural of 'Mouse'?", "o": ["Mouses", "Mice", "Micey", "Mice-s"], "a": "Mice"},
    {"q": "Past tense of 'Go'?", "o": ["Goes", "Gone", "Went", "Going"], "a": "Went"},
    {"q": "Synonym of 'HAPPY'?", "o": ["Sad", "Joyful", "Angry", "Brave"], "a": "Joyful"},
    {"q": "Antonym of 'BRAVE'?", "o": ["Strong", "Cowardly", "Fast", "Quiet"], "a": "Cowardly"},
    {"q": "Past tense of 'Eat'?", "o": ["Eaten", "Eats", "Ate", "Eating"], "a": "Ate"},
    {"q": "Synonym of 'LARGE'?", "o": ["Tiny", "Huge", "Soft", "Hard"], "a": "Huge"},
    {"q": "Plural of 'Child'?", "o": ["Childs", "Childrens", "Children", "Childes"], "a": "Children"},
    {"q": "Synonym of 'FAST'?", "o": ["Slow", "Quick", "Lazy", "Steady"], "a": "Quick"},
    {"q": "Opposite of 'BEAUTIFUL'?", "o": ["Pretty", "Ugly", "Nice", "Clean"], "a": "Ugly"}
]

# --- Functions ---
def trigger_effects(effect_type):
    if effect_type == "correct":
        st.markdown(f'<audio src="{CORRECT_SND}" autoplay></audio>', unsafe_allow_html=True)
    elif effect_type == "wrong":
        st.markdown(f'<audio src="{WRONG_SND}" autoplay></audio>', unsafe_allow_html=True)
        st.markdown("<script>window.parent.document.querySelector('.stApp').animate([{transform:'translate(2px,2px)'},{transform:'translate(-2px,-2px)'}],{duration:100,iterations:3});</script>", unsafe_allow_html=True)

# --- Session & Stats ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in, st.session_state.user, st.session_state.email = True, "Hero_Player", "player@guru.com"
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", (st.session_state.email, st.session_state.user, "123"))
    conn.commit()

if 'boss_hp' not in st.session_state: st.session_state.boss_hp = 100
if 'player_hp' not in st.session_state: st.session_state.player_hp = 100

txp = (c.execute("SELECT SUM(xp) FROM progress WHERE email=?", (st.session_state.email,)).fetchone()[0] or 0)
user_level = 1 + (txp // 100)

# --- UI Layout ---
st.set_page_config(page_title="English Guru Pro v37", page_icon="🎓", layout="wide")
st.markdown("""<style>@import url('https://fonts.googleapis.com/css2?family=Bungee&display=swap'); .stApp { background: #0e1117; color: white; } .hof-card { background: #1e2130; border-radius: 15px; padding: 20px; margin-bottom: 10px; border-left: 5px solid #ffd700; }</style>""", unsafe_allow_html=True)

# --- Navigation ---
page = st.sidebar.radio("MENU", ["🏠 Dashboard", "🎓 Training", "⚔️ Boss Battle", "🏆 Hall of Fame"])

if page == "🏠 Dashboard":
    st.title("🛡️ HERO DASHBOARD")
    st.metric("Level", user_level)
    st.metric("Total XP", txp)

elif page == "🎓 Training":
    st.title("🎓 Practice Area")
    if 't_q' not in st.session_state: st.session_state.t_q = random.choice(TRAINING_DATA)
    q = st.session_state.t_q
    st.subheader(q['q'])
    for opt in q['o']:
        if st.button(opt, key=f"t_{opt}", use_container_width=True):
            if opt == q['a']:
                trigger_effects("correct"); st.success("Sahi Jawab!")
                c.execute("INSERT INTO progress VALUES (?,?,?)", (st.session_state.email, str(date.today()), 10))
                conn.commit()
                time.sleep(1); del st.session_state.t_q; st.rerun()
            else:
                trigger_effects("wrong"); st.error("Galat!")

elif page == "⚔️ Boss Battle":
    st.markdown("<h1 style='color:red; font-family:Bungee; text-align:center;'>👹 BOSS ARENA</h1>", unsafe_allow_html=True)
    boss_max_hp = 100 + (user_level * 25)
    p_safe = max(0.0, min(st.session_state.player_hp / 100.0, 1.0))
    b_safe = max(0.0, min(st.session_state.boss_hp / boss_max_hp, 1.0))
    
    col_hp1, col_hp2 = st.columns(2)
    col_hp1.write(f"🛡️ Hero: {int(p_safe*100)}%"); col_hp1.progress(p_safe)
    col_hp2.write(f"👾 Boss: {int(b_safe*100)}%"); col_hp2.progress(b_safe)

    if st.session_state.boss_hp <= 0:
        st.balloons(); st.success("BOSS DEFEATED!")
        if st.button("Spawn Next Monster"): st.session_state.boss_hp = 100 + ((user_level + 1) * 25); st.session_state.player_hp = 100; st.rerun()
    elif st.session_state.player_hp <= 0:
        st.error("GAME OVER!"); st.button("Revive", on_click=lambda: setattr(st.session_state, 'player_hp', 100))
    else:
        st.image(BOSS_GIF, width=200)
        if 'b_q' not in st.session_state: st.session_state.b_q = random.choice(TRAINING_DATA)
        bq = st.session_state.b_q
        st.subheader(bq['q'])
        ans = st.radio("Choose Attack:", bq['o'], horizontal=True)
        if st.button("🔥 ATTACK"):
            if ans == bq['a']: st.session_state.boss_hp -= 35; trigger_effects("correct")
            else: st.session_state.player_hp -= 20; trigger_effects("wrong")
            del st.session_state.b_q; st.rerun()

elif page == "🏆 Hall of Fame":
    st.markdown("<h1 style='font-family:Bungee; text-align:center;'>🏆 HALL OF FAME 🏆</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>Top legendary English Gurus are honored here!</p>", unsafe_allow_html=True)
    
    # Data fetch from DB
    data = c.execute("SELECT u.username, SUM(p.xp) as total FROM progress p JOIN users u ON p.email = u.email GROUP BY u.email ORDER BY total DESC LIMIT 10").fetchall()
    
    if data:
        for i, row in enumerate(data):
            rank = i + 1
            name = row[0]
            score = row[1]
            
            # Special Rank Icons
            if rank == 1: medal = "🥇"; border = "gold"
            elif rank == 2: medal = "🥈"; border = "silver"
            elif rank == 3: medal = "🥉"; border = "#cd7f32"
            else: medal = f"#{rank}"; border = "#333"
            
            # Avatar generation using name
            avatar_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={name}"
            
            st.markdown(f"""
            <div class="hof-card" style="border-left-color: {border};">
                <table style="width:100%; border:none;">
                    <tr>
                        <td style="width:50px; font-size:24px;">{medal}</td>
                        <td style="width:60px;"><img src="{avatar_url}" width="50" style="border-radius:50%;"></td>
                        <td style="font-size:20px; font-weight:bold;">{name}</td>
                        <td style="text-align:right; color:#00f2ff; font-family:Bungee;">{score} XP</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No legends yet. Start playing to enter the Hall of Fame!")
