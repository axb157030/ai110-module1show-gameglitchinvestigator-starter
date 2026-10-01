
"""
Made by Claude Pro and GitHub Copilot
Tests for the "guess only appears after a second submit" bug in app.py.

TESTS ONLY -- nothing here modifies app.py or logic_utils.py.

THE ORIGINAL BUG
    The "Developer Debug Info" expander rendered st.session_state.history near
    the top of the script, but the submit handler appends to that list further
    DOWN. Streamlit reruns top-to-bottom on every interaction, so the panel
    painted the list BEFORE the new guess was added and always lagged one
    submission behind. The guess was recorded correctly -- it was just drawn a
    run too late, which is why a second click appeared to be required.

WHY THESE TESTS ARE STRUCTURE-AGNOSTIC
    There is more than one way to fix this (move the display below the handler,
    or render the history from inside the handler). These tests therefore do not
    care WHERE the history is drawn. They assert the behaviour that matters:

      1. every place the UI draws the history shows the CURRENT history, and
      2. the history is actually visible to the user.

    That keeps them valid across either fix, and keeps them honest -- adding a
    second, fresh render while leaving a stale one in place will still fail (1).

READING THE RESULTS
    Assertions on at.session_state  -> "was it recorded?"   (the data layer)
    Assertions on rendered elements -> "was it shown?"      (the UI)
    The bug is those two disagreeing.

Set GLITCH_APP_FILE to run the suite against a modified copy of the app, to
check a candidate fix without editing app.py itself.
"""

import json
import os
import random
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_FILE = Path(
    os.environ.get("GLITCH_APP_FILE", Path(__file__).resolve().parents[1] / "app.py")
)

SECRET = 50
GUESS_INPUT_KEY = "guess_input_Normal"  # key is f"guess_input_{difficulty}"


@pytest.fixture
def app():
    """A freshly started app with a fixed secret, so no guess wins by luck."""
    at = AppTest.from_file(str(APP_FILE)).run()
    at.session_state["secret"] = SECRET
    # print(at._tree) 
    return at
'''From Claude Pro after asking it 
was doesnt app.markdown list all the ui how do you 
know it just shows the accordian that shows lit 
of attributes.
From Claude Pro: 
"at.markdown lists the text you wrote 
with st.write/st.markdown, not the UI. 
If you add a st.write("Attempts left: ...") at 
the top of app.py tomorrow, it'll appear in 
at.markdown at index 0 and shift everything — which 
is why index-based assertions like at.markdown[0] 
are fragile, and why startswith("Secret:") filtering is safer."
'''
'''
markdown attribute is not an attribute of the file read,
it is an attribute from AppTest. According to Claude Pro,

"at.markdown includes only things the app drew to the 
UI as markdown text — never print()."
'''

def submit_guess(at, raw_value):
    """Type a guess and click 'Submit Guess' -- exactly one real user click."""
    at.text_input(key=GUESS_INPUT_KEY).set_value(raw_value)
    button = next(b for b in at.button if b.label.startswith("Submit Guess"))
    button.click().run()
    return at


def history_renders(at):
    """Every history list the UI drew on this run, wherever it was drawn.

    st.write("History:", <list>) emits an st.json element whose .value is the
    serialized list, and that is the app's only source of st.json elements, so
    this reads back exactly what the user can see -- in any expander, in any
    branch, in any order.
    """
    return [json.loads(e.value) for e in at.json]


def attempts_left_in_ui(at):
    """The 'Attempts left: N' number as rendered in the st.info banner."""
    text = at.info[0].value
    return int(text.rsplit("Attempts left:", 1)[1].strip().rstrip("."))

def secret_range_in_main_panel_ui(at):
    """The 'Secret range: N' number as rendered in the st.info banner."""
    text = at.info[0].value
    # Extract this "f"Guess a number between {low} and {high}. " from text
    # Extract 1 and 100 from '1 and 100. Attempts left: 5'  
    return text.rsplit("Guess a number between ", 1)[1].strip().rstrip(".").split(" and ")[0] + " to " + text.rsplit("Guess a number between ", 1)[1].strip().rstrip(".").split(" and ")[1].split(".")[0]



# --- the data layer is fine: these pass even with the bug present ------------

def test_first_guess_is_recorded_in_session_state(app):
    submit_guess(app, "40")

    assert app.session_state["history"] == [40]


def test_invalid_guess_is_recorded_in_session_state(app):
    submit_guess(app, "not a number")

    assert app.session_state["history"] == ["not a number"]


# --- invariant 1: no render may be stale -------------------------------------

def test_no_history_render_is_ever_stale(app):
    """Catches the original bug AND any leftover stale copy of the display."""
    for guess in ("40", "30", "20"):
        submit_guess(app, guess)
        stored = app.session_state["history"]
        for i, shown in enumerate(history_renders(app)):
            assert shown == stored, (
                f"history render #{i} shows {shown} but state holds {stored} -- "
                "a display is running before the submit handler"
            )


# --- invariant 2: the history must be visible --------------------------------

def test_valid_guess_is_visible_after_a_single_click(app):
    """The headline symptom: one click must be enough to see the guess."""
    submit_guess(app, "40")

    renders = history_renders(app)
    assert renders, "one click recorded the guess but nothing rendered the history"
    assert [40] in renders, f"expected a render of [40], got {renders}"


def test_both_guesses_visible_after_a_second_click(app):
    submit_guess(app, "40")
    submit_guess(app, "30")

    assert [40, 30] in history_renders(app)


