# tests of lexer correctness

from lexer import lex
from parseerror import ParseError
import pytest


def test_lex():
    with pytest.raises(ParseError):
        list(lex("1+2f"))
    with pytest.raises(ParseError):
        list(lex("hello!"))
    with pytest.raises(ValueError):
        list(lex("1.1.1"))
    with pytest.raises(ValueError):
        list(lex("1e-1.2"))
    assert len(list(lex("(1+2.4)*1e-2/(8-9)"))) == 14
