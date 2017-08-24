import unittest

from linguist.lang_builder import *


class Test(unittest.TestCase):
    def test_dfa_checker(self):
        self.assertEqual(True, dfa_checker(name_dfa, 'bv5_3'))
        self.assertEqual(True, dfa_checker(name_dfa, '_'))
        self.assertEqual(False, dfa_checker(name_dfa, '9ab'))

    def test_builder(self):
        lb = LangBuilder()
        lb.lex('PLUS', r'\+')
        lb.lex('MINUS', '-')
        lb.lex('TIMES', r'\*')
        lb.lex('DIVIDE', '/')
        lb.lex('LPAREN', r'\(')
        lb.lex('RPAREN', r'\)')
        lb.lex('BLANK', '[ \n\t]+', skip=True)

        @lb.lex('NUM', '[0-9]+')
        def rule_NUM(lexeme):
            return int(lexeme)

        lb.goal('expr')

        @lb.rule('expr = expr PLUS term')
        def rule_add(data_list, repo):
            return data_list[0] + data_list[2]

        @lb.rule('expr = expr MINUS term')
        def rule_minus(data_list, repo):
            return data_list[0] - data_list[2]

        @lb.rule('expr = term')
        def rule_expr(data_list, repo):
            return data_list[0]

        @lb.rule('term = term TIMES factor')
        def rule_times(data_list, repo):
            return data_list[0] * data_list[2]

        @lb.rule('term = term DIVIDE factor')
        def rule_divide(data_list, repo):
            return data_list[0] / data_list[2]

        @lb.rule('term = factor')
        def rule_term(data_list, repo):
            return data_list[0]

        @lb.rule('factor = NUM')
        def rule_factor(data_list, repo):
            return data_list[0]

        @lb.rule('factor = LPAREN expr RPAREN')
        def rule_factor_expr(data_list, repo):
            return data_list[1]

        scanner, parser = lb.build()

        tokens = scanner.tokens('3 + 4 * 5')
        result = parser.parse(tokens)
        self.assertEqual(23, result)

        tokens = scanner.tokens('(3 + 4) * 5')
        result = parser.parse(tokens)
        self.assertEqual(35, result)


if __name__ == '__main__':
    unittest.main()
