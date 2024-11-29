import streamlit as st
from utils.state import initialize_session_state

st.set_page_config(
    page_title="Riddle Game",
    page_icon="🎮",
)

initialize_session_state()

st.title("Welcome to the Riddle Game! 🎮")

st.markdown("""
## How to Play
1. Navigate to the **Play** page to start solving riddles
2. Choose your difficulty level
3. Try to solve the riddle with as few guesses as possible
4. Check your performance in the **Stats** page

## Features
- Multiple difficulty levels
- AI-powered hint system
- Performance tracking
- Quality scoring for guesses

Good luck! :)
""")
