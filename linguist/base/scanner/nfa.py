import copy
from collections import defaultdict

from linguist.base.metachar import epsilon


class NFA:
    def __init__(self):
        self.trans_matrix = {}
        self.starting_state = None
        self.accepting_states = {}
        self.alphabet = set()
        self.classifier = None

    def copy(self):
        nfa = NFA()
        nfa.trans_matrix = copy.deepcopy(self.trans_matrix)
        nfa.starting_state = self.starting_state
        nfa.accepting_states = self.accepting_states.copy()
        nfa.alphabet = self.alphabet.copy()
        if self.classifier is not None:
            nfa.classifier = self.classifier.copy()
        else:
            nfa.classifier = None
        return nfa

    def add_state(self, state):
        if state not in self.trans_matrix:
            self.trans_matrix[state] = defaultdict(set)

    def mark_starting(self, state):
        if state not in self.trans_matrix:
            raise ValueError(f'state {state} not in NFA')
        else:
            self.starting_state = state

    def mark_accepting(self, state, category_id):
        if state not in self.trans_matrix:
            raise ValueError(f'state {state} not in NFA')
        else:
            self.accepting_states[state] = category_id

    def add_transition(self, begin, end, char):
        # if begin not in self.trans_matrix:
        #     raise ValueError(f'begin state {begin} not in NFA')
        # elif end not in self.trans_matrix:
        #     raise ValueError(f'end state {end} not in NFA')
        # else:
        self.trans_matrix[begin][char].add(end)
        if char != epsilon:
            self.alphabet.add(char)
