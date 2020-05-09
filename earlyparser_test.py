# tests of parse correctness

from lexer import lex
from earlyparser import EarleyParser
from parseerror import ParseError
import pytest


def test_parse():
    tokens = list(lex("(1+2.4)*1e-2/(8-9)"))
    parser = EarleyParser(tokens)
    assert parser.parse() is not None

    tokens = list(lex("(1+2.4*1e-2/(8-9)"))
    parser = EarleyParser(tokens)
    assert parser.parse() is None

    tokens = list(lex("(1+2.4)1e-2/(8-9)"))
    parser = EarleyParser(tokens)
    assert parser.parse() is None