def test_invalid_guess_is_visible_after_a_single_click(app):
    """The error branch (app.py:95) appends too, so it must render too."""
    submit_guess(app, "not a number")

    renders = history_renders(app)
    assert renders, "invalid guess was recorded but the history was not rendered"
    assert ["not a number"] in renders


def test_history_is_visible_on_first_page_load(app):
    """An empty history is still a history -- the panel should exist on load."""
    assert history_renders(app) == [[]], (
        "no history rendered before the first submit -- the display only runs "
        "inside the submit branch"
    )


def test_history_stays_visible_on_a_non_submit_interaction(app):
    """Toggling an unrelated widget must not make the history vanish."""
    submit_guess(app, "40")
    app.checkbox[0].set_value(False).run()  # "Show hint"

    renders = history_renders(app)
    assert renders, "history disappeared on a rerun that was not a submit"
    assert [40] in renders



# I later greatly modified it
def test_attempts_left_banner_reflects_the_attempt_limit_shown_in_sidebar_and_num_of_attempts_in_debug_info_expander_starts_at_zero(app):
    attempt_limit = attempts_left_in_ui(app)
    attempt_limit_from_sidebar = app.sidebar.caption[1].value.split(':')[1].strip()
    print(f"attempt_limit_from_sidebar {attempt_limit_from_sidebar}")
    print(f"attempt_limit {attempt_limit}")
    assert str(attempt_limit) == attempt_limit_from_sidebar, ("Attempt limit shown should " +
    "be same in the one shown in the sidebar where users " +
    "can select difficulty and the one in the main panel in the blue block")
    attempts = 0 # Number of attempts user guessed the secret number
    for attempt_num in range(attempt_limit):
        assert app.session_state.attempts == attempts, (
            "Attempts left at end should be 0 and number number of attempts should start at 0" 
    )
        submit_guess(app, "40")
        attempts +=1
    # Users have one less attempt to guess number. When they are
    # stated to have 8 attempts in the sidebar shown in the UI as the number of attempts
    # shown in the UI defaults to 1 upon starting a game instead of 0 when user initially starts the application.
        
        


def test_whether_user_can_guess_for_secret_to_win_game_the_number_of_attempts_user_is_listed_to_have_to_guess_it(app):

    before = attempts_left_in_ui(app)

    submit_guess(app, "40")

    assert attempts_left_in_ui(app) == before - 1, (
        "the attempts banner renders above the submit handler, so it is stale"
    )

def test_secret_stays_fixed_when_a_guess_is_submitted(app):
    submit_guess(app, "40")

    assert app.session_state["secret"] == SECRET


def test_changing_difficulty_starts_a_new_game_with_a_stable_secret(app):
    app.session_state["secret"] = 88
    app.session_state["attempts"] = 3
    app.session_state["score"] = 15
    app.session_state["history"] = [40]

    app.selectbox[0].select("Easy").run()

    new_secret = app.session_state["secret"]
    assert 1 <= new_secret <= 20
    assert f"Secret: `{new_secret}`" in [item.value for item in app.markdown]
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert app.session_state["status"] == "playing"

    app.checkbox[0].set_value(False).run()

    assert app.session_state["secret"] == new_secret
    
# I modified this.
def test_new_game_uses_active_range_and_changes_secret(app):
    app.selectbox[0].select("Easy").run()
    app.session_state["secret"] = 50
    app.session_state["attempts"] = 4
    app.session_state["score"] = 45
    app.session_state["status"] = "won"
    app.session_state["history"] = [10, 30]

    new_game_button = next(
        button for button in app.button if button.label.startswith("New Game")
    )
    new_game_button.click().run()
    print("After new game, the secret " + str(app.session_state["secret"]))
    assert app.session_state["secret"] >= 1 and app.session_state["secret"] <= 20
    assert any(str(app.session_state["secret"]) in item.value for item in app.markdown)
    # assert f"Secret: `{new_secret}`" in [item.value for item in app.markdown]
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == []
    assert app.session_state["status"] == "playing"


def test_new_game_draws_a_real_random_secret_in_easy_range(app):
    """Exercise the REAL random draw -- no monkeypatch -- over many draws.

    One real draw is a weak test: against the old hardcoded random.randint(1, 100)
    the value still lands in 1..20 about 20% of the time, so the bug slips through
    roughly one run in five. Sampling 50 draws cuts that false-pass chance to
    0.2 ** 50, while still testing the genuine random behaviour end to end.
    """
    DRAWS = 50
    app.selectbox[0].select("Easy").run()

    secrets = []
    for _ in range(DRAWS):
        button = next(b for b in app.button if b.label.startswith("New Game"))
        button.click().run()
        secrets.append(app.session_state["secret"])

    out_of_range = [s for s in secrets if not 1 <= s <= 20]
    assert not out_of_range, (
        f"{len(out_of_range)}/{DRAWS} secrets fell outside Easy's range 1..20: "
        f"{sorted(set(out_of_range))}"
    )
    assert len(set(secrets)) > 1, (
        f"the secret was {secrets[0]} in all {DRAWS} draws -- it is not being redrawn"
    )

# Made by Claude Pro when I asked it how to extract from the sidebar in the app to test whether the attempts left and number of attempts the app listed during the first game when application restartsn is accuratr
def test_sidebar_shows_the_range_for_the_selected_difficulty(app):
    app.selectbox[0].select("Hard").run()


    assert app.sidebar.caption[0].value == "Range: 1 to 100"
    assert app.sidebar.caption[1].value == "Attempts allowed: 5"


def test_main_panel_shows_the_range_for_the_selected_difficulty(app):
    app.selectbox[0].select("Hard").run()

    assert secret_range_in_main_panel_ui(app) == "1 to 100"
