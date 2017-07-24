import unittest

from scanner.nfa import *
from scanner.tests.tools import build_test_nfa, build_nfa1, draw_nfa


class TestAddState(unittest.TestCase):
    def test_add_state(self):
        nfa = NFA()
        nfa.add_state(1)
        self.assertEqual(nfa.trans_matrix[1]['x'], set())
        self.assertFalse(nfa.accepting_states)
        self.assertEqual(nfa.starting_state, None)

    def test_duplicate_states(self):
        nfa = NFA()
        nfa.add_state(1)
        nfa.add_state(2)
        nfa.add_transition(1, 2, nfa.epsilon)
        nfa.add_state(1)
        self.assertEqual(nfa.trans_matrix[1][nfa.epsilon], {2})


class TestMarkingStates(unittest.TestCase):
    def test_mark_starting(self):
        nfa = NFA()
        nfa.add_state(1)
        nfa.mark_starting(1)
        self.assertEqual(nfa.starting_state, 1)

    def test_mark_accepting(self):
        nfa = NFA()
        nfa.add_state(1)
        nfa.add_state(2)
        nfa.mark_accepting(2, 33)
        nfa.add_state(3)
        nfa.mark_accepting(3, 45)
        nfa.add_state(4)
        self.assertEqual(nfa.accepting_states, {2: 33, 3: 45})


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


class TestCopy(unittest.TestCase):
    def test_copy(self):
        nfa = build_test_nfa()
        copy_nfa = nfa.copy()
        self.assertEqual(copy_nfa.trans_matrix, nfa.trans_matrix)
        self.assertEqual(copy_nfa.starting_state, nfa.starting_state)
        self.assertEqual(copy_nfa.accepting_states, nfa.accepting_states)
        self.assertEqual(copy_nfa.alphabet, nfa.alphabet)
        copy_nfa.add_state(42)
        copy_nfa.add_state(1337)
        copy_nfa.add_transition(1, 1337, 'leet')
        copy_nfa.mark_starting(42)
        copy_nfa.mark_accepting(1337, 404)
        self.assertEqual(nfa.trans_matrix[1]['leet'], set())
        self.assertFalse(42 in nfa.trans_matrix)
        self.assertEqual(nfa.starting_state, 0)
        self.assertFalse(1337 in nfa.accepting_states)
        self.assertFalse('leet' in nfa.alphabet)


class TestUtils(unittest.TestCase):
    def test_cat(self):
        nfa1 = build_nfa1()
        nfa2 = build_test_nfa()
        cat_nfa = cat([nfa1, nfa2])
        draw_nfa(cat_nfa, 'cat_nfa')

    def test_alt(self):
        nfa1 = build_nfa1()
        nfa2 = build_test_nfa()
        alt_nfa = alt([nfa1, nfa2])
        draw_nfa(alt_nfa, 'alt_nfa')

    def test_closure(self):
        nfa = build_nfa1()
        c_nfa = closure(nfa)
        draw_nfa(c_nfa, 'closure_nfa')


if __name__ == '__main__':
    unittest.main()
