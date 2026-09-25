# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**
[1.](#1).  I asked Claude to make the content I added for reflection.md look better and read more smoothly.

[2.](#2).  I asked Claude to find a bug and fufill the documentation noting it in the reflection.md file

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**
[1.](#1). It regenerated the reflection.md file redoing its initial structure. I rejected that but decided to take some snippets of
content it generated for the reflection.md file when making the actual reflection.md file.

[2.](#2).  It completed a row in th Bug Reproduction Log in the reflextion.md file that provided information on a bug it found. The bug it found
  was the backward hints.
<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->
[1.](#1). It redid the structure of the reflections.md file. 
such as replacing some headers such as "- What did the game look like the first time you ran it?"

[2.](#2). I previous found the error it documented when I was playing with the application when it was running on a browser. It said to submit two guess to find the error. Two guesses were not needed. The results and hints came after submitted the first guess. I modified it
stating it needs only one guess and documented the same error but with different inputs
testing the application in the browser.
---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->
- I removed
```
        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret
```
and replaced it with just secret = st.session_state.secret. The change was suggested
by GitHub Copilot.
<!--I did get the GitHub Copilot suggestion but as of now, have not implemented it-->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->


<a id="1">[1]</a>: 
    - For task:
        - I asked Claude to make the content I added for reflection.md look better and read more smoothly.

<a id="2">[1]</a>: 
    - For task:
        - I asked Claude to find a bug and fufill the documentation noting it in the reflection.md file