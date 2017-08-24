import unittest

from linguist.base.lalr_parser.rule_set import LALRRuleSet, d, t, nt

from linguist.base.lalr_parser.parser import *
from linguist.base.metachar import eof


class TestParser(unittest.TestCase):
    def test_parse(self):
        rule_set = LALRRuleSet()
        expr, term, factor = rule_set.new_nt(3)
        rule_set.add_rule(expr, d(nt(expr), t('plus'), nt(term)))
        rule_set.add_rule(expr, d(nt(expr), t('minus'), nt(term)))
        rule_set.add_rule(expr, d(nt(term)))
        rule_set.add_rule(term, d(nt(term), t('times'), nt(factor)))
        rule_set.add_rule(term, d(nt(term), t('divide'), nt(factor)))
        rule_set.add_rule(term, d(nt(factor)))
        rule_set.add_rule(factor, d(t('num')))
        rule_set.mark_goal(expr)

        def action00(data_list, repo):
            return data_list[0] + data_list[2]

        def action01(data_list, repo):
            return data_list[0] - data_list[2]

        def action02(data_list, repo):
            return data_list[0]

        def action10(data_list, repo):
            return data_list[0] * data_list[2]

        def action11(data_list, repo):
            return data_list[0] / data_list[2]

        def action12(data_list, repo):
            return data_list[0]

        def action20(data_list, repo):
            return data_list[0]

        rule_actions = {(0, 0): action00,
                        (0, 1): action01,
                        (0, 2): action02,
                        (1, 0): action10,
                        (1, 1): action11,
                        (1, 2): action12,
                        (2, 0): action20}

        parser = LALRParser(rule_set, rule_actions)
        result = parser.parse([('num', 3), ('plus', '+'), ('num', 4), (eof, '')])
        self.assertEqual(result, 7)
        result = parser.parse([('num', 3), ('minus', '-'), ('num', 4), (eof, '')])
        self.assertEqual(result, -1)
        result = parser.parse([('num', 3), (eof, '')])
        self.assertEqual(result, 3)
        result = parser.parse([('num', 3),
                               ('plus', '+'),
                               ('num', 4),
                               ('times', '*'),
                               ('num', 5),
                               (eof, '')])
        self.assertEqual(result, 23)

        with self.assertRaises(RuntimeError):
            parser.parse([('num', 3), ('plus', '+'), ('plus', '+'), (eof, '')])

    def test_parse_2(self):
        rule_set = LALRRuleSet()
        expr, term, factor = rule_set.new_nt(3)
        rule_set.add_rule(expr, d(nt(expr), t('plus/minus'), nt(term)))
        rule_set.add_rule(expr, d(nt(term)))
        rule_set.add_rule(term, d(nt(term), t('times/divide'), nt(factor)))
        rule_set.add_rule(term, d(nt(factor)))
        rule_set.add_rule(factor, d(t('num')))
        rule_set.mark_goal(expr)

        def action00(data_list, repo):
            if data_list[1] == '+':
                return data_list[0] + data_list[2]
            else:
                return data_list[0] - data_list[2]

        def action01(data_list, repo):
            return data_list[0]

        def action10(data_list, repo):
            if data_list[1] == '*':
                return data_list[0] * data_list[2]
            else:
                return data_list[0] / data_list[2]

        def action11(data_list, repo):
            return data_list[0]

        def action20(data_list, repo):
            return data_list[0]

        rule_actions = {(0, 0): action00,
                        (0, 1): action01,
                        (1, 0): action10,
                        (1, 1): action11,
                        (2, 0): action20}

        parser = LALRParser(rule_set, rule_actions)
        result = parser.parse([('num', 3),
                               ('plus/minus', '+'),
                               ('num', 4),
                               ('times/divide', '*'),
                               ('num', 5),
                               (eof, '')])
        self.assertEqual(result, 23)


if __name__ == '__main__':
    unittest.main()
