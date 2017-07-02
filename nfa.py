from collections import defaultdict


class NFA:
    epsilon = None

    def __init__(self):
        self.trans_matrix = {}
        self.starting_state = None
        self.accepting_states = {}
        self.alphabet = set()

    def copy(self):
        nfa = NFA()
        nfa.trans_matrix = self.trans_matrix.copy()
        nfa.starting_state = self.starting_state
        nfa.accepting_states = self.accepting_states.copy()
        nfa.alphabet = self.alphabet.copy()
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
        if char != self.epsilon:
            self.alphabet.add(char)


# todo: test
def cat(nfa_list):
    cat_nfa = NFA()
    for i, nfa in enumerate(nfa_list):  # add everything to cat_nfa
        for start, d in nfa.trans_matrix.items():
            cat_nfa.add_state((i, start))
            for char, end_set in d.items():
                for end in end_set:
                    cat_nfa.add_transition((i, start), (i, end), char)
        cat_nfa.alphabet |= nfa.alphabet

    for i in range(len(nfa_list) - 1):  # link these nfa
        this = nfa_list[i]
        next_ = nfa_list[i + 1]
        for state in this.accepting_states:
            cat_nfa.add_transition((i, state),
                                   (i + 1, next_.starting_state),
                                   cat_nfa.epsilon)

    cat_nfa.mark_starting((0, nfa_list[0].starting_state))
    for state, category in nfa_list[-1].accepting_states.items():
        cat_nfa.mark_accepting((len(nfa_list) - 1, state), category)

    return cat_nfa


def alt(nfa_list):
    alt_nfa = NFA()
    for i, nfa in enumerate(nfa_list):
        for start, d in nfa.trans_matrix.items():
            alt_nfa.add_state((i, start))
            for char, end_set in d.items():
                for end in end_set:
                    alt_nfa.add_transition((i, start), (i, end), char)
        alt_nfa.alphabet |= nfa.alphabet
        for state, category in nfa.accepting_states.items():
            alt_nfa.mark_accepting((i, state), category)

    alt_nfa.add_state(1)  # starting state
    for i, nfa in enumerate(nfa_list):
        alt_nfa.add_transition(1,
                               (i, nfa.starting_state),
                               alt_nfa.epsilon)

    alt_nfa.mark_starting(1)

    return alt_nfa


def closure(nfa: NFA):
    c_nfa = nfa.copy()
    for state in c_nfa.accepting_states:
        c_nfa.add_transition(c_nfa.starting_state,
                             state,
                             c_nfa.epsilon)
        c_nfa.add_transition(state,
                             c_nfa.starting_state,
                             c_nfa.epsilon)
    return c_nfa
