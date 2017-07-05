import warnings


class Scanner:
    def __init__(self, dfa, category_info):
        if dfa.starting_state in dfa.accepting_states:
            warnings.warn('DFA accepts empty string')
        self.dfa = dfa
        self.category_info = category_info

    def tokens(self, text):
        index = 0
        limit = len(text)

        def next_token():
            nonlocal index
            end = index
            state = self.dfa.starting_state
            states = [state]
            while end < limit and state is not None:  # eat
                char = text[end]
                state = self.dfa.trans_matrix[state][char]
                states.append(state)
                end += 1

            state = states.pop()
            while state not in self.dfa.accepting_states and index < end:  # spit
                state = states.pop()
                end -= 1

            if index < end:  # found lexeme
                token = (self.dfa.accepting_states[state],
                         text[index:end])
                index = end
                return token
            else:
                raise RuntimeError(f"unknown token near position {end}")

        while index < limit:
            yield next_token()
