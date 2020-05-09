from terminals import Terminals
from nonterminals import NonTerminals
from production import Production

"""
Calculator grammar:
    goal -> expr eof
    expr -> expr + term | expr - term | term
    term -> term * factor | term / factor | factor
    factor -> literal | ( expr )
"""
DEFAULT_GRAMMAR = (
    Production(
        NonTerminals.GOAL,
        NonTerminals.EXPR,
        Terminals.EOF,
        eval_fn=lambda c: c[0].evaluate(),
    ),
    Production(
        NonTerminals.EXPR,
        NonTerminals.EXPR,
        Terminals.PLUS,
        NonTerminals.TERM,
        eval_fn=lambda c: c[0].evaluate() + c[2].evaluate(),
    ),
    Production(
        NonTerminals.EXPR,
        NonTerminals.EXPR,
        Terminals.MINUS,
        NonTerminals.TERM,
        eval_fn=lambda c: c[0].evaluate() - c[2].evaluate(),
    ),
    Production(
        NonTerminals.EXPR, NonTerminals.TERM, eval_fn=lambda c: c[0].evaluate(),
    ),
    Production(
        NonTerminals.TERM,
        NonTerminals.TERM,
        Terminals.MULT,
        NonTerminals.FACTOR,
        eval_fn=lambda c: c[0].evaluate() * c[2].evaluate(),
    ),
    Production(
        NonTerminals.TERM,
        NonTerminals.TERM,
        Terminals.DIV,
        NonTerminals.FACTOR,
        eval_fn=lambda c: c[0].evaluate() / c[2].evaluate(),
    ),
    Production(
        NonTerminals.TERM, NonTerminals.FACTOR, eval_fn=lambda c: c[0].evaluate(),
    ),
    Production(NonTerminals.FACTOR, Terminals.LITERAL, eval_fn=lambda c: c[0].value,),
    Production(
        NonTerminals.FACTOR,
        Terminals.RPAREN,
        NonTerminals.EXPR,
        Terminals.LPAREN,
        eval_fn=lambda c: c[1].evaluate(),
    ),
)
