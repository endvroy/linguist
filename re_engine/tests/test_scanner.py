from re_engine.re_parser import scanner
from metachar import eof
import unittest


class TestLexer(unittest.TestCase):
    def test_scan(self):
        tokens = scanner.tokens('a.t[^0-9] 麻辣香锅')
        self.assertEqual([(13, 'a'),
                          (12, '.'),
                          (13, 't'),
                          (3, '['),
                          (10, '^'),
                          (13, '0'),
                          (11, '-'),
                          (13, '9'),
                          (4, ']'),
                          (13, ' '),
                          (13, '麻'),
                          (13, '辣'),
                          (13, '香'),
                          (13, '锅'),
                          (eof, '')],
                         list(tokens))


if __name__ == '__main__':
    unittest.main()
