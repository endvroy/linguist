import warnings
from metachar import eof


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
                char_class = self.dfa.classifier.classify(char)
                state = self.dfa.trans_matrix[state][char_class]
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
            token = next_token()
            action = self.category_info[token[0]].action
            if action == 'skip':
                continue
            elif action is not None:
                token = token[0], action(token[1])
            yield token
        yield (eof, '')


class CategoryInfo:
    def __init__(self, name, priority, action=None):
        self.name = name
        self.priority = priority
        self.action = action

    def __repr__(self):
        return f'CategoryInfo({self.name}, {self.priority}, {self.action})'