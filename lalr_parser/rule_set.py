from parserlib.rule_set import RuleSet, d, t, nt
from metachar import eof


class Item:
    def __init__(self, ntid, rule_id, pos, la_set):
        self.ntid = ntid
        self.rule_id = rule_id
        self.pos = pos
        self.la_set = frozenset(la_set)

    def __eq__(self, other):
        return self.ntid == other.ntid and self.rule_id == other.rule_id and self.pos == other.pos and self.la_set == other.la_set

    def __hash__(self):
        return hash(self.ntid) ^ hash(self.rule_id) ^ hash(self.pos) ^ hash(self.la_set)

    def __repr__(self):
        return f'Item({self.ntid}, {self.rule_id}, {self.pos}, {self.la_set})'


class LALRRuleSet(RuleSet):
    def item_closure(self, item_map):
        closure = item_map.copy()
        work_list = closure.copy()
        while work_list:
            item, la_set = work_list.popitem()
            ntid, rule_id, pos = item

            derives = self.nt_rules[ntid][rule_id]  # fetch the original rule
            if pos < len(derives):
                next_symbol = derives[pos]
                if next_symbol[0] == 'nt':
                    new_la = set()
                    for category in la_set:
                        new_la |= self.calc_first_set_seq(derives[pos + 1:] + d(t(category)))

                    next_ntid = next_symbol[1]
                    for rule_id in range(len(self.nt_rules[next_ntid])):
                        key = (next_ntid, rule_id, 0)
                        if key in closure:
                            diff = new_la - closure[key]
                            if diff:
                                closure[key] |= diff
                                work_list[key] = diff
                        else:
                            closure[key] = new_la.copy()
                            work_list[key] = new_la.copy()
        return closure

    def item_partition_goto(self, item_set):
        partition = {}
        for item, la_set in item_set.items():
            ntid, rule_id, pos = item

            derives = self.nt_rules[ntid][rule_id]  # fetch the original rule
            if pos < len(derives):
                next_symbol = derives[pos]
                if next_symbol in partition:
                    partition[next_symbol][item] = la_set.copy()
                else:
                    partition[next_symbol] = {item: la_set.copy()}
        return partition

    def item_advance(self, item_set):
        new_set = {}
        for item, la_set in item_set.items():
            ntid, rule_id, pos = item
            new_set[(ntid, rule_id, pos + 1)] = la_set.copy()
        return new_set
