from linguist.base.lalr_parser.rule_set import LALRRuleSet
from linguist.base.scanner.scanner import scanner_builder

from linguist.base.lalr_parser.parser import LALRParser
from linguist.base.metachar import epsilon
from linguist.base.scanner.re_utils import alt
from linguist.engine.bnf_parser import parser as bnf_parser, scanner as bnf_scanner


class PartialBuilder:
    def __init__(self):
        self.name_map = {}
        # grammar info
        self.goal_name = None
        self.raw_rules = {}
        self.rule_set = LALRRuleSet()
        self.rule_actions = {}
        # lex info
        self.nfa_list = []
        self.category_info = []

    def goal(self, name):
        self.goal_name = name

    def rule(self, rule_str):
        tokens = bnf_scanner.tokens(rule_str)
        name, derives_list = bnf_parser.parse(tokens)
        if name in self.raw_rules:
            rule_range = list(range(len(self.raw_rules[name]),
                                    len(self.raw_rules[name]) + len(derives_list)))
            ntid = self.name_map[name][1]
            self.raw_rules[name] += derives_list
        else:
            rule_range = list(range(len(derives_list)))
            ntid = self.rule_set.new_nt(1)[0]
            self.raw_rules[name] = derives_list
            self.name_map[name] = ('nt', ntid)

        for rule_id in rule_range:
            self.rule_actions[(ntid, rule_id)] = None

        def wrapper(fn):
            for rule_id in rule_range:
                self.rule_actions[(ntid, rule_id)] = fn
            return fn

        return wrapper

    def build(self):
        if self.goal_name is None:
            raise RuntimeError('goal symbol not set')
        if self.goal_name not in self.name_map:
            raise RuntimeError(f'symbol {self.goal_name} not defined')
        self.rule_set.mark_goal(self.name_map[self.goal_name][1])
        # build rule set
        for nt_name, all_derives in self.raw_rules.items():
            ntid = self.name_map[nt_name][1]
            for d_list in all_derives:
                derives = []
                if not d_list:
                    derives.append(('t', epsilon))
                else:
                    for d_name in d_list:
                        if d_name not in self.name_map:
                            raise RuntimeError(f'symbol {d_name} is not defined')
                        else:
                            derives.append(self.name_map[d_name])
                self.rule_set.add_rule(ntid, tuple(derives))
        parser = LALRParser(self.rule_set, self.rule_actions)

        # build NFA
        nfa = alt(self.nfa_list)
        scanner = scanner_builder(nfa, self.category_info)

        return scanner, parser
