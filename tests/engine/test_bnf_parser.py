import unittest

from linguist.base.metachar import eof
from linguist.engine.bnf_parser import *
from linguist.exceptions import ScanError, ParseError


class Test(unittest.TestCase):
    def test_lex(self):
        tokens = bnf_scanner.tokens(
            '''list = list a
                | _x_ y42
                |''')
        self.assertEqual([(NAME, 'list'),
                          (EQ, '='),
                          (NAME, 'list'),
                          (NAME, 'a'),
                          (ALT_DELIM, '|'),
                          (NAME, '_x_'),
                          (NAME, 'y42'),
                          (ALT_DELIM, '|'),
                          (eof, '')],
                         list(tokens))

        with self.assertRaises(ScanError):
            list(bnf_scanner.tokens('3list = 3list a'))

    def test_parser(self):
        tokens = bnf_scanner.tokens(
            '''list = list a
                | _x_ y42
                |''')
        result = bnf_parser.parse(tokens)
        self.assertEqual(('list', [('list', 'a'),
                                   ('_x_', 'y42'),
                                   ()]), result)

        tokens = bnf_scanner.tokens(
            '''A = ''')
        result = bnf_parser.parse(tokens)
        self.assertEqual(('A', [()]), result)

        tokens = bnf_scanner.tokens(
            '''A = B C''')
        result = bnf_parser.parse(tokens)
        self.assertEqual(('A', [('B', 'C')]), result)


if __name__ == '__main__':
    unittest.main()
