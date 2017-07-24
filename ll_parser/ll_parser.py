from ll_parser.rule import eof, t, nt


class LLParser:
    def __init__(self, rule_set):
        self.rule_set = rule_set
        self.rule_set.elim_lr()
        self.parse_table = self.rule_set.calc_parse_table()

    def parse(self, token_stream):
        tokens = gen_tokens(token_stream)
        token = next(tokens)
        stack = [t(eof), nt(self.rule_set.goal)]
        while True:
            focus = stack[-1]
            if focus == t(eof) and token[0] == eof:
                break  # todo: return the parse tree
            elif focus[0] == 't':
                if token[0] == focus[1]:  # categories match
                    stack.pop()
                    token = next(tokens)
                else:
                    raise RuntimeError(f'parse error: {token[0]} expected')
            else:
                try:
                    derives = self.parse_table[focus[1]][token[0]]
                except KeyError:
                    raise RuntimeError(f'parse error: {token[0]} expected')
                stack.pop()
                for x in reversed(derives):
                    stack.append(x)


def gen_tokens(token_stream):
    for token in token_stream:
        yield token
    yield (eof, '')
