class CategoryInfo:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __repr__(self):
        return f'CategoryInfo({self.name}, {self.priority})'


class Scanner:
    def __init__(self, dfa, category_info):
        self.dfa = dfa
        self.category_info = category_info
        # self.text = text
        # self.index = 0
        # self.limit = len(self.text)

    # todo : fill in
    def decide_category(self, categories):
        return max(categories, key=lambda x: self.category_info[x].priority)

    # todo: test
    # def next_token(self):
    #     end = self.index
    #     state = self.dfa.starting_state
    #     states = [state]
    #     while end < self.limit and state is not None:  # eat
    #         char = self.text[end]
    #         state = self.dfa.trans_matrix[state][char]
    #         states.append(state)
    #         end += 1
    #
    #     while state not in self.dfa.accepting_states and self.index < end:  # spit
    #         state = states.pop()
    #         end -= 1
    #
    #     lexeme = self.text[self.index:end]
    #
    #     if self.index < end:  # found lexeme
    #         token = (self.decide_category(self.dfa.accepting_states[state]),
    #                  lexeme)
    #         self.index = end
    #         return token
    #     else:
    #         raise RuntimeError(f'unknown token {lexeme}')

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

            lexeme = text[index:end]

            if index < end:  # found lexeme
                token = (self.decide_category(self.dfa.accepting_states[state]),
                         lexeme)
                index = end
                return token
            else:
                raise RuntimeError(f"unknown token '{lexeme}' near position {end}")

        while index < limit:
            yield next_token()
