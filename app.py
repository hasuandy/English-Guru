import streamlit as st
import sqlite3
import hashlib
from datetime import date
import random
import time

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('english_guru_v50.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (email TEXT PRIMARY KEY, username TEXT, password TEXT, xp INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS progress 
             (email TEXT, date TEXT, xp INTEGER, category TEXT)''')
conn.commit()

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_page' not in st.session_state: st.session_state.user_page = "📊 Dashboard"

def set_page():
    st.session_state.user_page = st.session_state.nav_key

# --- 3. THE "ATTRACTIVE" CYBER CSS ---
st.set_page_config(page_title="English Guru Pro", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Orbitron:wght@500;900&family=Rajdhani:wght@600&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #1a1a2e 0%, #050505 100%);
        color: #00f2ff;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Main Title Animation */
    .brand-title {
        font-family: 'Bungee', cursive;
        font-size: 5rem;
        text-align: center;
        background: linear-gradient(90deg, #00f2ff, #ff00ff, #00f2ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        filter: drop-shadow(0 0 10px rgba(0, 242, 255, 0.5));
        margin-top: -40px;
    }
    @keyframes shine { to { background-position: 200% center; } }

    /* Glassmorphism Cards */
    .cyber-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8), inset 0 0 15px rgba(0, 242, 255, 0.1);
        transition: 0.4s ease;
        text-align: center;
    }
    .cyber-card:hover {
        border-color: #ff00ff;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.3);
        transform: translateY(-5px);
    }

    /* Glowing Buttons */
    .stButton>button {
        background: transparent !important;
        color: #00f2ff !important;
        border: 2px solid #00f2ff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        border-radius: 50px !important;
        height: 55px;
        transition: 0.5s;
    }
    .stButton>button:hover {
        background: #00f2ff !important;
        color: #000 !important;
        box-shadow: 0 0 40px #00f2ff, 0 0 80px rgba(0, 242, 255, 0.3);
    }

    /* XP Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff00ff, #00f2ff) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.95) !important;
        border-right: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. APP LOGIC ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='brand-title'>ENGLISH GURU</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<div class='cyber-card'>", unsafe
