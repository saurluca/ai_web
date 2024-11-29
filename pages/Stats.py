import streamlit as st
import pandas as pd
import plotly.express as px
from utils.state import initialize_session_state, get_average_tries, get_average_guess_quality

# Initialize session state
initialize_session_state()

st.title("Game Statistics 📊")

# Display basic stats
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Games Played", st.session_state.games_played)

with col2:
    avg_tries = get_average_tries()
    st.metric("Average Tries per Riddle", f"{avg_tries:.1f}")

with col3:
    success_rate = (st.session_state.riddles_solved / st.session_state.games_played * 100) if st.session_state.games_played > 0 else 0
    st.metric("Success Rate", f"{success_rate:.1f}%")

# Guesses per game chart
st.subheader("Guesses per Riddle")
if st.session_state.tries_per_riddle:
    st.bar_chart(st.session_state.tries_per_riddle, x_label="Riddle number", y_label="Number of tries")
else:
    st.info("Play some games to see statistics!")

# Guess quality analysis
st.subheader("Guess Quality Analysis")
if st.session_state.guess_qualities:
    avg_quality = get_average_guess_quality()
    st.metric("Average Guess Quality", f"{avg_quality:.1f}/10")
    
    df_quality = pd.DataFrame({
        'Guess': range(1, len(st.session_state.guess_qualities) + 1),
        'Quality': st.session_state.guess_qualities
    })
    fig_quality = px.line(df_quality, x='Guess', y='Quality', 
                         title='Guess Quality Over Time',
                         labels={'Quality': 'Quality Score (1-10)'})
    st.plotly_chart(fig_quality)
    
    # Quality distribution
    quality_dist = pd.DataFrame({
        'Quality': list(range(1, 11)),  # Explicitly create bins from 1-10
        'Count': [st.session_state.guess_qualities.count(i) for i in range(1, 11)]  # Count occurrences of each score
    })
    fig_dist = px.bar(quality_dist, 
                     x='Quality', 
                     y='Count',
                     title='Distribution of Guess Qualities',
                     labels={'Count': 'Number of Guesses', 'Quality': 'Quality Score'})
    fig_dist.update_xaxes(tickmode='linear')
    st.plotly_chart(fig_dist)
else:
    st.info("Make some guesses to see quality analysis!")

