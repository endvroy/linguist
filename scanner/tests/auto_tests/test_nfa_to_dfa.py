import unittest

from scanner.dfa import CategoryInfo
from scanner.nfa import NFA
from scanner.nfa_to_dfa import *


def build_test_nfa():  # example NFA on page 51
    nfa = NFA()
    for i in range(10):
        nfa.add_state(i)
    nfa.mark_starting(0)
    nfa.mark_accepting(9, 1)

    nfa.add_transition(0, 1, 'a')
    nfa.add_transition(1, 2, nfa.epsilon)
    nfa.add_transition(2, 9, nfa.epsilon)
    nfa.add_transition(2, 3, nfa.epsilon)
    nfa.add_transition(3, 4, nfa.epsilon)
    nfa.add_transition(3, 6, nfa.epsilon)
    nfa.add_transition(4, 5, 'b')
    nfa.add_transition(5, 8, nfa.epsilon)
    nfa.add_transition(6, 7, 'c')
    nfa.add_transition(7, 8, nfa.epsilon)
    nfa.add_transition(8, 3, nfa.epsilon)
    nfa.add_transition(8, 9, nfa.epsilon)

    return nfa


class TestSubsetConstruction(unittest.TestCase):
    def test_eps_closure(self):
        nfa = build_test_nfa()
        self.assertEqual(epsilon_closure(nfa, {0}), {0})
        self.assertEqual(epsilon_closure(nfa, nfa.trans_matrix[0]['a']), {1, 2, 3, 4, 6, 9})
        self.assertEqual(epsilon_closure(nfa, nfa.trans_matrix[0]['b']), set())
        self.assertEqual(epsilon_closure(nfa, nfa.trans_matrix[0]['c']), set())

    def test_next_set(self):
        nfa = build_test_nfa()
        self.assertEqual(next_set(nfa, {1, 2, 3, 4, 6, 9}, 'a'), set())
        self.assertEqual(next_set(nfa, {1, 2, 3, 4, 6, 9}, 'b'), {5})
        self.assertEqual(next_set(nfa, {1, 2, 3, 4, 6, 9}, 'c'), {7})

    def test_next_closure(self):
        nfa = build_test_nfa()
        self.assertEqual(epsilon_closure(nfa, next_set(nfa, {1, 2, 3, 4, 6, 9}, 'a')), set())
        self.assertEqual(epsilon_closure(nfa, next_set(nfa, {1, 2, 3, 4, 6, 9}, 'b')),
                         {5, 8, 9, 3, 4, 6})
        self.assertEqual(epsilon_closure(nfa, next_set(nfa, {1, 2, 3, 4, 6, 9}, 'c')),
                         {7, 8, 9, 3, 4, 6})

    def test_subset_cons(self):
        nfa = build_test_nfa()
        trans_matrix, starting_state, accepting_states = subset_cons(nfa, {1: CategoryInfo('dummy', 0)})
        d0 = frozenset({0})
        d1 = frozenset({1, 2, 3, 4, 6, 9})
        d2 = frozenset({5, 8, 9, 3, 4, 6})
        d3 = frozenset({7, 8, 9, 3, 4, 6})
        self.assertEqual(trans_matrix,
                         {d0: {'a': d1},
                          d1: {'b': d2,
                               'c': d3},
                          d2: {'b': d2,
                               'c': d3},
                          d3: {'b': d2,
                               'c': d3}})
        self.assertEqual(starting_state, d0)
        self.assertEqual(accepting_states, {d1: 1,
                                            d2: 1,
                                            d3: 1})

    def test_ambiguous_subcons(self):
        nfa = NFA()
        for i in range(1, 7):
            nfa.add_state(i)
        nfa.add_transition(1, 2, 'i')
        nfa.add_transition(2, 3, 'f')
        nfa.add_transition(1, 4, 'i')
        nfa.add_transition(1, 5, 'a')
        nfa.add_transition(1, 6, 'f')
        for i in range(4, 7):
            for char in 'iaf':
                nfa.add_transition(i, i, char)
        nfa.mark_starting(1)
        nfa.mark_accepting(3, 'if')  # if
        for i in range(4, 7):
            nfa.mark_accepting(i, 'id')  # id

        trans_matrix, starting_state, accepting_states = subset_cons(nfa, {'if': CategoryInfo('IF', 0),
                                                                           'id': CategoryInfo('ID', -1)})
        d1 = frozenset({1})
        d2 = frozenset({2, 4})
        d3 = frozenset({3, 4})
        d4 = frozenset({4})
        d5 = frozenset({5})
        d6 = frozenset({6})
        self.assertEqual(trans_matrix,
                         {d1: {'a': d5,
                               'i': d2,
                               'f': d6},
                          d2: {'a': d4,
                               'i': d4,
                               'f': d3},
                          d3: {'a': d4,
                               'i': d4,
                               'f': d4},
                          d4: {'a': d4,
                               'i': d4,
                               'f': d4},
                          d5: {'a': d5,
                               'i': d5,
                               'f': d5},
                          d6: {'a': d6,
                               'i': d6,
                               'f': d6},
                          })
        self.assertEqual(starting_state, d1)
        self.assertEqual(accepting_states, {d2: 'id',
                                            d3: 'if',
                                            d4: 'id',
                                            d5: 'id',
                                            d6: 'id'})


if __name__ == '__main__':
    unittest.main()
