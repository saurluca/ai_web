import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "total_num_tries" not in st.session_state:
        st.session_state.total_num_tries = 0
    
    if "games_played" not in st.session_state:
        st.session_state.games_played = 0
    
    if "riddles_solved" not in st.session_state:
        st.session_state.riddles_solved = 0
    
    if "tries_per_riddle" not in st.session_state:
        st.session_state.tries_per_riddle = []
    
    if "running" not in st.session_state:
        st.session_state.running = False
    
    if "answer" not in st.session_state:
        st.session_state.answer = ""
        
    if "guess_qualities" not in st.session_state:
        st.session_state.guess_qualities = []  # Store quality scores for each guess


def get_average_tries():
    """Calculate average tries per game"""
    if st.session_state.games_played == 0:
        return 0
    return st.session_state.total_num_tries / st.session_state.games_played


def get_average_guess_quality():
    """Calculate average guess quality"""
    if not st.session_state.guess_qualities:
        return 0
    return sum(st.session_state.guess_qualities) / len(st.session_state.guess_qualities)
