from random import randint
import streamlit as st
from openai import OpenAI

# TODO If stats page loaded first, session state is not loaded, so error
# TODO add lives? max tries?
# TODO put riddles in extra file?

# Setup part

# Set the sidebar to be collapsed by default
st.set_page_config(initial_sidebar_state="collapsed")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session states to persist across reloads

# saves all messages, from user and assistant
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_num_tries" not in st.session_state:
    st.session_state.total_num_tries = 0

if "games_played" not in st.session_state:
    st.session_state.games_played = 0

if "riddles_solved" not in st.session_state:
    st.session_state.riddles_solved = 0

# saves the number of tries per riddle in a list
if "tries_per_riddle" not in st.session_state:
    st.session_state.tries_per_riddle = []

if "running" not in st.session_state:
    st.session_state.running = False

if "answer" not in st.session_state:
    st.session_state.answer = ""

# list of riddles to choose from, contains riddles of different difficulty with answers
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
            {"riddle": "The more you take, the more you leave behind. What am I?", "answer": "steps"},
            {"riddle": "What comes at night without being called, and is lost in the day without being stolen?", "answer": "Stars"},
            {"riddle": "What has no beginning, or end?", "answer": "A circle"}
        ]
    }


def restart():
    # increment games played every timeme a new riddle is started
    st.session_state.games_played += 1

    # choose a riddle from the list of riddles, based on the difficulty level and the random number
    random_number = randint(0, 9)
    # print("random number", random_number, add_selectbox)
    riddle = st.session_state.riddles[add_selectbox][random_number]
    st.session_state.answer = riddle["answer"]
    # system prompt to be sent to the AI, to tell it what to do
    system_prompt = {"role": "system", "content": f"You are a master of riddles. Ask the user the following riddle. The riddle: {riddle["riddle"]}, "
                                                  f"The answer: {riddle["answer"]}. The user has to guess the answer. If the"
                                                  f" user guesses the riddle correctly, respond with a message containing The answer: {riddle["answer"] }"
                                                  f"and a section that tells the number of tries like this 'number of tries: <num>'. And for each guess"
                                                  f"give a score from 1 to 10 to rate the quality of the guess."}
    # add the system prompt to the list of messages, so it is sent to the AI
    st.session_state.messages = [system_prompt]

    # Get initial response
    # noinspection PyTypeChecker
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=False,
    )
    # save response to assistant messages
    response_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response_message})

    st.session_state.running = True


# Ui part

st.title("The Riddle game")

# select box to choose difficulty level
add_selectbox = st.selectbox(
    "Choose a difficulty level",
    ('Easy', 'Medium', 'Hard')
)

# button to start a new riddle
if st.button("New Riddle"):
    restart()

# display all messages from the list of messages, except the first one, which is the system prompt
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# If game is running, display a chat input widget inline.
if st.session_state.running:
    if prompt := st.chat_input("Make a guess ..."):
        # Add user message to the list of messages
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # send response to assistant and stream the incoming response to the user
        with st.chat_message("assistant"):
            # noinspection PyTypeChecker
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # TODO make sure user can not abuse this and let AI write Stats
        # Prompted the AI to respond with a message containing 'Stats' at the end of the response
        if st.session_state.answer in response:
            print("response end: ", response)
            stats = response.split("number of tries: ")

            # double check, because stats should be a list with two elements
            if len(stats) == 2:
                num_tries = int(stats[1].strip(".!?:"))
                st.session_state.total_num_tries += num_tries
                # print("total num tries", st.session_state.total_num_tries)
                st.session_state.tries_per_riddle.append(num_tries)
                # print("tries per riddle", st.session_state.tries_per_riddle)

            # if the user guessed the riddle correctly, increment the number of riddles solved
            st.session_state.riddles_solved += 1

            # Set running to False to hide the input widget and force a reload of the page
            st.session_state.running = False
            st.rerun()
