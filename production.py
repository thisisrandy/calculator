from terminals import Terminals


class Production:
    def __init__(
        self,
        name,
        *expansion,
        pos=0,
        origin=0,
        children=None,
        eval_fn=lambda children: None,
    ):
        """
        :param name: the LHS of the production, a NonTerminal
        :param expansion: the RHS of the production, a sequence of Terminals
        and NonTerminals
        :param int pos: the current position
        :param int origin: the token position at which matching began
        :param children: a sequence of matched NonTerminals and Tokens
        (should not be manually specified)
        :param eval_fn: a function with param children which specifies the
        semantics of the production. must be specified in order for evaluate
        to work properly
        """
        self.name = name
        if len(expansion) < pos:
            raise Exception(
                "Productions must have expansions at least as long as the specified position"
            )
        self.expansion = expansion
        self.pos = pos
        self.origin = origin
        self.children = children if children else [None] * len(expansion)
        self.eval_fn = eval_fn

    def __eq__(self, other):
        """
        equality on name if other is a string, hash if Production, and false
        otherwise
        """
        return (
            self.name == other
            if isinstance(other, str)
            else hash(self) == hash(other)
            if isinstance(other, Production)
            else False
        )

    def __hash__(self):
        return hash((self.name, self.expansion, self.pos, self.origin))

    def __repr__(self):
        return (
            f"Name: {self.name}\nExpansion: {self.expansion}\n"
            f"Position: {self.pos} Origin: {self.origin}"
        )

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
        """
        create a copy with pos 0 and specified origin. children are NOT
        copied
        """
        return Production(
            self.name, *self.expansion, pos=0, origin=origin, eval_fn=self.eval_fn
        )

    def advance(self, matched_child):
        """
        create a copy of self with position advanced by one. in the copy,
        add matched_child to the children array
        """
        children = [
            matched_child if idx == self.pos else item
            for idx, item in enumerate(self.children)
        ]
        return Production(
            self.name,
            *self.expansion,
            pos=self.pos + 1,
            origin=self.origin,
            children=children,
            eval_fn=self.eval_fn,
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

    def evaluate(self):
        children = self.children
        if not all(children):
            raise Exception("Cannot evaluate until a full parse is available")
        return self.eval_fn(children)
