from terminals import Terminals
from nonterminals import NonTerminals
from production import Production

"""
The grammar:
    goal -> expr eof
    expr -> expr + term | expr - term | term
    term -> term * factor | term / factor | factor
    factor -> literal | ( expr )
"""
GRAMMAR = (
    Production(NonTerminals.GOAL, NonTerminals.EXPR, Terminals.EOF),
    Production(NonTerminals.EXPR, NonTerminals.EXPR, Terminals.PLUS, NonTerminals.TERM),
    Production(
        NonTerminals.EXPR, NonTerminals.EXPR, Terminals.MINUS, NonTerminals.TERM
    ),
    Production(NonTerminals.EXPR, NonTerminals.TERM),
    Production(
        NonTerminals.TERM, NonTerminals.TERM, Terminals.MULT, NonTerminals.FACTOR
    ),
    Production(
        NonTerminals.TERM, NonTerminals.TERM, Terminals.DIV, NonTerminals.FACTOR
    ),
    Production(NonTerminals.TERM, NonTerminals.FACTOR),
    Production(NonTerminals.FACTOR, Terminals.LITERAL),
    Production(
        NonTerminals.FACTOR, Terminals.RPAREN, NonTerminals.EXPR, Terminals.LPAREN
    ),
)
