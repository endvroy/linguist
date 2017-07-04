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


def build_test_dfa():  # example DFA on page 56
    dfa = DFA(dict_to_dfa_matrix({0: {'f': 1},
                                  1: {'e': 2,
                                      'i': 4},
                                  2: {'e': 3},
                                  3: {},
                                  4: {'e': 5},
                                  5: {}}),
              0,
              {3: 42, 5: 42},
              {'f', 'e', 'i'})
    return dfa


def build_test_dfa_2():
    dfa = DFA(dict_to_dfa_matrix({0: {'a': 2,
                                      'i': 1,
                                      'f': 2},
                                  1: {'a': 2,
                                      'i': 2,
                                      'f': 3},
                                  2: {'a': 2,
                                      'i': 2,
                                      'f': 2},
                                  3: {'a': 2,
                                      'i': 2,
                                      'f': 2}}),
              0,
              {1: 'id', 2: 'id', 3: 'if'},
              {'a', 'i', 'f'})
    return dfa


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
        dfa = build_test_dfa()

        partition, rev_index = partition_states(dfa)
        self.assertEqual(partition,
                         {frozenset({3, 5}),
                          frozenset({0}),
                          frozenset({1}),
                          frozenset({2, 4})})
        # self.assertEqual(RevIndex(partition).p_map, rev_index.p_map)

    def test_partition_2(self):
        dfa = build_test_dfa_2()

        partition, rev_index = partition_states(dfa)
        self.assertEqual(partition,
                         {frozenset({0}),
                          frozenset({1}),
                          frozenset({2}),
                          frozenset({3})})


if __name__ == '__main__':
    unittest.main()
