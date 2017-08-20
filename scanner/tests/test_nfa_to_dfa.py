import unittest

from scanner.tests.tools import build_test_nfa, draw_dfa
from scanner.nfa import NFA
from scanner.scanner import CategoryInfo
from scanner.nfa_to_dfa import *


class TestSubsetConstruction(unittest.TestCase):
    def test_eps_closure(self):
        nfa = build_test_nfa()
        self.assertEqual(epsilon_closure(nfa, {0}), {0})
        self.assertEqual({1, 2, 3, 4, 6, 9}, epsilon_closure(nfa, nfa.trans_matrix[0][nfa.classifier.classify('a')]))
        self.assertEqual(set(), epsilon_closure(nfa, nfa.trans_matrix[0][nfa.classifier.classify('b')]))
        self.assertEqual(set(), epsilon_closure(nfa, nfa.trans_matrix[0]['c']))

    def test_next_set(self):
        nfa = build_test_nfa()
        self.assertEqual(set(), next_set(nfa, {1, 2, 3, 4, 6, 9}, nfa.classifier.classify('a')))
        self.assertEqual({5}, next_set(nfa, {1, 2, 3, 4, 6, 9}, nfa.classifier.classify('b')))
        self.assertEqual({7}, next_set(nfa, {1, 2, 3, 4, 6, 9}, nfa.classifier.classify('c')))

    def test_next_closure(self):
        nfa = build_test_nfa()
        self.assertEqual(epsilon_closure(nfa, next_set(nfa, {1, 2, 3, 4, 6, 9}, nfa.classifier.classify('a'))), set())
        self.assertEqual(epsilon_closure(nfa, next_set(nfa, {1, 2, 3, 4, 6, 9}, nfa.classifier.classify('b'))),
                         {5, 8, 9, 3, 4, 6})
        self.assertEqual(epsilon_closure(nfa, next_set(nfa, {1, 2, 3, 4, 6, 9}, nfa.classifier.classify('c'))),
                         {7, 8, 9, 3, 4, 6})

    def test_subset_cons(self):
        nfa = build_test_nfa()
        trans_matrix, starting_state, accepting_states = subset_cons(nfa, {1: CategoryInfo('dummy', 0)})
        d0 = frozenset({0})
        d1 = frozenset({1, 2, 3, 4, 6, 9})
        d2 = frozenset({5, 8, 9, 3, 4, 6})
        d3 = frozenset({7, 8, 9, 3, 4, 6})
        self.assertEqual(trans_matrix,
                         {d0: {1: d1},
                          d1: {2: d2,
                               3: d3},
                          d2: {2: d2,
                               3: d3},
                          d3: {2: d2,
                               3: d3}})
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

    def test_nfa_to_dfa(self):
        nfa = build_test_nfa()
        dfa = nfa_to_dfa(nfa, {1: CategoryInfo('dummy', 0)})
        draw_dfa(dfa, 'nfa_to_dfa')


if __name__ == '__main__':
    unittest.main()
