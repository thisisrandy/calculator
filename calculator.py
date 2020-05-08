# %%
from enum import Enum, auto
import re
from orderedset import OrderedSet
from terminals import Terminals
from nonterminals import NonTerminals
from lexer import lex
from production import Production

# %%
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


class EarleyParser:
    """
    implementation of
    https://en.wikipedia.org/wiki/Earley_parser#Pseudocode
    """

    def __init__(self, tokens, grammar=GRAMMAR):
        """
        grammar is a tuple of Productions, where the first production is
        assumed to be the top level
        """
        self.tokens = tokens
        if len(grammar) == 0:
            raise Exception("grammar must contain at least one production")
        self.grammar = grammar

    def parse(self):
        tokens = self.tokens
        top_level = self.grammar[0]
        S = self.S = [OrderedSet() for _ in range(len(tokens) + 1)]
        S[0].add(top_level)

        for k in range(len(tokens) + 1):
            while S[k].hasNext():
                state = S[k].next()
                if not state.isComplete():
                    if not state.isNextTerminal():
                        self._predictor(state, k)
                    else:
                        self._scanner(state, k)
                else:
                    self._completer(state, k)

        return top_level.asComplete() in S[len(tokens)]

    def _predictor(self, state, k):
        for rule in filter(lambda r: r.nameMatches(state.next()), self.grammar):
            self.S[k].add(rule.copy(k))

    def _scanner(self, state, k):
        if state.nextMatches(self.tokens[k]):
            self.S[k + 1].add(state.advance())

    def _completer(self, state, k):
        S = self.S
        for production in filter(lambda p: p.nextMatches(state.name), S[state.origin]):
            S[k].add(production.advance())


# %%
tokens = list(lex("1+2*3/4"))
parser = EarleyParser(tokens)
print(parser.parse())

# %%
class AST:
    class Node:
        def __init__(self, symbol, parent=None, child_left=None, child_right=None):
            self.symbol = symbol
            self.parent = parent
            self.child_left = child_left
            self.child_right = child_right

    def __init__(self, expression):
        """
        see https://en.wikipedia.org/wiki/Earley_parser#Pseudocode

        parsing:
        - try to match current token to left-most unmatched node
        - if we succeed, advance to next token
        - otherwise
            - if the rightmost node is not a terminal, expand it and try again
            - if the rightmost node is a terminal, back up until an alternate
            expansion is found, or fail

        the stack:

        """
        self.root = AST.Node(NonTerminals.GOAL)
