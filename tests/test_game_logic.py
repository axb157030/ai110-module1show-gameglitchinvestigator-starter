from logic_utils import check_guess
from logic_utils import get_range_for_difficulty
from logic_utils import parse_guess
from logic_utils import update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, hint = check_guess(50, 50)
    assert result == "Win"
    assert hint == "🎉 Correct!"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, hint = check_guess(60, 50)
    assert result == "Too High"
    assert hint == "📉 Go LOWER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, hint = check_guess(40, 50)
    assert result == "Too Low"
    assert hint == "📈 Go HIGHER!"
    

def test_get_range_for_difficulty_easy():
    # On easy difficulty, the range should be from 1 to 20
    range = get_range_for_difficulty("Easy")
    assert range == (1, 20)

def test_get_range_for_difficulty_easy_case_sensitivity():
    # On easy difficulty regardless of casing, the range should be from 1 to 20
    range = get_range_for_difficulty("easy")
    assert range == (1, 20)

def test_get_range_for_difficulty_normal():
    # On normal difficulty, the range should be from 1 to 50
    range = get_range_for_difficulty("Normal")
    assert range == (1, 50)

def test_get_range_for_difficulty_normal_and_case_sensitivity():
    # On normal difficulty regardless of casing, the range should be from 1 to 50
    range = get_range_for_difficulty("NoMaL")
    assert range == (1, 50)

def test_get_range_for_difficulty_hard():
    # On nhard difficulty, the range should be from 1 to 100
    range = get_range_for_difficulty("Hard")
    assert range == (1, 100)
def test_get_range_for_difficulty_hard_and_case_sensitivity():
    # On nhard difficulty regardless of casing, the range should be from 1 to 100
    range = get_range_for_difficulty("haRd")
    assert range == (1, 100)
def test_get_range_for_difficulty_invalid_difficulty():
    # On invalid difficulties, any difficulty that is not
    # case insensitive easy, normal, or hard, the range should be from 1 to 100
    range = get_range_for_difficulty("3562gv")
    assert range == (1, 100)

# Parse guess
def test_parse_guess_if_guess_is_none():
    # Parse guess when the guess is None
    guess_tuple = parse_guess(None)
    assert guess_tuple == (False, None, "Enter a guess.")
# Parse guess
def test_parse_guess_if_guess_is_empty_string():
    # Parse guess when the guess is an empty string
    guess_tuple = parse_guess("")
    assert guess_tuple == (False, None, "Enter a guess.")

def test_parse_guess_if_guess_is_just_spaces():
    # Parse guess when the guess is an empty string
    guess_tuple = parse_guess("     \t\n")
    assert guess_tuple == (False, None, "That is not a number.")

def test_parse_guess_if_guess_is_alphanumerical():
    # Parse guess when the guess has letters and numbers
    guess_tuple = parse_guess("4t8359g8j")
    assert guess_tuple == (False, None, "That is not a number.")

def test_parse_guess_if_guess_is_alphanumerical_and_has_spaces():
    # Parse guess when the guess has letters, numbers, and spaces
    guess_tuple = parse_guess("\t    4t8359g8j")
    assert guess_tuple == (False, None, "That is not a number.")


def test_parse_guess_if_guess_is_floating_number():
    # Parse guess correctly when the guess is a floating number
    # Floating number should be floored to an int of 5 or floating number is 5.5
    guess_tuple = parse_guess("5.5")
    assert guess_tuple == (True, 5, None)

def test_parse_guess_if_guess_is_integer():
    # Parse guess correctly when the guess is a floating number
    guess_tuple = parse_guess("5")
    assert guess_tuple == (True, 5, None)

def test_update_score_with_easy_values_to_check_whether_it_returns_an_integer():
    # Testing wheher update_score with easy values such as 0,"Too High", and 8
    # Should returns an integer
    score = update_score(0, "Too High", 8)
    print("^^^^",type(score))
    assert int == type(score)



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
