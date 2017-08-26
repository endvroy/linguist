from linguist.base.scanner.minimize_dfa import minimize_dfa
from linguist.base.scanner.nfa_to_dfa import nfa_to_dfa
from linguist.base.scanner.scanner import CategoryInfo
from linguist.engine.bnf_parser import category_info
from linguist.engine.bnf_parser import name as name_nfa
from linguist.engine.re_parser import re_scanner, re_parser
from linguist.engine.partial_builder import PartialBuilder
from linguist.exceptions import LangBuildError, ScanError, ParseError

name_dfa = minimize_dfa(nfa_to_dfa(name_nfa, category_info))


def dfa_checker(dfa, text):
    state = dfa.starting_state
    for x in text:
        cls = dfa.classifier.classify(x)
        state = dfa.trans_matrix[state][cls]
        if state is None:
            return False
    if state in dfa.accepting_states:
        return True
    else:
        return False


class LangBuilder(PartialBuilder):
    def lex(self, name, pattern, skip=False):
        if not dfa_checker(name_dfa, name):
            raise LangBuildError(f'illegal name: {name}')
        else:
            if name in self.name_map:
                raise LangBuildError(f'conflict name {name}')

            category = len(self.category_info)
            self.name_map[name] = ('t', category)
            self.category_info.append(CategoryInfo(name, -category))
            try:
                tokens = re_scanner.tokens(pattern)
                nfa = re_parser.parse(tokens, category)
            except (ScanError, ParseError):
                raise LangBuildError

            self.nfa_list.append(nfa)

            if skip:
                self.category_info[category].action = 'skip'

                def wrapper(fn):
                    raise LangBuildError(f'cannot define action to skipped tokens {name}')
            else:
                def wrapper(fn):
                    self.category_info[category].action = fn
                    return fn

            return wrapper
