import streamlit as st
import numpy as np


# Set the sidebar to be collapsed by default
st.set_page_config(initial_sidebar_state="collapsed")
st.sidebar.title("Navigation")


st.title("The Riddle game")

# print out hello world
add_selectbox = st.selectbox(
    "Choose a difficulty level",
    ('To Easy', 'Possible', 'Blood sweat and tears')
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#  Insert a chat message container.
# with st.chat_message("assistant"):
#     st.write("Hello there")
    # st.line_chart(np.random.randn(30, 3))

# Display a chat input widget inline.
if prompt := st.chat_input("Say something ..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

