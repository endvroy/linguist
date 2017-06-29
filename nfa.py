from collections import defaultdict


class NFA:
    epsilon = None

    def __init__(self):
        self.trans_matrix = {}
        self.accepting_states = set()
        self.starting_state = None
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

    def epsilon_closure(self, states):
        closure = set(states)
        working_set = set(states)

        while True:
            new_working_set = set()
            for s in working_set:
                for new_state in self.trans_matrix[s][self.epsilon]:
                    if new_state not in closure:
                        closure.add(new_state)
                        new_working_set.add(new_state)
            if new_working_set:
                working_set = new_working_set
            else:
                break

        return closure

    def _next_set(self, states, char):
        """the set immediately obtained from state in states on char, without epsilon closure"""
        next_set = set()
        for state in states:
            if char in self.trans_matrix[state]:
                next_set |= self.trans_matrix[state][char]
        return next_set

    def to_dfa(self):
        trans_matrix = {}
        accepting_states = set()
        working_list = [frozenset(self.epsilon_closure({self.starting_state}))]

        while working_list:
            states = working_list.pop()
            trans_matrix[states] = {}

            for char in self.alphabet:
                next_set = self._next_set(states, char)
                new_states = self.epsilon_closure(next_set)

                if new_states:
                    new_states = frozenset(new_states)
                    for state in new_states:
                        if state in self.accepting_states:
                            accepting_states.add(new_states)

                    trans_matrix[states][char] = new_states
                    if new_states not in trans_matrix.keys():
                        working_list.append(new_states)

        return trans_matrix, accepting_states
