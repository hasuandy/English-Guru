import streamlit as st

# Page Title
st.set_page_config(page_title="English Guru Live")

# Data Save karne ke liye
if 'xp' not in st.session_state:
    st.session_state.xp = 0

st.title("🎮 English Guru: LIVE!")
st.write("Bhai, agar ye dikh raha hai toh aapki app chal gayi! 🎉")

# Sidebar
st.sidebar.header(f"XP: {st.session_state.xp}")
name = st.sidebar.text_input("Apna Naam Likho:", "Hero")

# Main Game
st.subheader(f"Welcome, {name}!")
if st.button("Get 10 XP"):
    st.session_state.xp += 10
    st.success("Mil gaye 10 XP!")
    st.balloons()

st.metric("Total Score", st.session_state.xp)
