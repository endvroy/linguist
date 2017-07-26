import unittest

from ll_parser.rule_set import *


class TestLLRuleSet(unittest.TestCase):
    def test_new_nt(self):
        rule_set = LLRuleSet()
        ntid = rule_set.new_nt(1)
        self.assertEqual(ntid, [0])
        ntid = rule_set.new_nt(1)
        self.assertEqual(ntid, [1])
        ntid_list = rule_set.new_nt(3)
        self.assertEqual(ntid_list, [2, 3, 4])
        ntid = rule_set.new_nt(1)
        self.assertEqual(ntid, [5])

    def test_rewrite_rule(self):
        rule_set = LLRuleSet()
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
        rule_set = LLRuleSet()  # example grammar on Dragon Book pp.213
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

    def test_parse_table(self):
        rule_set = LLRuleSet()  # example grammar on DB pp.217
        E, Ep, T, Tp, F = rule_set.new_nt(5)
        rule_set.add_rule(E, d(nt(T), nt(Ep)))
        rule_set.add_rule(Ep, d(t('+'), nt(T), nt(Ep)))
        rule_set.add_rule(Ep, d(t(epsilon)))
        rule_set.add_rule(T, d(nt(F), nt(Tp)))
        rule_set.add_rule(Tp, d(t('*'), nt(F), nt(Tp)))
        rule_set.add_rule(Tp, d(t(epsilon)))
        rule_set.add_rule(F, d(t('('), nt(E), t(')')))
        rule_set.add_rule(F, d(t('id')))
        rule_set.mark_goal(E)
        parse_table = rule_set.calc_parse_table()
        self.assertEqual(parse_table,  # answer on DB pp.225
                         {E: {'id': d(nt(T), nt(Ep)),
                              '(': d(nt(T), nt(Ep))},
                          Ep: {'+': d(t('+'), nt(T), nt(Ep)),
                               ')': d(t(epsilon)),
                               eof: d(t(epsilon)),
                               epsilon: d(t(epsilon))},
                          T: {'id': d(nt(F), nt(Tp)),
                              '(': d(nt(F), nt(Tp))},
                          Tp: {'+': d(t(epsilon)),
                               '*': d(t('*'), nt(F), nt(Tp)),
                               ')': d(t(epsilon)),
                               eof: d(t(epsilon)),
                               epsilon: d(t(epsilon))},
                          F: {'id': d(t('id')),
                              '(': d(t('('), nt(E), t(')'))}
                          })

    def test_conflict_parse_table(self):
        rule_set = LLRuleSet()  # example grammar on DB pp.225
        S, Sp, E = rule_set.new_nt(3)
        rule_set.add_rule(S, d(t('i'), nt(E), t('t'), nt(S), nt(Sp)))
        rule_set.add_rule(S, d(t('a')))
        rule_set.add_rule(S, d(t('e'), nt(S)))
        rule_set.add_rule(S, d(t(epsilon)))
        rule_set.add_rule(E, d(t('b')))
        rule_set.mark_goal(S)
        with self.assertRaises(RuntimeError):
            rule_set.calc_parse_table()


if __name__ == '__main__':
    unittest.main()
