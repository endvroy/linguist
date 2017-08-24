class DFA:
    def __init__(self,
                 trans_matrix,
                 starting_state,
                 accepting_states,
                 alphabet,
                 classifier):
        self.trans_matrix = trans_matrix
        self.starting_state = starting_state
        self.accepting_states = accepting_states
        self.alphabet = alphabet
        self.classifier = classifier
