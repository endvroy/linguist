from nfa_to_dfa import *
from nfa import NFA
import unittest


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
        trans_matrix, starting_state, accepting_states = subset_cons(nfa)
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
        self.assertEqual(accepting_states, {d1, d2, d3})


if __name__ == '__main__':
    unittest.main()
