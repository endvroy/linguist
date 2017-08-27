Linguist: Getting Started
=========================
linguist is an LALR(1) compiler-compiler that is built upon itself

.. code-block:: python
    from linguist import LangBuilder

    lb = LangBuilder()
    lb.lex('PLUS', r'\+')   # add a lexical rule
    lb.lex('MINUS', '-')
    lb.lex('TIMES', r'\*')
    lb.lex('DIVIDE', '/')
    lb.lex('LPAREN', r'\(')
    lb.lex('RPAREN', r'\)')
    lb.lex('BLANK', '[ \n\t]+', skip=True)  # add skipped tokens

    @lb.lex('NUM', '[0-9]+')    # add a lexical rule and associate with an action
    def rule_NUM(lexeme):
        return int(lexeme)

    lb.goal('expr') # set the goal symbol

    @lb.rule('expr = expr PLUS term')   # add a grammar rule and associate with an action
    def rule_add(data_list, repo):  # repo is an external repository
        return data_list[0] + data_list[2]

    @lb.rule('expr = expr MINUS term')
    def rule_minus(data_list, repo):
        return data_list[0] - data_list[2]

    @lb.rule('expr = term')
    def rule_expr(data_list, repo):
        return data_list[0]

    @lb.rule('term = term TIMES factor')
    def rule_times(data_list, repo):
        return data_list[0] * data_list[2]

    @lb.rule('term = term DIVIDE factor')
    def rule_divide(data_list, repo):
        return data_list[0] / data_list[2]

    @lb.rule('term = factor')
    def rule_term(data_list, repo):
        return data_list[0]

    @lb.rule('factor = NUM')
    def rule_factor(data_list, repo):
        return data_list[0]

    @lb.rule('factor = LPAREN expr RPAREN')
    def rule_factor_expr(data_list, repo):
        return data_list[1]

    scanner, parser = lb.build()    # build the language

    tokens = scanner.tokens('3 + 4 * 5')
    result = parser.parse(tokens)   # 23

    tokens = scanner.tokens('(3 + 4) * 5')
    result = parser.parse(tokens)   # 35
