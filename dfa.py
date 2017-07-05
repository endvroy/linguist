class DFA:
    def __init__(self,
                 trans_matrix,
                 starting_state,
                 accepting_states,
                 alphabet):
        self.trans_matrix = trans_matrix
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        self.alphabet = alphabet


class CategoryInfo:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __repr__(self):
        return f'CategoryInfo({self.name}, {self.priority})'
