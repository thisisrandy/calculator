from orderedset import OrderedSet
from defaultgrammar import DEFAULT_GRAMMAR


class EarleyParser:
    """
    implementation of
    https://en.wikipedia.org/wiki/Earley_parser#Pseudocode
    """

    def __init__(self, tokens, grammar=DEFAULT_GRAMMAR):
        """
        grammar is a tuple of Productions, where the first production is
        assumed to be the top level
        """
        self.tokens = tokens
        if len(grammar) == 0:
            raise Exception("grammar must contain at least one production")
        self.grammar = grammar

    def parse(self):
        """
        return a Production object containing a successful parse or None on
        failure. the returned object may be evaluated per its specified rules
        """
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

        return (
            S[len(tokens)].peek() if top_level.asComplete() in S[len(tokens)] else None
        )

    def _predictor(self, state, k):
        for rule in filter(lambda r: r.nameMatches(state.next()), self.grammar):
            self.S[k].add(rule.copy(k))

    def _scanner(self, state, k):
        tokens = self.tokens
        if state.nextMatches(tokens[k]):
            self.S[k + 1].add(state.advance(tokens[k]))

    def _completer(self, state, k):
        S = self.S
        for production in filter(lambda p: p.nextMatches(state.name), S[state.origin]):
            S[k].add(production.advance(state))
