# %%
from enum import Enum, auto
import re
from terminals import Terminals
from nonterminals import NonTerminals
from lexer import lex
from production import Production
from earlyparser import EarleyParser

# %%
tokens = list(lex("1+2*(3/4-1.0)+13e-2"))
parser = EarleyParser(tokens)
res = parser.parse()
if res:
    print(res.evaluate())
