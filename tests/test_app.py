
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
    return at


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


# --- same root cause, different widget ---------------------------------------

def test_attempts_left_banner_reflects_the_submitted_guess(app):
    """st.info (app.py:49-52) still renders above the handler, so it lags."""
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
    assert app.session_state["history"] == [40]
    assert app.session_state["status"] == "playing"

    app.checkbox[0].set_value(False).run()

    assert app.session_state["secret"] == new_secret


def test_new_game_uses_active_range_and_changes_secret(app, monkeypatch):
    app.selectbox[0].select("Easy").run()
    app.session_state["secret"] = 20
    app.session_state["attempts"] = 4
    app.session_state["score"] = 45
    app.session_state["status"] = "won"
    app.session_state["history"] = [10, 20]
    monkeypatch.setattr(random, "randint", lambda low, high: high)

    new_game_button = next(
        button for button in app.button if button.label.startswith("New Game")
    )
    new_game_button.click().run()

    assert app.session_state["secret"] == 1
    assert app.session_state["secret"] != 20
    assert "Secret: `1`" in [item.value for item in app.markdown]
    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 0
    assert app.session_state["history"] == [10, 20]
    assert app.session_state["status"] == "playing"

    # Users have one less attempt to guess number. When they are
    # stated to have 8 attempts to guess the number, they only have 7.
