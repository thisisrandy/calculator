# tests of calculation correctness

from lexer import lex
from earlyparser import EarleyParser
from parseerror import ParseError
import pytest


def test_calc():
    tokens = list(lex("80*8+1"))
    parser = EarleyParser(tokens)
    res = parser.parse()
    assert res.evaluate() == 641

    tokens = list(lex("(1+2.4)*1e-2/(8-9)"))
    parser = EarleyParser(tokens)
    res = parser.parse()
    assert res.evaluate() == -0.034
