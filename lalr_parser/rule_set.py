from parserlib.rule_set import RuleSet, d, t, nt
from metachar import eof
from enum import Enum, unique


@unique
class Action(Enum):
    shift = 0
    reduce = 1
    accept = 2


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

    def calc_parse_table(self):
        initial = {(self.goal, i, 0): {eof} for i in range(len(self.nt_rules[self.goal]))}
        initial = self.item_closure(initial)
        cc = [initial]
        cc_map = {frozenset(initial.keys()): 0}

        action = []
        goto = []

        # build cc and goto table
        i = 0
        while i < len(cc):
            item_set = cc[i]
            goto.append({})

            partition = self.item_partition_goto(item_set)
            for sym, item_set_x in partition.items():
                new_item_set = self.item_closure(self.item_advance(item_set_x))
                cc_key = frozenset(new_item_set.keys())

                # update canonical collection
                if cc_key in cc_map:
                    for k, v in new_item_set.items():
                        cc[cc_map[cc_key]][k] |= v  # merge lookahead
                else:  # found new state
                    cc_map[cc_key] = len(cc)
                    cc.append(new_item_set)

                goto_id = cc_map[cc_key]
                goto[i][sym] = goto_id  # update goto table
            i += 1

        for i, item_set in enumerate(cc):  # build action table
            action.append({})
            for item, la_set in item_set.items():
                ntid, rule_id, pos = item
                derives = self.nt_rules[ntid][rule_id]  # fetch the original rule
                for category in la_set:
                    if pos == len(derives):
                        if category == eof and ntid == self.goal:
                            action[i][eof] = Action.accept,  # accept
                        else:
                            action[i][category] = Action.reduce, ntid, rule_id  # reduce
                    else:
                        next_sym = derives[pos]
                        if next_sym[0] == 't':
                            action[i][next_sym[1]] = Action.shift,  # shift

        return action, goto  # action table, goto table
