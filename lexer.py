import re
from terminals import Terminals
from parseerror import ParseError


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __eq__(self, other):
        """equality by type, not value"""
        return self.type == other

    def __repr__(self):
        return f"{self.type} {self.value}"


def lex(expression):
    """
    :raise ParseError on encountering invalid character
    :raise ValueError on invalid float
    """
    accum = ""
    for char in expression:
        if (
            re.match("[\d.e]", char)
            or len(accum)
            and accum[-1] == "e"
            and re.match("[+-]", char)
        ):
            accum += char
        else:
            if len(accum) > 0:
                yield Token(Terminals.LITERAL, float(accum))
                accum = ""
            if re.match("\s", char):
                continue
            try:
                type = {
                    "+": Terminals.PLUS,
                    "-": Terminals.MINUS,
                    "*": Terminals.MULT,
                    "/": Terminals.DIV,
                    "(": Terminals.RPAREN,
                    ")": Terminals.LPAREN,
                }[char]
                yield Token(type, char)
            except:
                raise ParseError(f"Invalid character {char} in expression {expression}")
    if len(accum) > 0:
        yield Token(Terminals.LITERAL, float(accum))
    yield Token(Terminals.EOF)
