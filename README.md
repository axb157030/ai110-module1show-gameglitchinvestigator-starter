# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X ] Describe the game's purpose.
- [X ] Detail which bugs you found.
- [X ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Open a terminal. I used Powershell 
2. This may not be requred but please type and enter command, `pip install -r requirements.txt` 
3. Then please type and enter command, `streamlit run app.py`
4. Go to the UI and play the game. Guess for the secret number by inputting a number into the input field and click the `Submit Guess' button. To start a new game, either change difficulty in the sidebar or click the 'New Game' button. The difficulty levels are Easy, Normal, and Hard. They determine the range the secret number will be in and the number of attempts users has to guess for the secret.

5. Bugs I fixed
   - Inaccurate hints
   - Normal difficulty level given higher range secret is in than the Hard difficulty and vice versa.
   - I changed the blue block that showed the number range the secret will be in to a more accurate range and made it show more accurate attempts left.
   - I made the secret change upon user selecting a new game and also when they pick a different difficulty.
   - I stopped the debug info lagging. Now it updates nearly every time user submits a guess.
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```bash

tests/test_app.py::test_first_guess_is_recorded_in_session_state PASSED                             [  2%]
tests/test_app.py::test_invalid_guess_is_recorded_in_session_state PASSED                           [  5%]
tests/test_app.py::test_no_history_render_is_ever_stale PASSED                                      [  7%]
tests/test_app.py::test_valid_guess_is_visible_after_a_single_click PASSED                          [ 10%]
tests/test_app.py::test_both_guesses_visible_after_a_second_click PASSED                            [ 13%]
tests/test_app.py::test_invalid_guess_is_visible_after_a_single_click PASSED                        [ 15%]
tests/test_app.py::test_history_is_visible_on_first_page_load PASSED                                [ 18%]
tests/test_app.py::test_history_stays_visible_on_a_non_submit_interaction PASSED                    [ 21%]
tests/test_app.py::test_attempts_left_banner_reflects_the_attempt_limit_shown_in_sidebar_and_num_of_attempts_in_debug_info_expander_starts_at_zero PASSED [ 23%]
tests/test_app.py::test_whether_user_can_guess_for_secret_to_win_game_the_number_of_attempts_user_is_listed_to_have_to_guess_it PASSED [ 26%]
tests/test_app.py::test_secret_stays_fixed_when_a_guess_is_submitted PASSED                         [ 28%]
tests/test_app.py::test_changing_difficulty_starts_a_new_game_with_a_stable_secret PASSED           [ 31%]
tests/test_app.py::test_new_game_uses_active_range_and_changes_secret PASSED                        [ 34%]
tests/test_app.py::test_new_game_draws_a_real_random_secret_in_easy_range PASSED                    [ 36%]
tests/test_app.py::test_sidebar_shows_the_range_for_the_selected_difficulty PASSED                  [ 39%]
tests/test_app.py::test_main_panel_shows_the_range_for_the_selected_difficulty PASSED               [ 42%]
tests/test_game_logic.py::test_winning_guess PASSED                                                 [ 44%]
tests/test_game_logic.py::test_guess_too_high PASSED                                                [ 47%]
tests/test_game_logic.py::test_guess_too_low PASSED                                                 [ 50%]
tests/test_game_logic.py::test_guess_too_high_with_string_guess PASSED                              [ 52%]
tests/test_game_logic.py::test_guess_too_low_with_string_guess PASSED                               [ 55%]
tests/test_game_logic.py::test_get_range_for_difficulty_easy PASSED                                 [ 57%]
tests/test_game_logic.py::test_get_range_for_difficulty_easy_case_sensitivity PASSED                [ 60%]
tests/test_game_logic.py::test_get_range_for_difficulty_normal PASSED                               [ 63%]
tests/test_game_logic.py::test_get_range_for_difficulty_normal_and_case_sensitivity PASSED          [ 65%]
tests/test_game_logic.py::test_get_range_for_difficulty_hard PASSED                                 [ 68%]
tests/test_game_logic.py::test_get_range_for_difficulty_hard_and_case_sensitivity PASSED            [ 71%]
tests/test_game_logic.py::test_get_range_for_difficulty_invalid_difficulty PASSED                   [ 73%]
tests/test_game_logic.py::test_parse_guess_if_guess_is_none PASSED                                  [ 76%]
tests/test_game_logic.py::test_parse_guess_if_guess_is_empty_string PASSED                          [ 78%]
tests/test_game_logic.py::test_parse_guess_if_guess_is_just_spaces PASSED                           [ 81%]
tests/test_game_logic.py::test_parse_guess_if_guess_is_alphanumerical PASSED                        [ 84%]
tests/test_game_logic.py::test_parse_guess_if_guess_is_alphanumerical_and_has_spaces PASSED         [ 86%]
tests/test_game_logic.py::test_parse_guess_if_guess_is_floating_number PASSED                       [ 89%]
tests/test_game_logic.py::test_parse_guess_if_guess_is_integer PASSED                               [ 92%]
tests/test_game_logic.py::test_update_score_with_easy_values_to_check_whether_it_returns_an_integer PASSED[ 94%]
tests/test_game_logic.py::test_update_score_with_score_below_secret PASSED                          [ 97%]
tests/test_game_logic.py::test_update_score_with_score_higher_than_secret PASSED                    [100%]

=========================================== 38 passed in 4.22s ===========================================
```


## 🚀 Stretch Features

- [X ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
   - I added a snow animation when user clicks the 'New Game' Button
