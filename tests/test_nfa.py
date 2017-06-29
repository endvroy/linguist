from nfa import NFA
import unittest


class TestAddState(unittest.TestCase):
    def test_add_state(self):
        nfa = NFA()
        nfa.add_state(1)
        self.assertEqual(nfa.trans_matrix[1]['x'], set())
        self.assertFalse(nfa.accepting_states)
        self.assertEqual(nfa.starting_state, None)

    def test_add_accepting_states(self):
        nfa = NFA()
        nfa.add_state(1)
        nfa.add_state(2, accepting=True)
        nfa.add_state(3, accepting=True)
        nfa.add_state(4)
        self.assertEqual(nfa.accepting_states, {2, 3})

    def test_duplicate_states(self):
        nfa = NFA()
        nfa.add_state(1)
        with self.assertRaises(ValueError):
            nfa.add_state(1)

    def test_add_starting_states(self):
        nfa = NFA()
        nfa.add_state(1, starting=True)
        self.assertEqual(nfa.starting_state, 1)
        with self.assertRaises(ValueError):
            nfa.add_state(2, starting=True)


class TestAddTransition(unittest.TestCase):
    def test_add_trans(self):
        nfa = NFA()
        for x in [1, 2, 3]:
            nfa.add_state(x)
        nfa.add_transition(1, 3, 'x')
        self.assertEqual(nfa.trans_matrix[1]['x'], {3})
        self.assertEqual(nfa.trans_matrix[1][nfa.epsilon], set())
        self.assertEqual(nfa.alphabet, {'x'})  # add transition updates alphabet
        nfa.add_transition(1, 2, 'x')
        self.assertEqual(nfa.trans_matrix[1]['x'], {2, 3})
        nfa.add_transition(1, 3, 'x')  # duplicate transition ignored
        self.assertEqual(nfa.trans_matrix[1]['x'], {2, 3})
        self.assertEqual(nfa.alphabet, {'x'})
        nfa.add_transition(1, 2, nfa.epsilon)  # epsilon transition
        self.assertEqual(nfa.trans_matrix[1][nfa.epsilon], {2})
        self.assertEqual(nfa.alphabet, {'x'})  # epsilon not in alphabet
        nfa.add_transition(2, 2, 'y')  # self-loop
        self.assertEqual(nfa.trans_matrix[2]['y'], {2})
        self.assertEqual(nfa.alphabet, {'x', 'y'})


def build_test_nfa():  # example NFA on page 51
    nfa = NFA()
    for i in range(1, 9):
        nfa.add_state(i)
    nfa.add_state(0, starting=True)
    nfa.add_state(9, accepting=True)

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
        self.assertEqual(nfa.epsilon_closure({0}), {0})
        self.assertEqual(nfa.epsilon_closure(nfa.trans_matrix[0]['a']), {1, 2, 3, 4, 6, 9})
        self.assertEqual(nfa.epsilon_closure(nfa.trans_matrix[0]['b']), set())
        self.assertEqual(nfa.epsilon_closure(nfa.trans_matrix[0]['c']), set())

    def test_next_set(self):
        nfa = build_test_nfa()
        self.assertEqual(nfa._next_set({1, 2, 3, 4, 6, 9}, 'a'), set())
        self.assertEqual(nfa._next_set({1, 2, 3, 4, 6, 9}, 'b'), {5})
        self.assertEqual(nfa._next_set({1, 2, 3, 4, 6, 9}, 'c'), {7})

    def test_next_closure(self):
        nfa = build_test_nfa()
        self.assertEqual(nfa.epsilon_closure(nfa._next_set({1, 2, 3, 4, 6, 9}, 'a')), set())
        self.assertEqual(nfa.epsilon_closure(nfa._next_set({1, 2, 3, 4, 6, 9}, 'b')),
                         {5, 8, 9, 3, 4, 6})
        self.assertEqual(nfa.epsilon_closure(nfa._next_set({1, 2, 3, 4, 6, 9}, 'c')),
                         {7, 8, 9, 3, 4, 6})

    def test_to_dfa(self):
        nfa = build_test_nfa()
        trans_matrix, accepting_states = nfa.to_dfa()
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
        self.assertEqual(accepting_states, {d1, d2, d3})


if __name__ == '__main__':
    unittest.main()
