from enum import Enum, auto


class Terminals(Enum):
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    RPAREN = auto()
    LPAREN = auto()
    LITERAL = auto()
    EOF = auto()
