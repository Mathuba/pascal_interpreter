import pytest

from part1.calc1 import *


@pytest.mark.parametrize(
    "token_type,value,expected",
    [
        (INTEGER, 0, "Token(INTEGER, 0)"),
        (INTEGER, 9, "Token(INTEGER, 9)"),
        (PLUS, "+", "Token(PLUS, '+')"),
        (EOF, None, "Token(EOF, None)"),
    ],
)
def test_token_multiple_values(token_type, value, expected):
    """Test token creation with multiple values using parametrize."""
    token = Token(token_type, value)
    assert token.type == token_type
    assert token.value == value
    assert str(token) == expected


def test_interpreter_initialization():
    """Test Interpreter initialization."""
    interpreter = Interpreter("3+5")
    assert interpreter.text == "3+5"
    assert interpreter.pos == 0
    assert interpreter.current_token is None


# Tests for get_next_token method
def test_get_next_token_integer():
    """Test getting an INTEGER token."""
    interpreter = Interpreter("3")
    token = interpreter.get_next_token()
    assert token.type == INTEGER
    assert token.value == 3
    assert interpreter.pos == 1


def test_get_next_token_plus():
    """Test getting a PLUS token."""
    interpreter = Interpreter("+")
    token = interpreter.get_next_token()
    assert token.type == PLUS
    assert token.value == "+"
    assert interpreter.pos == 1


def test_get_next_token_eof():
    """Test getting an EOF token when past end of input."""
    interpreter = Interpreter("3")
    interpreter.pos = 1  # Move past the end
    token = interpreter.get_next_token()
    assert token.type == EOF
    assert token.value is None


def test_get_next_token_sequence():
    """Test getting multiple tokens in sequence."""
    interpreter = Interpreter("3+5")

    token1 = interpreter.get_next_token()
    assert token1.type == INTEGER
    assert token1.value == 3

    token2 = interpreter.get_next_token()
    assert token2.type == PLUS
    assert token2.value == "+"

    token3 = interpreter.get_next_token()
    assert token3.type == INTEGER
    assert token3.value == 5

    token4 = interpreter.get_next_token()
    assert token4.type == EOF


def test_get_next_token_invalid_character():
    """Test error handling for invalid character."""
    interpreter = Interpreter("3&5")
    interpreter.get_next_token()  # Get first token (3)
    with pytest.raises(Exception, match="Error parsing input"):
        interpreter.get_next_token()  # Should fail on '&'

    # Tests for eat method


def test_eat_matching_token():
    """Test eat method with matching token type."""
    interpreter = Interpreter("3+5")
    interpreter.current_token = interpreter.get_next_token()  # INTEGER token
    assert interpreter.current_token.type == INTEGER

    interpreter.eat(INTEGER)
    assert interpreter.current_token.type == PLUS


def test_eat_non_matching_token():
    """Test eat method with non-matching token type."""
    interpreter = Interpreter("3+5")
    interpreter.current_token = interpreter.get_next_token()  # INTEGER token

    with pytest.raises(Exception, match="Error parsing input"):
        interpreter.eat(PLUS)  # Expecting PLUS but got INTEGER


# Tests for expr method
def test_expr_simple_addition():
    """Test expr method with simple addition."""
    interpreter = Interpreter("3+5")
    result = interpreter.expr()
    assert result == 8


def test_expr_zero_plus_zero():
    """Test expr with 0+0."""
    interpreter = Interpreter("0+0")
    result = interpreter.expr()
    assert result == 0


def test_expr_nine_plus_one():
    """Test expr with 9+1."""
    interpreter = Interpreter("9+1")
    result = interpreter.expr()
    assert result == 10


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("1+2", 3),
        ("5+5", 10),
        ("0+9", 9),
        ("7+2", 9),
    ],
)
def test_expr_multiple_inputs(input_str, expected):
    """Test expr with multiple input combinations."""
    interpreter = Interpreter(input_str)
    result = interpreter.expr()
    assert result == expected


def test_expr_missing_left_operand():
    """Test expr with missing left operand."""
    interpreter = Interpreter("+5")
    with pytest.raises(Exception, match="Error parsing input"):
        interpreter.expr()


def test_expr_missing_operator():
    """Test expr with missing operator."""
    interpreter = Interpreter("35")
    with pytest.raises(Exception, match="Error parsing input"):
        interpreter.expr()
