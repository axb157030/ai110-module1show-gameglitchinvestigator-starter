# Docstring added by Claude Pro

def get_range_for_difficulty(difficulty: str):
    """Return the inclusive ``(low, high)`` guessing range for a difficulty.

    Args:
        difficulty: Difficulty name. Matched case-insensitively against
            ``"easy"`` and ``"normal"``; any other value falls through to the
            default range.

    Returns:
        tuple[int, int]: The inclusive ``(low, high)`` bounds.

    Raises:
        AttributeError: If ``difficulty`` is not a string, since ``.lower()``
            is called on it unguarded -- notably when it is ``None``.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("normal")
        (1, 50)
        >>> get_range_for_difficulty("Hard")
        (1, 100)
        >>> get_range_for_difficulty("bogus")
        (1, 100)

    Note:
        The ``"hard "`` comparison carries a trailing space, so it can never
        match ``difficulty.lower()``; ``"Hard"`` reaches the default ``return``
        instead. Both paths yield ``(1, 100)``, so the branch is unreachable
        rather than visibly wrong -- but Hard's range is not defined where it
        appears to be. Note also that Hard (1-100) is wider than Normal (1-50)
        while allowing fewer attempts (5 vs 8) in ``app.py``.
    """
    if difficulty.lower() == "easy":
        return 1, 20
    if difficulty.lower() == "normal":
        return 1, 50
    if difficulty.lower() == "hard ":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
    """Parse raw user input into an integer guess.

    Args:
        raw: Text entered by the player. ``None`` and ``""`` are both treated
            as "nothing entered".

    Returns:
        tuple[bool, int | None, str | None]: ``(ok, guess, error)``. On success,
        ``(True, <int>, None)``; on failure, ``(False, None, <message>)``.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("")
        (False, None, 'Enter a guess.')
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')

    Note:
        Decimal input is truncated toward zero rather than rejected or rounded,
        so a guess of ``"3.9"`` is played as ``3``:

        >>> parse_guess("3.9")
        (True, 3, None)

        Because conversion defers to ``int()``, surrounding whitespace, a
        leading sign and PEP 515 underscore separators are all accepted, while
        scientific notation is not:

        >>> parse_guess(" 42 ")
        (True, 42, None)
        >>> parse_guess("1_0")
        (True, 10, None)
        >>> parse_guess("1e3")
        (False, None, 'That is not a number.')

        No range check is performed, so zero and negative numbers parse
        successfully and are passed on to :func:`check_guess`.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess against the secret and return an outcome and a hint.

    Both arguments are normalised first: a ``str`` is stripped of surrounding
    whitespace and converted to ``int`` when it consists only of digits. This
    lets the comparison stay numeric when the caller supplies the secret as a
    string, as ``app.py`` does on even-numbered attempts.

    Args:
        guess: The player's guess, as an ``int`` or a digit-only ``str``.
        secret: The number to be found, as an ``int`` or a digit-only ``str``.

    Returns:
        tuple[str, str]: ``(outcome, message)``, where ``outcome`` is one of
        ``"Win"``, ``"Too High"`` or ``"Too Low"`` and ``message`` is the
        player-facing hint.

    Raises:
        TypeError: If one argument is an ``int`` and the other is a ``str``
            that ``str.isdigit`` rejects -- a negative number, a decimal, or an
            empty string. Coercion is skipped for such a value, the numeric
            comparison fails, and the ``except TypeError`` branch then compares
            a ``str`` against an ``int`` and raises again, uncaught.
        ValueError: If a ``str`` argument satisfies ``str.isdigit`` but is not
            accepted by ``int``, such as the superscript ``"²"``.

    Examples:
        >>> check_guess(50, 50)[0]
        'Win'
        >>> check_guess(60, 50)[0]
        'Too High'
        >>> check_guess(40, 50)[0]
        'Too Low'

        A ``str`` on either side is accepted, and numeric order is preserved:

        >>> check_guess(9, "50")[0]
        'Too Low'
        >>> check_guess(100, "50")[0]
        'Too High'
        >>> check_guess(" 60 ", 50)[0]
        'Too High'

    Note:
        ``str.isdigit`` accepts non-ASCII digits, so the Arabic-Indic five
        ``"٥"`` is coerced to ``5`` and compares numerically.

        The ``except TypeError`` branch is now reachable only when ``guess`` is
        an ``int`` and ``secret`` is a non-numeric ``str``. It compares the two
        lexicographically rather than numerically, so its verdict is not
        meaningful:

        >>> check_guess(50, "abc")[0]
        'Too Low'
    """
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

def update_score(current_score: int, outcome: str, attempt_number: int):
    """Apply the score change for a single guess outcome.

    Args:
        current_score: The score before this guess.
        outcome: An outcome from :func:`check_guess` -- ``"Win"``,
            ``"Too High"`` or ``"Too Low"``. Any other value leaves the score
            unchanged.
        attempt_number: The attempt counter at the time of the guess.

    Returns:
        int: The updated score.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(0, "Too Low", 1)
        -5
        >>> update_score(100, "Bogus", 1)
        100

    Note:
        Win points are ``100 - 10 * (attempt_number + 1)``, floored at 10. The
        ``+ 1`` means a first-attempt win scores 80 rather than 90, and the
        floor is reached from attempt 8 onward:

        >>> [update_score(0, "Win", n) for n in (1, 2, 8, 20)]
        [80, 70, 10, 10]

        ``"Too High"`` depends on the parity of ``attempt_number``, awarding
        ``+5`` on even attempts and ``-5`` on odd ones, whereas ``"Too Low"``
        always costs ``-5``:

        >>> [update_score(0, "Too High", n) for n in (1, 2, 3, 4)]
        [-5, 5, -5, 5]
        >>> [update_score(0, "Too Low", n) for n in (1, 2, 3, 4)]
        [-5, -5, -5, -5]
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

