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
