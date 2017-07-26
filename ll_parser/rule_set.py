from parserlib.rule_set import RuleSet, d, t, nt
from metachar import epsilon, eof


class LLRuleSet(RuleSet):
    def rewrite_rule(self, ntid):
        lr_derives = []
        free_derives = []
        for derives in self.nt_rules[ntid]:
            if derives[0] == nt(ntid):
                lr_derives.append(derives)
            else:
                free_derives.append(derives)

        self.nt_rules[ntid].clear()
        tmp = self.new_nt(1)[0]
        for derives in free_derives:
            self.add_rule(ntid, derives + d(nt(tmp)))

        for derives in lr_derives:
            self.add_rule(tmp, derives[1:] + d(nt(tmp)))
        self.add_rule(tmp, d(t(epsilon)))

    def elim_indir_lr(self):
        nt_ordering = sorted(list(self.nt_rules.keys()))
        for idx, end_nt in enumerate(nt_ordering[1:], 1):
            for this_nt in nt_ordering[:idx]:
                for this_derived in self.nt_rules[this_nt]:  # detect forward derivation
                    if this_derived[0] == nt(end_nt):  # forward derivation detected
                        new_derives = []
                        for end_derived in self.nt_rules[end_nt]:  # rewrite every rule
                            if end_derived[0] == nt(this_nt):
                                for dr in self.nt_rules[this_nt]:
                                    new_derives.append(dr + end_derived[1:])
                            else:
                                new_derives.append(end_derived)
                        self.nt_rules[end_nt] = new_derives
                        break

    def elim_lr(self):
        self.elim_indir_lr()
        for ntid in self.nt_rules:
            self.rewrite_rule(ntid)

    def calc_parse_table(self):
        follow_sets = self.calc_follow_sets()
        parse_table = {ntid: {} for ntid in self.nt_rules}
        for ntid, derives_list in self.nt_rules.items():
            for derives in derives_list:
                first_set_seq = self.calc_first_set_seq(derives)
                if epsilon in first_set_seq:
                    first_plus_set = first_set_seq | follow_sets[ntid]
                else:
                    first_plus_set = first_set_seq
                for category in first_plus_set:
                    if category not in parse_table[ntid]:
                        parse_table[ntid][category] = derives
                    else:
                        raise RuntimeError(f'conflict lookahead rules: {parse_table[ntid][category]}, {derives}')

        return parse_table
