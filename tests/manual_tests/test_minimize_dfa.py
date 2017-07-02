from minimize_dfa import *
from tests.auto_tests.test_minimize_dfa import build_test_dfa
from pprint import pprint


def test_minimize():
    dfa = build_test_dfa()
    min_dfa = minimize_dfa(dfa)
    pprint(min_dfa.trans_matrix)
    print(min_dfa.starting_state)
    print(min_dfa.accepting_states)
    print(min_dfa.alphabet)
