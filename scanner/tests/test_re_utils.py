from scanner.re_utils import *
from scanner.tests.tools import build_test_nfa, build_nfa1, draw_nfa
import unittest


class TestUtils(unittest.TestCase):
    def test_char_range(self):
        markers, accept = char_range('a', 'z')
        nfa = char_set(markers, accept, 0)
        self.assertEqual(0, nfa.classifier.classify(chr(ord('a') - 1)))
        self.assertEqual(1, nfa.classifier.classify('a'))
        self.assertEqual(1, nfa.classifier.classify('t'))
        self.assertEqual(1, nfa.classifier.classify('z'))
        self.assertEqual(2, nfa.classifier.classify(chr(ord('z') + 1)))

    def test_merge_members(self):
        a = char_range('a', 'z')
        b = char_member('_')
        c = char_range('A', 'Z')
        markers, accept = merge_members([a, b, c])
        self.assertEqual([ord('A'),
                          ord('Z') + 1,
                          ord('_'),
                          ord('_') + 1,
                          ord('a'),
                          ord('z') + 1], markers)
        self.assertEqual({1, 3, 5}, accept)

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
