epsilon = None


class RuleSet:
    def __init__(self):
        self.nt_rules = {}
        self._next_ntid = 0

    def new_nt(self, num):
        specifiers = list(range(self._next_ntid, self._next_ntid + num))
        for i in range(self._next_ntid, self._next_ntid + num):
            self.nt_rules[i] = []
        self._next_ntid += num
        return specifiers

    def add_rule(self, ntid, derives):
        self.nt_rules[ntid].append(derives)

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

    def calc_first_sets(self):
        first_sets = {ntid: set() for ntid in self.nt_rules}

        def first(x):
            if x[0] == 't':
                return {x[1]}
            else:
                return first_sets[x[1]]

        changed = True
        while changed:
            changed = False
            for ntid, derives_list in self.nt_rules.items():
                for derives in derives_list:
                    trailer = set()
                    for x in derives:
                        trailer |= (first(x) - {epsilon})
                        if epsilon not in first(x):
                            break
                    else:
                        if epsilon in first(derives[-1]):
                            trailer.add(epsilon)

                    new_set = first_sets[ntid] | trailer
                    if len(new_set) != len(first_sets[ntid]):
                        changed = True
                        first_sets[ntid] = new_set

        return first_sets

    # todo: fill in
    def calc_follow_sets(self, first_sets):
        pass


def nt(ntid):
    return 'nt', ntid


def t(category):
    return 't', category


def d(*seq):  # derived sequence
    return tuple(seq)
