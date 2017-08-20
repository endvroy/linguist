from scanner.re_utils import atom, char_set, neg_set, char_range, dot, cat, alt, closure
from scanner.scanner import CategoryInfo, scanner_builder

category_info = {1: CategoryInfo('LPAREN', -1),
                 2: CategoryInfo('RPAREN', -2),
                 3: CategoryInfo('LBRACKET', -3),
                 4: CategoryInfo('RBRACKET', -4),
                 5: CategoryInfo('STAR', -5),
                 6: CategoryInfo('PLUS', -6),
                 7: CategoryInfo('QMARK', -7),
                 8: CategoryInfo('BSLASH', -8),
                 9: CategoryInfo('ALT_DELIM', -9),
                 10: CategoryInfo('CARET', -10),
                 11: CategoryInfo('DASH', -11),
                 12: CategoryInfo('DOT', -12),
                 13: CategoryInfo('NOT_RESERVED', -13),
                 }

lparen = atom('(', 1)
rparen = atom(')', 2)
lbracket = atom('[', 3)
rbracket = atom(']', 4)
star = atom('*', 5)
plus = atom('+', 6)
qmark = atom('?', 7)
bslash = atom('\\', 8)
alt_delim = atom('|', 9)
caret = atom('^', 10)
dash = atom('-', 11)
dot_ = atom('.', 12)
not_reserved = dot(13)

nfa = alt([lparen,
           rparen,
           lbracket,
           rbracket,
           star,
           plus,
           qmark,
           bslash,
           alt_delim,
           caret,
           dash,
           dot_,
           not_reserved])

scanner = scanner_builder(nfa, category_info)
