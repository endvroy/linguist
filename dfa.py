class DFA:
    def __init__(self):
        self.trans_matrix = {}
        self.accepting_states = set()
        self.starting_state = None
        self.alphabet = set()
