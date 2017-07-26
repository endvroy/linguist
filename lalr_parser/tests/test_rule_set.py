import unittest
from lalr_parser.rule_set import *


def build_test_rule():
    rule_set = LALRRuleSet()  # example grammar on EC pp.120
    goal, list_, pair = rule_set.new_nt(3)
    rule_set.add_rule(goal, d(nt(list_)))
    rule_set.add_rule(list_, d(nt(list_), nt(pair)))
    rule_set.add_rule(list_, d(nt(pair)))
    rule_set.add_rule(pair, d(t('('), nt(pair), t(')')))
    rule_set.add_rule(pair, d(t('('), t(')')))
    rule_set.mark_goal(goal)
    return rule_set


class TestRuleSet(unittest.TestCase):
    def test_item_closure(self):
        rule_set = LALRRuleSet()  # example grammar on EC pp.120
        goal, list_, pair = rule_set.new_nt(3)
        rule_set.add_rule(goal, d(nt(list_)))
        rule_set.add_rule(list_, d(nt(list_), nt(pair)))
        rule_set.add_rule(list_, d(nt(pair)))
        rule_set.add_rule(pair, d(t('('), nt(pair), t(')')))
        rule_set.add_rule(pair, d(t('('), t(')')))
        rule_set.mark_goal(goal)

        first_sets = rule_set.calc_first_sets()
        item_set = {(goal, 0, 0): {eof}}
        closure = rule_set.item_closure(first_sets, item_set)
        self.assertEqual(closure, {(goal, 0, 0): {eof},
                                   (list_, 0, 0): {eof, '('},
                                   (list_, 1, 0): {eof, '('},
                                   (pair, 0, 0): {eof, '('},
                                   (pair, 1, 0): {eof, '('}})


if __name__ == '__main__':
    unittest.main()
