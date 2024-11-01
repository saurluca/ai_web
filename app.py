import streamlit as st
import numpy as np
from openai import OpenAI


# Set the sidebar to be collapsed by default
st.set_page_config(initial_sidebar_state="collapsed")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

system_prompt = {"role": "system", "content": "You are a riddle master. Your job is to ask the user a riddle based on the provided difficulty. The user will try to guess the answer. Use a new line for each line of the riddle. Rememeber the different answers by the user and rate each answer on a sacle from 1 to 10 on how good of a guess they were. Also after finishing the riddle tell the user how many attemtps they took to guess the right answer. "}


st.sidebar.title("Navigation")
st.title("The Riddle game")

add_selectbox = st.selectbox(
    "Choose a difficulty level",
    ('Easy', 'Possible', 'Blood sweat and tears')
)

if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display a chat input widget inline.
if prompt := st.chat_input("Say something ..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
