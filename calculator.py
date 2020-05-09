if __name__ == "__main__":
    from enum import Enum, auto
    import re
    from terminals import Terminals
    from nonterminals import NonTerminals
    from lexer import lex
    from production import Production
    from earlyparser import EarleyParser
    from parseerror import ParseError
    import signal
    import sys

    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))

    while True:
        try:
            user_input = input("Enter an expression: ")
            tokens = list(lex(user_input))
            parser = EarleyParser(tokens)
            res = parser.parse()
            if not res:
                raise ParseError(f"Unable to parse {user_input}")
            print(f"Result: {res.evaluate()}")
        except EOFError:
            sys.exit(0)
        except Exception as e:
            print(e)
