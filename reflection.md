# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - It looks good and from a glance, it looked finished.
  - It had a **sidebar** with "Settings" as it header, a Difficulty select box having options Easy, Normal, and Hard defaulting to Normal, 
  a caption that displayed the number of attempts per difficult per difficulty and 
  another caption stating the range per difficulty.
    - Attempt captions
      - 6 for Easy difficulty
      - 8 for Normal difficulty
      - 5 for hard difficulty
    - Range captions:
      - 1 to 20 when the diffculty field easy option was picked
      - 1 to 100 when the diffculty field normal option was picked
      - 1 to 50 when the diffculty field hard option was picked

  - It has a **main panel** that has a big header, Game Glitch Investigator,
  a blue info banner stating the range and attempts left, a "Developer Debug Info" expander listing the secret, attempts, score, difficulty, and history, a text input for the guess, and a row with Submit Guess, New Game, and a "Show hint" checkbox. Submitting a guess produced a yellow warning banner with the hint [[1]](#1).
    - It has a blue block that always says the generated number to find in the game ranges from 1 to 100 and provides the number of attempts remaining even when the number is not in that range. 
    - It has an accordian that tells the number of attempts, the score, and history.
    - Below the accordian it has an input field where users can guess the number.
    - Below the input field there is a section that provides buttons from left to right
    to submit the guess and to start a new game. In that row where the submit and new game buttons are, there is check input field that allows users to decide whether hints should show or not.
    - There is a yellow block that appears when users submit a number that is suppose to
    provide hints.

<br/>
<div>
<img src="./assets/gameglitchinvestigator_before_changes_and_bugfixes.png"/>
</div>


> *Terminal output documenting the game was run before any code changes*


- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
    - **1. In **sidebar** listed Ranges does not correspond with the range of numbers the secret  number to guess is between"**
      - The Range field in the sidebar seems misleading as they do not correspond to the range of numbers that the random number can be in. 
    - **2. in the **sidebar** Difficulty doesn't scale coherently [[1]](#1)
      - Normal grants the most attempts (8) against the widest range (1 to 100), while Hard grants the fewest (5) against a narrower range (1 to 50), so "Hard" is not reliably harder than "Normal" [[1]](#1).
    
    - **3. "Attempts left" in the blue box in the **Main Panel** is off by one and lags a turn behind.**
      - The blue block in the **main panel** provides an inaccurate number of the attempts left. It is one off.      
        - Before the user inputs their guessed number when the game starts the blue block in normal difficulty says user has 7 attempts even when they have 8. 
        - The "Attempts left" number does not change after the user inputs their first guess to the application, but changes and decrements starting from the user's second attempt onward
  
      **4. Inaccurate range in the blue block**
        - It keeps stating: "Guess a number between 1 and 100." no matter what the range stated in the **side bar** is.
      
      **5. The debug expander shows stale state for the same reason [[1]](#1)**
      - The Attempts field in the expander starts with 1 even though when the game starts no attempts were made.
      - The Attempts field does not update upon user inputing and submitting their first guess. It updates upon user changing the input field to provide guessed number upon second attempts and onward.
      - When the user guesses the number, the expander only shows the updated score upon the next guess. 
      - The history field in the exapnder, only shows the last number that the user guessed upon submitting another guessed number after it, not immediately upon user submitted the guessed number. 
        - For example, user inputs 10 on the input field on first try and then clicks the submit button, the history field in the accordian will not show it. After the user inputs another number, for example 45 and then clicks the submit button, the history field will show only that the user only inputted number 10 for the current playthough.
    

    **6. The hints were backwards**
      - When I guess a number that is <i>higher</i> than the secret number to find in the game, the hints say to "Go LOWER!". 
      - When I guess a number that is <i>lower</i> than the secret number to find in the game, the hints say to "Go HIGHER!".

  
  <br/>
<div>
<img src="./assets/gameglitchinvestigator_some_initial_errors.png"/>
</div>


> *Terminal output documenting some errors shown while running the game before any code changes*

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Difficulty = Normal, secret = 76 (from Developer Debug Info). Submit a guess of 20| 20 < 76, so the app should report **Too Low** and give a hint of *Go LOWER* | App reports **Too High** and it gives a hint of  *Go HIGHER*  | No traceback — a TypeError: '>' not supported between instances of 'int' and 'str' is raised and silently swallowed by the except TypeError fallback. [[2]](#2). Also [look at failed test case](#3) |
|Set difficulty to Normal |Range is 1, 50 | Range is 1, 100|[Look at failed test case](#4) |
|Set difficulty to Hard |Range is 1, 100 | Range is 1, 50|[Look at failed test case](#5) |
|The input is Easy, Normal and Hard.When difficulty is Easy, Normal| The **Secret** always has a range from 1 to 100 despite the difficulty set. When difficulty is Easy, Normal, Hard secret should be in range from 1 to 30, 50, and 100 respectively. Regardless whether user just started the application or clicked new game | Secret is always between 1 to 100. It can be greater than 20 and 50 regardless of the difficulty chosen. The default difficulty when setting the secret is always "Normal".|[Look at the error. The picture and bug](#6) |
| Guess 40 and it is the first guess, secret is 50, and user clicks submit button |The history list in the UI is not showing the guess upon submit. | The history list should show the guess | The history of the guesses has some laging. The user submits a guess and their guess is not showing in the history list in the UI unless they submit it again [See the picture of the UI](#6). |
| Guess 40 and it is the first guess, and it is the first guess, secret is 50, and user clicks submit button |The **score** should update immediately with a score of -5. the guess | The score is showing as 0, The score field in the UI is not showing any updated score.| The score is not updated immediately upon the submitted. Also [See picture of the UI](#6)|
| The difficulty selected to Easy | The **main panel** should show "Guess a number between 1 and 20." |It shows "Guess a number between 1 and 100. "| The **main panel** always shows "Guess a number between 1 and 100." regardless of difficulty. It should represent the range of the secrets based on the difficulty user selected [See picture](#7).|
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I primarily used Claude and GitHub Copilot for this project.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - I wanted to find why the history list that the game would show required users to submit
  another guess for their previous game to be recorded and shown in it.
  According to GitHub Copilot to fix this issue: 

```bash
The history is appended when you click Submit, but the app displays it earlier in the script. The “Developer Debug Info” expander writes st.session_state.history before the submit handler runs, so Streamlit’s rerun shows the previous history; your new guess appears on the next rerun, which makes it look like you need to submit twice.

Move the history display below the submit handler (or render it in a placeholder that you update after appending). The append itself is happening on the first submit. You can see the render and append order in app.py:47 and app.py:94.
```
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

  - I asked it to improve my document by making it easier to read and understand. Initially it remade the reflection.md file but, I rejected much of the content it generated as I wanted to better document applications myself and use AI ethically.  Also importantly I wanted to keep the original structure of the reflection.md. I felt that it did not strictly abide by the stakeholder requirements because of that. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I used what I would normally consider to be correct such as giving hints to tell users to guess lower when they guessed a higher number than the secret number to guess and that more challenging difficulties such Hard over Normal should have a wider range. I then essentially made an acceptance criteria it had to pass. I would run the UI and if it showed to be running correctly I would mark it as correct. 
  - Also I made test cases with pytest, which had to pass as well.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
    - There was an error, secrets were not in range of selected difficulty when I changed difficulties in the game from the UI. The secrets initially would not change at all unless the application was reloaded. I decided to test removing a conditional conditional [Look at the bug](#6) in the code
    and modify the code to also show the secret in the tab bar, to find why the secret generated had no relation to what difficulty the user picked. The secret was changing but no one could guess the secret as it would immediately change upon submission. So I asked GitHub Copilot. We stored the difficulty user selected in the streamlit session state where the one that was not in session state made a function to reset the values except for the difficulty and called that whenever user clicked a new game or the difficulty user selected was different from the one stored in the streamlit session, the previous difficulty, the secret and the debug log would reset. Essentially we made a function called  `start_new_game(low, high)` to reset the debug data and moved down displaying the debug info in the apppy file making it just before `st.divider()`.
    - I tested those changes by checking the results in the UI upon my clicking a different difficulty and my clicking on new game with a different difficulty. After every difficulty level and new game, I selected, the secret shown in the UI immediately updated in both the backend service and its UI. Also these changes made the score and history update in time, but also introduced a bug regarding the number of times a user can attempt to guess the number.
      - **The bug it introduced** allowed the user one less than the attempt limit shown in the sidebar of the UI and made the main panel show the attempt limit is one less than it. I uses this to test it using pytest. [Please see this for more details](#9). I
      made a fix through by changing the initial number of attempts from 1 to 0 and then  tested it in the UI by checking the attempt limit in both the side bar and main panel are the same and by using all the available guesses users can submit in a game to see whether the attempt limit provides the actual number of times a user can submit a guess to find the secret number.

    - I also tested for this secret changing issue by using pytest [[8]](#8).

    - I ran tests with pytest to test that the score function that calculates the scores correctly calculates the score. The test case passed with no code changes [[10]](#10). 

    - **Another Bug Fix** # Backward hints. I made the hints suggest users to guess higher when the guess is lower than the secret number to find and lower when the guess is higher than the secret number to define. The bug was in the method `check_guess`. It would return `Too High", "📈 Go HIGHER!` and `"Too Low", "📉 Go LOWER!"` I changed those return statements to return  `"Too High", "📉 Go LOWER!"` and `Too Low", "📈 Go HIGHER!"`. Also there was others bugs that was passing the secret as a string rather than an integer. I fixed that, [please see more here](#3) I manually tested in the UI and the hints were showing accurately.

    - Also the blue block in the main panel was given an inaccurate range, It always gave
    "Guess a number between 1 and 100." . [ Please see](#7). I changed that by adding replacing a line of code in app.py with 
    `f"Guess a number between {low} and {high}. "
`
 

- Did AI help you design or understand any tests? How?

  - Yes it did. GitHub Copilot initially made the test_app.py file, but the content was replaced by Claude Pro and it taught me how to test streamlit files that make UI changes rather than base Python files by making test cases for app.py that did effect the UI. It taught me by providing examples. Please see test_app.py



---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - session state holds the values that the UI shows. They are like a list of variables that can hold many types of data in JavaScript. Streamlit "reruns" Rerender the UI to show the updated data of the session state.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    - Asking AI agents to provide me examples on how to test applications or units of code I am really unfamiliar with 
    and make test cases on my own from their using AI Agents as an assistant for making them from there. 
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would come up with acceptance criteria. I would brainstorm and write down what I want to be completed. Ask AI to assist me in brainstorming and coming up the acceptance criteria and the description describing the application design and function etc. I would come up with some classes of my own. Then I would ask the AI to build based on those classes, acceptace criteria and descriptions I provided. I would also ask AI to give detailed and simple explanations for them to ensure I understand them.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - It is important to really know the application. When I asked GitHub Copilot to make test cases to find whether the history list updates and shows in the UI, it made a test case that did not test for it showing the updates in the UI.

## 6. Citations and Extra Notes

<a id="1">[1]</a>: Anthropic. Claude Pro. https://claude.ai. 
  - I asked it to improve the reflection.md by making it easier to read and understand. 

<a id="2">[2]</a>: Anthropic. Claude Pro. https://claude.ai. 
  - I asked Claude to find a bug and fufill the documentation noting it in the reflection.md file.
    - I previous found the error it documented when I was playing with the application when it was running on a browser. It said to submit two guess to find the error. Two guesses were not needed. The results and hints came after submitted the first guess I made so I modified it stating it needs only one guess and documented the same error but with different inputs testing the application in the browser.. <a href="ai_interactions.md"> See ai_interactions.md</a>.

  - It completed a row in the Bug Reproduction Log that provided information on a bug it found. The bug it found was the backward hints. 
  - It guided me on how to report bugs for this project and
  how to make tables in .md files.

<a id="3">[3]</a>:
```bash
FAILED tests/test_game_logic.py::test_guess_too_high - AssertionError: assert '📈 Go HIGHER!' == '📉 Go LOWER!'
FAILED tests/test_game_logic.py::test_guess_too_low - AssertionError: assert '📉 Go LOWER!' == '📈 Go HIGHER!'
```
Suspected bugs for the inaccurate hints

In logic_utils.py

```bash
    
    try:
        if guess > secret:
            return "Too High", "📈 Go HIGHER!"
        else:
            return "Too Low", "📉 Go LOWER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go HIGHER!"
        return "Too Low", "📉 Go LOWER!"
        # The return "Too High", "📈 Go HIGHER!" is the bug
        # It should be return "Too High", "📉 Go LOWER"
        # return "Too Low", "📈 Go HIGHER!"
        # These bugs are in logic_utils.py file
```

```bash
    # The bug was that the guesses and secrets were # not parsed to integers. 
      # '40' < 9  will return true
      # '40' < '9'  will return true
      # 40 < 9  will return false
    # The bug fix applied.
    if(type(guess) == str):
            guess = guess.strip() if guess is not None else None
            guess = int(guess) if guess and guess.isdigit() else guess

    if(type(secret) == str):
            secret = secret.strip() if secret is not None else None
            secret = int(secret) if secret and secret.isdigit() else secret

    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"
```

In app.py

```bash
        st.session_state.history.append(guess_int)
        # I asked GitHub Copilot, it says: "In the current app.py:98-103, 
        # st.session_state.secret is converted to a string on 
        # every even-numbered attempt: making the hints inaccurate."
        # secret = str(st.session_state.secret)
        # After reading that from GitHub Copilot, I asked whether
        # the if else statement that converts secret to a string upon
        # even attemps should be deleted. It agreed
        # BUG
        #if st.session_state.attempts % 2 == 0:
        #    secret = str(st.session_state.secret)
        #else:
        #    secret = st.session_state.secret
        # BUG
        
        # BUG FIX
        secret = st.session_state.secret
```
<div>
<img src="./assets/backward_hints.png" style="width 16rem; height: 15rem;">
</div>
<a id="4">[4]</a>:

```bash
    def test_get_range_for_difficulty_normal():
        # On normal difficulty, the range should be from 1 to 50
        range = get_range_for_difficulty("Normal")
>       assert range == (1, 50)
E       assert (1, 100) == (1, 50)
E         
E         At index 1 diff: 100 != 50
E         Use -v to get more diff
```

Suspected bugs for inaccurate ranges for the selected difficulty, Normal

```bash
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
        ''' return statement immediately above, return 1, 100 is the bug. It should be, return 1, 50'''
    if difficulty == "Hard":
        return 1, 50
    return 1, 100
```

<a id="5">[5]</a>:

```bash
    def test_get_range_for_difficulty_hard():
        ''' On hard difficulty, the range should be from 1 to 100 '''
        range = get_range_for_difficulty("Hard")
>       assert range == (1, 100)
E       assert (1, 50) == (1, 100)
E         
E         At index 1 diff: 50 != 100
E         Use -v to get more diff
```

Suspected bugs for inaccurate ranges for the selected difficulty, Hard

```bash
  def get_range_for_difficulty(difficulty: str):
      """Return (low, high) inclusive range for a given difficulty."""
      if difficulty == "Easy":
          return 1, 20
      if difficulty == "Normal":
          return 1, 100
      if difficulty == "Hard":
          return 1, 50
          ''' return statement immediately above, return 1, 50 is the bug. It should be, return 1, 100'''
    return 1, 100
```
<a id="6">[6]</a>:
<br/>
<div>
<img src="./assets/mismatch_secret_range.png" style="width 16rem; height: 15rem;">
</div>
<br/>

Suspected bug for the secret being in a range outside of selected difficulty.

```bash
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
    ''' The conditional is the suspected bug. This code is in app.py '''
```
<a id="7">[7]</a>:
<br/>
<div>
<img src="./assets/blue_block.png">
</div>

```bash
# Test case for testing that the blue block gives the accurate range. Of course blue block also gives attempts left. This test case is in test_app.py

secret_range_in_main_panel_ui

```

Fix for this was replacing this line of code
`f"Guess a number between 1 and 100.` with this line of code, `f"Guess a number between {low} and {high}. "` in app.py file.

```bash
with attempts_display.container():
    st.info(
        # Another bug. 
        # f"Guess a number between 1 and 100. "
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
```

<br/>
<div>
<img src="./assets/blue_block_range_corrected.png">
</div>
<a id="8">[8]</a>:

Tests in test_app.py are suppose to test where secret changes based on difficulty or when user clicks a new game

```bash
test_changing_difficulty_starts_a_new_game_with_a_stable_secret

test_new_game_uses_active_range_and_changes_secret
```

<a id="9">[9]</a>:

Tests in test_app.py are suppose to test 
that number of attempts user has tried is shown as 0
in the UI upon first starting the game.

```bash
test_attempts_left_banner_reflects_the_attempt_limit_shown_in_sidebar_and_num_of_attempts_in_debug_info_expander_starts_at_zero
```

Suspected bug. 

```bash
if "attempts" not in st.session_state:
    st.session_state.attempts = 1
    # Now is 
    # st.session_state.attempts = 0
```

<a id="10">[10]</a>:

In test_game_logic.py file, which tests the logic_utils.py file.

```bash
def test_update_score_with_score_below_secret():
    # Testing wheher update_score with easy values such as 0,"Too High", and 8
    # Should returns an integer
    score = update_score(0, "Too High", 8)
    assert 5 == score

def test_update_score_with_score_higher_than_secret():
    # Testing wheher update_score with easy values such as 0,"Too High", and 8
    # Should returns an integer
    score = update_score(0, "Too Low", 8)
    assert -5 == score
```