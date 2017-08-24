import unittest

from linguist.base.metachar import eof
from linguist.engine.bnf_parser import *


class Test(unittest.TestCase):
    def test_lex(self):
        tokens = scanner.tokens(
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

        with self.assertRaises(RuntimeError):
            list(scanner.tokens('3list = 3list a'))

    def test_parser(self):
        tokens = scanner.tokens(
            '''list = list a
                | _x_ y42
                |''')
        result = parser.parse(tokens)
        self.assertEqual(('list', [('list', 'a'),
                                   ('_x_', 'y42'),
                                   ()]), result)

        tokens = scanner.tokens(
            '''A = ''')
        result = parser.parse(tokens)
        self.assertEqual(('A', [()]), result)

        tokens = scanner.tokens(
            '''A = B C''')
        result = parser.parse(tokens)
        self.assertEqual(('A', [('B', 'C')]), result)


if __name__ == '__main__':
    unittest.main()
