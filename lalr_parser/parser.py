from lalr_parser.rule_set import Action, t, nt


class LALRParser:
    def __init__(self, rule_set, rule_actions):
        self.rule_set = rule_set
        self.action, self.goto = self.rule_set.calc_parse_table()
        self.rule_actions = rule_actions

    def parse(self, tokens):
        tokens = iter(tokens)
        data_stack = [None]
        state_stack = [0]
        token = next(tokens)
        while True:
            state = state_stack[-1]
            if token[0] not in self.action[state]:
                raise RuntimeError  # error
            else:
                action = self.action[state][token[0]]
                if action[0] == Action.accept:
                    ntid, rule_id = action[1:]
                    derives = self.rule_set.nt_rules[ntid][rule_id]
                    split_point = -len(derives)
                    data_list = data_stack[split_point:]
                    if self.rule_actions[(ntid, rule_id)] is not None:
                        data = self.rule_actions[(ntid, rule_id)](data_list)
                    else:
                        data = None
                    return data

                elif action[0] == Action.shift:
                    data_stack.append(token[1])
                    state_stack.append(self.goto[state][t(token[0])])
                    token = next(tokens)

                elif action[0] == Action.reduce:
                    ntid, rule_id = action[1:]
                    derives = self.rule_set.nt_rules[ntid][rule_id]
                    split_point = -len(derives)
                    data_list = data_stack[split_point:]
                    data_stack = data_stack[:split_point]
                    state_stack = state_stack[:split_point]
                    # perform actions
                    if self.rule_actions[(ntid, rule_id)] is not None:
                        data = self.rule_actions[(ntid, rule_id)](data_list)
                    else:
                        data = None
                    data_stack.append(data)
                    state = state_stack[-1]
                    state_stack.append(self.goto[state][nt(ntid)])
                else:
                    raise RuntimeError  # error
