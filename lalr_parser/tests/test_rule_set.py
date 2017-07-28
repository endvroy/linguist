import unittest
from lalr_parser.rule_set import *
import itertools


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

        item_set = {(goal, 0, 0): {eof}}
        closure = rule_set.item_closure(item_set)
        self.assertEqual(closure, {(goal, 0, 0): {eof},
                                   (list_, 0, 0): {eof, '('},
                                   (list_, 1, 0): {eof, '('},
                                   (pair, 0, 0): {eof, '('},
                                   (pair, 1, 0): {eof, '('}})

        item_set = {(pair, 0, 1): {eof, '('},
                    (pair, 1, 1): {eof, '('}}
        closure = rule_set.item_closure(item_set)
        self.assertEqual(closure, {(pair, 0, 1): {eof, '('},
                                   (pair, 1, 1): {eof, '('},
                                   (pair, 0, 0): {')'},
                                   (pair, 1, 0): {')'}})  # CC3

        item_set = {(pair, 0, 1): {')'},
                    (pair, 1, 1): {')'}}
        closure = rule_set.item_closure(item_set)
        self.assertEqual(closure, {(pair, 0, 0): {')'},
                                   (pair, 0, 1): {')'},
                                   (pair, 1, 0): {')'},
                                   (pair, 1, 1): {')'}})  # CC6

    def test_ietm_partition_goto(self):
        rule_set = LALRRuleSet()  # example grammar on EC pp.120
        goal, list_, pair = rule_set.new_nt(3)
        rule_set.add_rule(goal, d(nt(list_)))
        rule_set.add_rule(list_, d(nt(list_), nt(pair)))
        rule_set.add_rule(list_, d(nt(pair)))
        rule_set.add_rule(pair, d(t('('), nt(pair), t(')')))
        rule_set.add_rule(pair, d(t('('), t(')')))
        rule_set.mark_goal(goal)

        cc3 = {(pair, 0, 1): {eof, '('},
               (pair, 1, 1): {eof, '('},
               (pair, 0, 0): {')'},
               (pair, 1, 0): {')'}}

        partitions = rule_set.item_partition_goto(cc3)
        self.assertEqual(partitions,
                         {('nt', pair): {(pair, 0, 1): {eof, '('}},
                          ('t', '('): {(pair, 0, 0): {')'},
                                       (pair, 1, 0): {')'}},
                          ('t', ')'): {(pair, 1, 1): {eof, '('}}})

    def test_item_advance(self):
        rule_set = LALRRuleSet()  # example grammar on EC pp.120
        goal, list_, pair = rule_set.new_nt(3)
        rule_set.add_rule(goal, d(nt(list_)))
        rule_set.add_rule(list_, d(nt(list_), nt(pair)))
        rule_set.add_rule(list_, d(nt(pair)))
        rule_set.add_rule(pair, d(t('('), nt(pair), t(')')))
        rule_set.add_rule(pair, d(t('('), t(')')))
        rule_set.mark_goal(goal)

        item_set = {(pair, 0, 0): {')'},
                    (pair, 1, 0): {')'}}
        result = rule_set.item_advance(item_set)
        self.assertEqual(result, {(pair, 0, 1): {')'},
                                  (pair, 1, 1): {')'}})

    def assertIsomorphism(self, action, goto, correct_action, correct_goto):
        if len(action) != len(correct_action) or len(goto) != len(correct_goto):
            self.fail(f'number of states unequal: correct = {len(correct_action)}, got = {len(action)}')

        for state_map in itertools.permutations(range(len(action))):
            mapped_action = [action[i] for i in state_map]
            mapped_goto = [{} for i in range(len(action))]
            for a, b in enumerate(state_map):
                mapped_goto[a] = goto[b].copy()
                for k, v in mapped_goto[a].items():
                    mapped_goto[a][k] = state_map[v]
            if mapped_action == correct_action and mapped_goto == correct_goto:
                return
        else:
            self.fail('parse tables non-isomorphic')

    def test_calc_parse_table(self):
        rule_set = LALRRuleSet()  # example grammar on EC pp.120
        goal, list_, pair = rule_set.new_nt(3)
        rule_set.add_rule(goal, d(nt(list_)))
        rule_set.add_rule(list_, d(nt(list_), nt(pair)))
        rule_set.add_rule(list_, d(nt(pair)))
        rule_set.add_rule(pair, d(t('('), nt(pair), t(')')))
        rule_set.add_rule(pair, d(t('('), t(')')))
        rule_set.mark_goal(goal)

        action, goto = rule_set.calc_parse_table()
        correct_action = [{'(': (Action.shift,)},
                          {'(': (Action.shift,), eof: (Action.accept,)},
                          {'(': (Action.reduce, 1, 1), eof: (Action.reduce, 1, 1)},
                          {'(': (Action.shift,), ')': (Action.shift,)},
                          {'(': (Action.reduce, 1, 0), eof: (Action.reduce, 1, 0)},
                          {')': (Action.shift,)},
                          {'(': (Action.reduce, 2, 1), eof: (Action.reduce, 2, 1)},
                          {'(': (Action.reduce, 2, 0), eof: (Action.reduce, 2, 0)}]

        correct_goto = [{('nt', 1): 1, ('nt', 2): 2, ('t', '('): 3},
                        {('nt', 2): 4, ('t', '('): 3},
                        {},
                        {('nt', 2): 5, ('t', '('): 3, ('t', ')'): 6},
                        {},
                        {('t', ')'): 7},
                        {},
                        {}]

        self.assertIsomorphism(action, goto, correct_action, correct_goto)

    def test_calc_parse_table_2(self):
        rule_set = LALRRuleSet()  # example grammar on stanford handout pp.0
        S, X = rule_set.new_nt(2)
        rule_set.add_rule(S, d(nt(X), nt(X)))
        rule_set.add_rule(X, d(t('a'), nt(X)))
        rule_set.add_rule(X, d(t('b')))
        rule_set.mark_goal(S)

        action, goto = rule_set.calc_parse_table()
        correct_action = [{'a': (Action.shift,), 'b': (Action.shift,)},
                          {'a': (Action.shift,), 'b': (Action.shift,)},
                          {'a': (Action.shift,), 'b': (Action.shift,)},
                          {'a': (Action.reduce, 1, 1), 'b': (Action.reduce, 1, 1), eof: (Action.reduce, 1, 1)},
                          {eof: (Action.accept,)},
                          {'a': (Action.reduce, 1, 0), 'b': (Action.reduce, 1, 0), eof: (Action.reduce, 1, 0)}]

        correct_goto = [{('nt', X): 1, ('t', 'a'): 2, ('t', 'b'): 3},
                        {('nt', X): 4, ('t', 'a'): 2, ('t', 'b'): 3},
                        {('nt', X): 5, ('t', 'a'): 2, ('t', 'b'): 3},
                        {},
                        {},
                        {}]

        self.assertIsomorphism(action, goto, correct_action, correct_goto)


if __name__ == '__main__':
    unittest.main()
