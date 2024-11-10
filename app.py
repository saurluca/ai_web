from random import randint
import streamlit as st
from openai import OpenAI

# TODO Can interact with a before new riddle is started, thus not sytem prompt

# Setup part

# Set the sidebar to be collapsed by default
st.set_page_config(initial_sidebar_state="collapsed")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_num_tries" not in st.session_state:
    st.session_state.total_num_tries = 0

if "games_played" not in st.session_state:
    st.session_state.games_played = 0

if "riddles_solved" not in st.session_state:
    st.session_state.riddles_solved = 0

if "riddles" not in st.session_state:
    st.session_state.riddles = {
        "Easy": [
            {"riddle": "What has to be broken before you can use it?", "answer": "An egg"},
            {"riddle": "I’m tall when I’m young, and I’m short when I’m old. What am I?", "answer": "A candle"},
            {"riddle": "What can travel around the world while staying in the same corner?", "answer": "A stamp"},
            {"riddle": "What has hands but can’t clap?", "answer": "A clock"},
            {"riddle": "The more you take away, the bigger I get. What am I?", "answer": "A hole"},
            {"riddle": "What has legs but doesn’t walk?", "answer": "A table"},
            {"riddle": "I have a face and two hands, but no arms or legs. What am I?", "answer": "A clock"},
            {"riddle": "What has a head, a tail, but no body?", "answer": "A coin"},
            {"riddle": "What is full of holes but still holds water?", "answer": "A sponge"},
            {"riddle": "What gets wetter as it dries?", "answer": "A towel"}
        ],
        "Medium": [
            {"riddle": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "The letter 'M'"},
            {"riddle": "What is so fragile that saying its name breaks it?", "answer": "Silence"},
            {"riddle": "The more you take from me, the bigger I get. What am I?", "answer": "A hole"},
            {"riddle": "I am always in front of you but can’t be seen. What am I?", "answer": "The future"},
            {"riddle": "What begins with T, ends with T, and has T in it?", "answer": "A teapot"},
            {"riddle": "I’m found in socks, scarves, and mittens; and often in the paws of playful kittens. What am I?", "answer": "Yarn"},
            {"riddle": "What has a neck but no head?", "answer": "A bottle"},
            {"riddle": "What has cities, but no houses; forests, but no trees; and rivers, but no water?", "answer": "A map"},
            {"riddle": "The more of this there is, the less you see. What is it?", "answer": "Darkness"},
            {"riddle": "What has an eye but can’t see?", "answer": "A needle"}
        ],
        "Hard": [
            {"riddle": "What can run but never walks, has a bed but never sleeps, has a mouth but never talks?", "answer": "A river"},
            {"riddle": "I am not alive, but I can grow. I don’t have lungs, but I need air. I don’t have a mouth, but water kills me. What am I?", "answer": "Fire"},
            {"riddle": "The person who makes it doesn’t need it. The person who buys it doesn’t want it. The person who uses it doesn’t know it. "
                       "What is it?", "answer": "A coffin"},
            {"riddle": "Have keys but open no locks. You can enter but not leave. I have space but no rooms.", "answer": "A keyboard"},
            {"riddle": "Forward, I am heavy. Backward, I am not. What am I?", "answer": "A ton"},
            {"riddle": "I have branches, but no fruit, trunk, or leaves. What am I?", "answer": "A bank"},
            {"riddle": "I am a word of letters three, add two and fewer there will be. What am I?", "answer": "Few"},
            {"riddle": "The more you take, the more you leave behind. What am I?", "answer": "Footsteps"},
            {"riddle": "What comes at night without being called, and is lost in the day without being stolen?", "answer": "Stars"},
            {"riddle": "What has no beginning, or end?", "answer": "A circle"}
        ]
    }


def restart():
    print("restart")
    st.session_state.solved = False
    random_number = randint(0, 9)
    print("random number", random_number, add_selectbox)
    riddle = st.session_state.riddles[add_selectbox][random_number]

    system_prompt = {"role": "system", "content": f"You are a master of riddles. Ask the user the following riddle. The riddle: {riddle["riddle"]}, "
                                                  f"The answer: {riddle["answer"]}. Do not repeat the riddleThe user has to guess the answer. If the"
                                                  f" user guesses the riddle correctly, respond with message containing 'congratiolations'. The message"
                                                  f" correctly, respond with message containing 'Congratulations'. The message should also contain a"
                                                  f"section that start with 'Stats:' then 'number of tries: <num>'."}

    st.session_state.messages = [system_prompt]

    # Get initial response
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=False,
    )
    response_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response_message})
    st.session_state.games_played += 1


# Ui part

st.title("The Riddle game")

add_selectbox = st.selectbox(
    "Choose a difficulty level",
    ('Easy', 'Medium', 'Hard')
)

if st.button("New Riddle"):
    restart()

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

    if "Stats" in response:
        print("response end:::: ", response)
        stats = response.split("number of tries: ")
        print("stats", stats)
        if len(stats) == 2:
            st.session_state.total_num_tries += int(stats[1].strip(".!?:"))
            print("total num tries", st.session_state.total_num_tries)

        st.session_state.riddles_solved += 1


