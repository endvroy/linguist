import warnings
from metachar import eof
from scanner.nfa_to_dfa import nfa_to_dfa
from scanner.minimize_dfa import minimize_dfa


def scanner_builder(nfa, category_info):
    dfa = nfa_to_dfa(nfa, category_info)
    min_dfa = minimize_dfa(dfa)
    scanner = Scanner(min_dfa, category_info)
    return scanner


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
                raise RuntimeError(f"illegal char near position {end}")

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
