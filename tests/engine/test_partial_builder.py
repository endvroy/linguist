from bnf_engine.partial_builder import *
import unittest


class Test(unittest.TestCase):
    def test_rule(self):
        pb = PartialBuilder()

        @pb.rule('''expr = expr add term
                        |expr sub term''')
        def foo():
            pass

        self.assertEqual({'expr': [('expr', 'add', 'term'),
                                   ('expr', 'sub', 'term')]},
                         pb.raw_rules)
        self.assertEqual({'expr': ('nt', 0)}, pb.name_map)
        self.assertEqual(foo, pb.rule_actions[(0, 0)])
        self.assertEqual(foo, pb.rule_actions[(0, 1)])

        @pb.rule('''expr = term
                            |lp expr rp
                            |''')
        def bar():
            pass

        self.assertEqual({'expr': [('expr', 'add', 'term'),
                                   ('expr', 'sub', 'term'),
                                   ('term',),
                                   ('lp', 'expr', 'rp'),
                                   ()]},
                         pb.raw_rules)
        self.assertEqual({'expr': ('nt', 0)}, pb.name_map)
        self.assertEqual(foo, pb.rule_actions[(0, 0)])
        self.assertEqual(foo, pb.rule_actions[(0, 1)])
        self.assertEqual(bar, pb.rule_actions[(0, 2)])
        self.assertEqual(bar, pb.rule_actions[(0, 3)])
        self.assertEqual(bar, pb.rule_actions[(0, 4)])

        pb.rule('''term = term times factor''')

        self.assertEqual({'expr': [('expr', 'add', 'term'),
                                   ('expr', 'sub', 'term'),
                                   ('term',),
                                   ('lp', 'expr', 'rp'),
                                   ()],
                          'term': [('term', 'times', 'factor')]},
                         pb.raw_rules)
        self.assertEqual({'expr': ('nt', 0),
                          'term': ('nt', 1)}, pb.name_map)
        self.assertEqual(foo, pb.rule_actions[(0, 0)])
        self.assertEqual(foo, pb.rule_actions[(0, 1)])
        self.assertEqual(bar, pb.rule_actions[(0, 2)])
        self.assertEqual(bar, pb.rule_actions[(0, 3)])
        self.assertEqual(bar, pb.rule_actions[(0, 4)])
        self.assertEqual(None, pb.rule_actions[(1, 0)])


if __name__ == '__main__':
    unittest.main()
