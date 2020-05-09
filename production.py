from terminals import Terminals


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
