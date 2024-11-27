import streamlit as st
from openai import OpenAI
from random import randint
from utils.riddles import RIDDLES
from utils.state import initialize_session_state

# Initialize session state
initialize_session_state()

model = "gpt-4o-mini"

# Set OpenAI API key
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Error initializing OpenAI client. Please check your API key.")
    st.stop()

def restart():
    """Start a new game with a new riddle"""
    try:
        st.session_state.games_played += 1
        
        # Get the current difficulty level
        difficulty = st.session_state.get('difficulty', 'Easy')
        
        # Get the number of riddles for the current difficulty
        num_riddles = len(RIDDLES[difficulty])
        if num_riddles == 0:
            raise ValueError(f"No riddles found for difficulty level: {difficulty}")
            
        # Generate random index within bounds
        random_number = randint(0, num_riddles - 1)
        
        # Get the riddle
        riddle = RIDDLES[difficulty][random_number]
        st.session_state.answer = riddle["answer"]
        
        system_prompt = {
            "role": "system", 
            "content": f"""You are a master of riddles. Ask the user the following riddle. 
            The riddle: {riddle["riddle"]}, The answer: {riddle["answer"]}. 
            The user has to guess the answer. If the user guesses correctly, respond with:
            'Correct! The answer is: {riddle["answer"]} number of tries: <num>'.
            For each guess, rate its quality from 1-10 and explain why, format as:
            'Guess quality: X/10 - [explanation]'"""
        }
        
        st.session_state.messages = [system_prompt]
        
        # Add error handling for API call
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=False,
            )
            
            response_message = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": response_message})
            st.session_state.running = True
            
        except Exception as api_error:
            st.error(f"Error communicating with OpenAI API: {str(api_error)}")
            return
            
    except Exception as e:
        st.error(f"Error starting new game: {str(e)}")
        return


st.title("Play the Riddle Game 🎲")

add_selectbox = st.selectbox(
    "Choose difficulty level",
    ('Easy', 'Medium', 'Hard')
)

if st.button("New Riddle"):
    restart()

# Display chat history
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if st.session_state.running:
    try:
        if prompt := st.chat_input("Make a guess..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=model,
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Extract guess quality if present
            if "Guess quality:" in response:
                try:
                    quality_text = response.split("Guess quality:")[1].split("/")[0]
                    quality = int(quality_text.strip())
                    st.session_state.guess_qualities.append(quality)
                except (ValueError, IndexError) as e:
                    st.error(f"Error parsing guess quality: {str(e)}")

            # Handle correct answer
            if st.session_state.answer in response:
                stats = response.split("number of tries: ")
                if len(stats) == 2:
                    try:
                        # Extract only the number before any extra text
                        num_tries = int(stats[1].split()[0].strip(".!?:"))
                        st.session_state.total_num_tries += num_tries
                        st.session_state.tries_per_riddle.append(num_tries)
                    except ValueError as e:
                        st.error(f"Error parsing number of tries: {str(e)}")
                st.session_state.riddles_solved += 1
                st.session_state.running = False
                st.rerun()

    except Exception as e:
        st.error(f"Error processing guess: {str(e)}")
