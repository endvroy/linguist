from enum import Enum, unique

from linguist.base.lalr_parser.parser_base import RuleSet, d, t
from linguist.base.metachar import eof, epsilon
from linguist.exceptions import LALRTableBuildError


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
                    for rule_id, rule in enumerate(self.nt_rules[next_ntid]):
                        loc = 0
                        while loc < len(rule) and rule[loc] == t(epsilon):  # skip over epsilons
                            loc += 1
                        key = (next_ntid, rule_id, loc)
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

    def calc_initial(self):
        initial = {}
        for rule_id, rule in enumerate(self.nt_rules[self.goal]):
            loc = 0
            while loc < len(rule) and rule[loc] == t(epsilon):  # skip over epsilons
                loc += 1
            initial[(self.goal, rule_id, loc)] = {eof}
        # initial = {(self.goal, i, 0): {eof} for i in range(len(self.nt_rules[self.goal]))}
        initial = self.item_closure(initial)
        return initial

    def calc_parse_table(self):
        initial = self.calc_initial()

        cc = [initial]
        cc_map = {frozenset(initial.keys()): 0}
        goto = [{}]
        # build cc and goto table
        work_list = {0}
        while work_list:
            i = work_list.pop()
            item_set = cc[i]

            partition = self.item_partition_goto(item_set)  # prepare goto
            for sym, item_set_x in partition.items():
                new_item_set = self.item_closure(self.item_advance(item_set_x))  # calc goto
                cc_key = frozenset(new_item_set.keys())

                # update canonical collection
                if cc_key in cc_map:
                    for k, v in new_item_set.items():
                        diff = v - cc[cc_map[cc_key]][k]
                        if diff:
                            cc[cc_map[cc_key]][k] |= diff  # merge lookahead
                            work_list.add(cc_map[cc_key])
                else:  # found new state
                    cc_map[cc_key] = len(cc)
                    work_list.add(len(cc))
                    cc.append(new_item_set)
                    goto.append({})

                goto_id = cc_map[cc_key]
                goto[i][sym] = goto_id  # update goto table

        action = []  # build action table
        for i, item_set in enumerate(cc):
            action.append({})
            for item, la_set in item_set.items():
                ntid, rule_id, pos = item
                derives = self.nt_rules[ntid][rule_id]  # fetch the original rule
                if pos == len(derives):  # accept or reduce
                    for category in la_set:
                        if category == eof and ntid == self.goal:  # accept
                            entry = Action.accept, ntid, rule_id
                            if eof in action[i] and action[i][eof] != entry:
                                raise LALRTableBuildError(cc, i)
                            else:
                                action[i][eof] = entry  # accept
                        else:  # reduce
                            entry = Action.reduce, ntid, rule_id
                            if category in action[i] and action[i][category] != entry:  # conflict
                                raise LALRTableBuildError(cc, i)
                            else:
                                action[i][category] = entry  # reduce
                else:  # shift or error
                    next_sym = derives[pos]
                    if next_sym[0] == 't':  # shift
                        entry = Action.shift,
                        if next_sym[1] in action[i] and action[i][next_sym[1]] != entry:
                            raise LALRTableBuildError(cc, i)
                        else:
                            action[i][next_sym[1]] = entry  # shift

        return cc, action, goto  # action table, goto table
