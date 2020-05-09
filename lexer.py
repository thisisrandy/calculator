import re
from terminals import Terminals


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __eq__(self, other):
        """equality by type, not value"""
        return self.type == other

    def __repr__(self):
        return f"{self.type} {self.value}"


class ParseError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def lex(expression):
    """
    :raise ParseError on encountering invalid character
    """
    accum = ""
    for char in expression:
        if re.match("\d", char):
            accum += char
        else:
            if len(accum) > 0:
                yield Token(Terminals.LITERAL, int(accum))
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
                raise Exception(f"Invalid character {char} in expression {expression}")
    if len(accum) > 0:
        yield Token(Terminals.LITERAL, int(accum))
    yield Token(Terminals.EOF)
