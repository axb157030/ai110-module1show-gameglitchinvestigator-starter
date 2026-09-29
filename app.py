import random
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score
import streamlit as st
import os;

# GitHub Copilot and I did to restart the game and change secret
# Every time user switches difficulty or starts a new game
def start_new_game(low, high):
    #Try this attempt_limit = attempt_limit_map[difficulty]
    secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.secret = secret
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)
# How to test this. Even though it does not define a function. main
attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state: 
    st.session_state.secret = random.randint(low, high) 

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty
elif st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game(low, high)

st.subheader("Make a guess")

attempts_display = st.empty()
debug_info_display = st.empty()

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁", on_click=start_new_game, args=(low, high))
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.success("New game started.")

os.write(1, f"&&&&&&{new_game}\n".encode()) 
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
elif submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)
        # I asked GitHub Copilot, it says: "In the current app.py:98-103, 
        # st.session_state.secret is converted to a string on 
        # every even-numbered attempt:"
        # secret = str(st.session_state.secret)
        # After reading that from GitHub Copilot, I asked whether
        # the if else statement that converts secret to a string upon
        # even attemps should be deleted. It agreed
        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret
        #Remove
        #secret = st.session_state.secret
            

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

with attempts_display.container():
    st.info(
        f"Guess a number between 1 and 100. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
# Must be after submit handler so that it gets the data upon submitted
# not before it was submitted.
# Made by GitHub Copilot.
#According to GitHub Copilot regarding this:
    # Because Streamlit runs the script top to bottom. 
    # If the banner and debug panel render before the submit 
    # handler, they read the old attempts and history. 
    # Later changes to st.session_state don’t automatically
    # redraw elements that were already rendered.

    # In this app, the placeholders are created above 
    # the controls to reserve their page positions, 
    # then filled after the handler so they display the 
    # updated values. You could instead render the updated 
    # values inside the submit handler; what matters is that 
    # the render happens after the state change.

with debug_info_display.container():
    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")