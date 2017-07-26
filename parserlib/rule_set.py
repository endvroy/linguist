from metachar import epsilon, eof


class RuleSet:
    def __init__(self):
        self.nt_rules = {}
        self.goal = None
        self._next_ntid = 0
        self.first_sets = None
        self.follow_sets = None

    def new_nt(self, num):
        specifiers = list(range(self._next_ntid, self._next_ntid + num))
        for i in range(self._next_ntid, self._next_ntid + num):
            self.nt_rules[i] = []
        self._next_ntid += num
        return specifiers

    def mark_goal(self, ntid):
        self.goal = ntid

    def add_rule(self, ntid, derives):
        self.nt_rules[ntid].append(derives)

    def calc_first_sets(self):
        first_sets = {ntid: set() for ntid in self.nt_rules}

        first = first_fn(first_sets)

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

        self.first_sets = first_sets
        return first_sets

    def calc_follow_sets(self):
        if self.first_sets is None:
            self.calc_first_sets()
        first = first_fn(self.first_sets)

        follow_sets = {ntid: set() for ntid in self.nt_rules}
        follow_sets[self.goal].add(eof)

        changed = True
        while changed:
            changed = False
            for ntid, derives_list in self.nt_rules.items():
                for derives in derives_list:
                    trailer = follow_sets[ntid].copy()
                    for x in reversed(derives):
                        if x[0] == 'nt':
                            new_set = follow_sets[x[1]] | trailer
                            if len(new_set) != len(follow_sets[x[1]]):
                                changed = True
                                follow_sets[x[1]] = new_set

                            if epsilon in first(x):
                                trailer |= (first(x) - {epsilon})
                            else:
                                trailer = first(x)
                        else:
                            trailer = first(x)

        self.follow_sets = follow_sets
        return follow_sets

    def calc_first_set_seq(self, d_seq):
        if self.first_sets is None:
            self.calc_first_sets()

        first = first_fn(self.first_sets)

        f_set = set()
        for symbol in d_seq:
            f_set |= first(symbol)
            if epsilon not in first(symbol):
                f_set -= {epsilon}
                break
        return f_set


def nt(ntid):
    return 'nt', ntid


def t(category):
    return 't', category


def d(*seq):  # derived sequence
    return tuple(seq)


def first_fn(first_sets):
    def first(x):
        if x[0] == 't':
            return {x[1]}
        else:
            return first_sets[x[1]]

    return first
