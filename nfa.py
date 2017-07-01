from collections import defaultdict


class NFA:
    epsilon = None

    def __init__(self):
        self.trans_matrix = {}
        self.starting_state = None
        self.accepting_states = set()
        self.alphabet = set()

    def add_state(self, state, starting=False, accepting=False):
        if state in self.trans_matrix:
            raise ValueError(f'state {state} already in NFA')
        else:
            self.trans_matrix[state] = defaultdict(set)

            if starting:
                if self.starting_state is None:
                    self.starting_state = state
                else:
                    raise ValueError(f'starting state already set to {self.starting_state} in NFA')

            if accepting:
                self.accepting_states.add(state)

    def add_transition(self, begin, end, char):
        if begin not in self.trans_matrix:
            raise ValueError(f'begin state {begin} not in NFA')
        elif end not in self.trans_matrix:
            raise ValueError(f'end state {end} not in NFA')
        else:
            self.trans_matrix[begin][char].add(end)
            if char != self.epsilon:
                self.alphabet.add(char)
