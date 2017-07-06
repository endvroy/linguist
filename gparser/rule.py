class RuleSet:
    def __init__(self):
        self.nt_rules = {}
        self._nt_index = 0

    def new_nt(self, num):
        specifiers = list(range(self._nt_index, self._nt_index + num))
        for i in range(self._nt_index, self._nt_index + num):
            self.nt_rules[i] = []
        self._nt_index += num
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
        self.add_rule(tmp, d())


def nt(ntid):
    return 'nt', ntid


def t(category):
    return 't', category


def d(*seq):  # derived sequence
    return tuple(seq)
