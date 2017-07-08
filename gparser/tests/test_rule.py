from gparser.rule import *
import unittest


class TestRuleSet(unittest.TestCase):
    def test_new_nt(self):
        rule_set = RuleSet()
        ntid = rule_set.new_nt(1)
        self.assertEqual(ntid, [0])
        ntid = rule_set.new_nt(1)
        self.assertEqual(ntid, [1])
        ntid_list = rule_set.new_nt(3)
        self.assertEqual(ntid_list, [2, 3, 4])
        ntid = rule_set.new_nt(1)
        self.assertEqual(ntid, [5])

    def test_rewrite_rule(self):
        rule_set = RuleSet()
        expr, term = rule_set.new_nt(2)
        rule_set.add_rule(expr, d(nt(expr), t('+'), nt(term)))
        rule_set.add_rule(expr, d(nt(expr), t('-'), nt(term)))
        rule_set.add_rule(expr, d(nt(term)))
        rule_set.rewrite_rule(expr)
        expr_prime = rule_set._next_ntid - 1
        self.assertEqual(rule_set.nt_rules,
                         {expr: [d(nt(term), nt(expr_prime))],
                          expr_prime: [d(t('+'), nt(term), nt(expr_prime)),
                                       d(t('-'), nt(term), nt(expr_prime)),
                                       d(t(epsilon))],
                          term: []})

    def test_elim_indir_lr(self):
        rule_set = RuleSet()  # example grammar on Dragon Book pp.213
        S, A = rule_set.new_nt(2)
        rule_set.add_rule(S, d(nt(A), t('a')))
        rule_set.add_rule(S, d(t('b')))
        rule_set.add_rule(A, d(nt(A), t('c')))
        rule_set.add_rule(A, d(nt(S), t('d')))
        rule_set.elim_indir_lr()
        self.assertEqual(rule_set.nt_rules, {S: [d(nt(A), t('a')),
                                                 d(t('b'))],
                                             A: [d(nt(A), t('c')),
                                                 d(nt(A), t('a'), t('d')),
                                                 d(t('b'), t('d'))]})

    def test_first_sets(self):  # example grammar on EC pp.101
        rule_set = RuleSet()
        expr, expr_prime, term, term_prime, factor = rule_set.new_nt(5)
        rule_set.add_rule(expr, d(nt(term), nt(expr_prime)))
        rule_set.add_rule(expr_prime, d(t('+'), nt(term), nt(expr_prime)))
        rule_set.add_rule(expr_prime, d(t('-'), nt(term), nt(expr_prime)))
        rule_set.add_rule(expr_prime, d(t(epsilon)))
        rule_set.add_rule(term, d(nt(factor), nt(term_prime)))
        rule_set.add_rule(term_prime, d(t('*'), nt(factor), nt(term_prime)))
        rule_set.add_rule(term_prime, d(t('/'), nt(factor), nt(term_prime)))
        rule_set.add_rule(term_prime, d(t(epsilon)))
        rule_set.add_rule(factor, d(t('('), nt(expr), t(')')))
        rule_set.add_rule(factor, d(t('num')))
        rule_set.add_rule(factor, d(t('name')))
        first_sets = rule_set.calc_first_sets()
        # answer on EC pp.105
        self.assertEqual(first_sets, {expr: {'(', 'name', 'num'},
                                      expr_prime: {'+', '-', epsilon},
                                      term: {'(', 'name', 'num'},
                                      term_prime: {'*', '/', epsilon},
                                      factor: {'(', 'name', 'num'}})

    def test_follow_sets(self):
        rule_set = RuleSet()
        expr, expr_prime, term, term_prime, factor = rule_set.new_nt(5)
        rule_set.mark_goal(expr)
        rule_set.add_rule(expr, d(nt(term), nt(expr_prime)))
        rule_set.add_rule(expr_prime, d(t('+'), nt(term), nt(expr_prime)))
        rule_set.add_rule(expr_prime, d(t('-'), nt(term), nt(expr_prime)))
        rule_set.add_rule(expr_prime, d(t(epsilon)))
        rule_set.add_rule(term, d(nt(factor), nt(term_prime)))
        rule_set.add_rule(term_prime, d(t('*'), nt(factor), nt(term_prime)))
        rule_set.add_rule(term_prime, d(t('/'), nt(factor), nt(term_prime)))
        rule_set.add_rule(term_prime, d(t(epsilon)))
        rule_set.add_rule(factor, d(t('('), nt(expr), t(')')))
        rule_set.add_rule(factor, d(t('num')))
        rule_set.add_rule(factor, d(t('name')))
        first_sets = rule_set.calc_first_sets()
        follow_sets = rule_set.calc_follow_sets(first_sets)
        # answer on EC pp.106
        self.assertEqual(follow_sets, {expr: {')', eof},
                                       expr_prime: {')', eof},
                                       term: {'+', '-', ')', eof},
                                       term_prime: {'+', '-', ')', eof},
                                       factor: {'+', '-', '*', '/', ')', eof}})


if __name__ == '__main__':
    unittest.main()
