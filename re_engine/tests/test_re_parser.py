from re_engine.re_parser import *
from scanner.scanner import scanner_builder, CategoryInfo
from metachar import eof
import unittest


class TestLexer(unittest.TestCase):
    def test_lex(self):
        tokens = re_scanner.tokens('a.t[^0-9] 麻辣香锅')
        self.assertEqual([(12, 'a'),
                          (11, '.'),
                          (12, 't'),
                          (2, '['),
                          (9, '^'),
                          (12, '0'),
                          (10, '-'),
                          (12, '9'),
                          (3, ']'),
                          (12, ' '),
                          (12, '麻'),
                          (12, '辣'),
                          (12, '香'),
                          (12, '锅'),
                          (eof, '')],
                         list(tokens))


class TestGrammar(unittest.TestCase):
    def test_parser(self):
        tokens = re_scanner.tokens(r'(a|[0-9^])+\\?')
        nfa = re_parser.parse(tokens, 0)
        scanner = scanner_builder(nfa, {0: CategoryInfo('dummy', 0)})

        tks = scanner.tokens('a\\')
        self.assertEqual([(0, 'a\\'), (eof, '')], list(tks))

        tks = scanner.tokens('a42aa13^37')
        self.assertEqual([(0, 'a42aa13^37'), (eof, '')], list(tks))

        tks = scanner.tokens('a\\\\')
        with self.assertRaises(RuntimeError):
            list(tks)

        tks = scanner.tokens('\\')
        with self.assertRaises(RuntimeError):
            list(tks)

    def test_parser_2(self):
        tokens = re_scanner.tokens(r'[^^0-9]+')
        nfa = re_parser.parse(tokens, 0)
        scanner = scanner_builder(nfa, {0: CategoryInfo('dummy', 0)})

        tks = scanner.tokens('a\\')
        self.assertEqual([(0, 'a\\'), (eof, '')], list(tks))

        tks = scanner.tokens('abc麻辣香锅')
        self.assertEqual([(0, 'abc麻辣香锅'), (eof, '')], list(tks))

        tks = scanner.tokens('^')
        with self.assertRaises(RuntimeError):
            list(tks)

        tks = scanner.tokens('4')
        with self.assertRaises(RuntimeError):
            list(tks)

    def test_errornous_re(self):
        tokens = re_scanner.tokens(r'[a-m-z]')
        with self.assertRaises(RuntimeError):
            re_parser.parse(tokens)


if __name__ == '__main__':
    unittest.main()
