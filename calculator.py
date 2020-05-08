# %%
from enum import Enum, auto
import re
from OrderedSet import OrderedSet

# %%
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __eq__(self, other):
        """equality by type, not value"""
        return self.type == other

    def __repr__(self):
        return f"{self.type} {self.value}"


class Terminals(Enum):
    PLUS = auto()
    MINUS = auto()
    MULT = auto()
    DIV = auto()
    RPAREN = auto()
    LPAREN = auto()
    LITERAL = auto()
    EOF = auto()


def lex(expression):
    accum = ""
    for char in expression:
        if re.match("\d", char):
            accum += char
        else:
            if len(accum) > 0:
                yield Token(Terminals.LITERAL, accum)
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
        yield Token(Terminals.LITERAL, accum)
    yield Token(Terminals.EOF)


# %%
class NonTerminals(Enum):
    GOAL = auto()
    EXPR = auto()
    TERM = auto()
    FACTOR = auto()


class Production:
    def __init__(self, name, *expansion, pos=0, origin=0):
        self.name = name
        if len(expansion) < pos:
            raise Exception(
                "Productions must have expansions at least as long as the specified position"
            )
        self.expansion = expansion
        self.pos = pos
        self.origin = origin

    def __eq__(self, other):
        """ equality on name if other is a string """
        return (
            self.name == other
            if isinstance(other, str)
            else self.name == other.name and self.expansion == other.expansion
            if isinstance(other, Production)
            else False
        )

    def __hash__(self):
        return hash((self.name, self.expansion, self.pos, self.origin))

    def __repr__(self):
        return f"Name: {self.name}\nExpansion: {self.expansion}\nPosition: {self.pos} Origin: {self.origin}"

    def nameMatches(self, symbol):
        """ check if name (LHS) matches symbol """
        return self.name == symbol

    def nextMatches(self, symbol):
        """ check if symbol is in the next position """
        return self.expansion[self.pos] == symbol

    def next(self):
        """ get the symbol in the next position """
        return self.expansion[self.pos]

    def isNextTerminal(self):
        return isinstance(self.expansion[self.pos], Terminals)

    def copy(self, origin):
        """ create a copy with pos 0 and specified origin """
        return Production(self.name, *self.expansion, pos=0, origin=origin)

    def advance(self):
        """ create a copy of self with position advanced by one """
        return Production(
            self.name, *self.expansion, pos=self.pos + 1, origin=self.origin
        )

    def isComplete(self):
        return self.pos == len(self.expansion)

    def asComplete(self):
        """
        create a copy with position at end. useful for checking if top
        level was in end state
        """
        return Production(
            self.name, *self.expansion, pos=len(self.expansion), origin=self.origin
        )


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
