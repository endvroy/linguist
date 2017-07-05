from scanner.nfa import *
from scanner.tests.auto_tests.test_nfa_to_dfa import build_test_nfa
from pprint import pprint


def build_nfa1():  # NFA on page 151 of the Dragon Book
    nfa = NFA()
    for i in range(4):
        nfa.add_state(i)
    nfa.add_transition(0, 0, 'b')
    nfa.add_transition(0, 1, 'a')
    nfa.add_transition(1, 1, 'a')
    nfa.add_transition(1, 2, 'b')
    nfa.add_transition(2, 1, 'a')
    nfa.add_transition(2, 3, 'b')
    nfa.add_transition(3, 0, 'b')
    nfa.add_transition(3, 1, 'a')
    nfa.mark_starting(0)
    nfa.mark_accepting(3, 0)
    return nfa


def test_cat():
    nfa1 = build_nfa1()
    nfa2 = build_test_nfa()
    cat_nfa = cat([nfa1, nfa2])
    pprint(cat_nfa.trans_matrix)
    print(cat_nfa.starting_state)
    print(cat_nfa.accepting_states)
    print(cat_nfa.alphabet)


def test_alt():
    nfa1 = build_nfa1()
    nfa2 = build_test_nfa()
    alt_nfa = alt([nfa1, nfa2])
    pprint(alt_nfa.trans_matrix)
    print(alt_nfa.starting_state)
    print(alt_nfa.accepting_states)
    print(alt_nfa.alphabet)


def test_closure():
    nfa = build_nfa1()
    c_nfa = closure(nfa)
    pprint(c_nfa.trans_matrix)
    print(c_nfa.starting_state)
    print(c_nfa.accepting_states)
    print(c_nfa.alphabet)
