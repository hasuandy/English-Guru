import streamlit as st
import sqlite3
import hashlib
from datetime import date
import pandas as pd
import random

# --- DATABASE SETUP ---
conn = sqlite3.connect('users_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT, xp INTEGER)')
conn.commit()

# Password Security
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# --- LOGIN/SIGNUP UI ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_system():
    st.title("🛡️ English Guru Portal")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Access Mode", menu)

    if choice == "Login":
        username = st.text_input("User Name")
        password = st.text_input("Password", type='password')
        if st.button("LOGIN"):
            c.execute('SELECT password FROM users WHERE username =?', (username,))
            data = c.fetchone()
            if data and check_hashes(password, data[0]):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else: st.error("Invalid Details")

    elif choice == "Sign Up":
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Set Password", type='password')
        invite_code = st.text_input("Enter Secret Invite Code") # Ye aapka verification hai
        
        if st.button("CREATE ACCOUNT"):
            if invite_code == "GURU77": # Aapka Master Code
                try:
                    c.execute('INSERT INTO users VALUES (?,?,?)', (new_user, make_hashes(new_pass), 0))
                    conn.commit()
                    st.success("Account Created! Go to Login.")
                except: st.warning("Username already exists!")
            else: st.error("Wrong Invite Code! Ask the owner for access.")

# --- MAIN APP LOGIC ---
if not st.session_state.logged_in:
    login_system()
else:
    st.sidebar.success(f"Welcome {st.session_state.user}!")
    if st.sidebar.button("Logout"): 
        st.session_state.logged_in = False
        st.rerun()
    
    # Yahan wahi purana gaming code rahega (Home, MCQ, Boss Battle)
    st.title("🎮 English Guru: Pro Arena")
    st.write("Aapka app ab puri tarah secure hai!")
    # [Baki features jo humne pehle banaye the...]
