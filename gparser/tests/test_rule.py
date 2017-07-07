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
        expr_prime = rule_set._nt_index - 1
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


if __name__ == '__main__':
    unittest.main()
