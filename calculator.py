# %%
from enum import Enum, auto
import re
from terminals import Terminals
from nonterminals import NonTerminals
from lexer import lex
from production import Production
from earlyparser import EarleyParser

# %%
tokens = list(lex("1+2*(3/4-1)"))
parser = EarleyParser(tokens)
res = parser.parse()
if res:
    print(res.evaluate())

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
