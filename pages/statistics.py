import streamlit as st


st.title("Statistics")

# write out statistics
st.write("Games played: ", st.session_state.games_played)
st.write("Riddles solved: ", st.session_state.riddles_solved)
st.write("Total number of tries: ", st.session_state.total_num_tries)

average_tries = 0

# for 0 safe division
if st.session_state.riddles_solved > 0:
    average_tries = round(st.session_state.total_num_tries / st.session_state.games_played, 2)

st.write("Average number of tries per solved riddle: ", average_tries)

# bar chart to display tries per riddle
st.bar_chart(st.session_state.tries_per_riddle, x_label="Riddle number", y_label="Number of tries")
