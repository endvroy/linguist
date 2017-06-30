from minimize_dfa import *
from nfa_to_dfa import dict_to_dfa_matrix
from dfa import DFA
import unittest


class TestBuilder(unittest.TestCase):
    def test_matrix_builder(self):
        matrix = dict_to_dfa_matrix({0: {'f': 1},
                                     1: {'e': 2,
                                         'i': 4},
                                     2: {'e': 3},
                                     3: {},
                                     4: {'e': 5},
                                     5: {}})
        self.assertEqual(set(matrix.keys()), set(range(6)))
        self.assertEqual(matrix[1]['e'], 2)
        self.assertEqual(matrix[1]['i'], 4)
        self.assertEqual(matrix[0]['i'], None)
        self.assertEqual(matrix[3]['x'], None)


class TestMinimize(unittest.TestCase):
    def test_RevIndex(self):
        partitions = {frozenset({1, 2, 3}), frozenset({4, 5})}
        rev_index = RevIndex(partitions)
        self.assertEqual(rev_index.p_id, 2)
        self.assertTrue(rev_index.p_map[1] == rev_index.p_map[2] == rev_index.p_map[3])
        self.assertEqual(rev_index.p_map[4], rev_index.p_map[5])
        self.assertNotEqual(rev_index.p_map[1], rev_index.p_map[4])
        rev_index.mark_new_part({2, 3})
        self.assertEqual(rev_index.p_id, 3)
        self.assertEqual(rev_index.p_map[2], rev_index.p_map[3])
        self.assertNotEqual(rev_index.p_map[1], rev_index.p_map[2])
        self.assertNotEqual(rev_index.p_map[2], rev_index.p_map[4])

    def test_partition(self):
        dfa = DFA()
        dfa.trans_matrix = dict_to_dfa_matrix({0: {'f': 1},
                                               1: {'e': 2,
                                                   'i': 4},
                                               2: {'e': 3},
                                               3: {},
                                               4: {'e': 5},
                                               5: {}})

        dfa.accepting_states = {3, 5}
        dfa.alphabet = {'f', 'e', 'i'}
        partition = partition_states(dfa)
        self.assertEqual(partition,
                         {frozenset({3, 5}),
                          frozenset({0}),
                          frozenset({1}),
                          frozenset({2, 4})})
