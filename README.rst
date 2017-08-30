Linguist: Getting Started
=========================
Linguist is an LALR(1) compiler-compiler that is built upon itself

A quick example:

.. code-block:: python

    from linguist import LangBuilder

    lb = LangBuilder()
    lb.lex('PLUS', r'\+')   # add a lexical rule by specifying its regular expression
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

Use lex(name, pattern, skip=True) to add a lexical rule

You can use it as a decorator to associate an action with the rule

The wrapped function must have the signature fn(lexeme), where lexeme is the captured text

If no action is specified, the lexeme is returned unaltered

Use rule(bnf) to add a grammatical rule

You can use it as a decorator to associate an action with **each** production rule specified in the bnf

The wrapped function must have the signature fn(data_list, repo), where repo is the external repository (ie. a symbol table) specified before the parsing (see below)

If no action is specified, **None** is returned

After the rules are specified, use build() to build the scanner and parser

use scanner.tokens(text) to tokenize the text, then use parser.parse(tokens, repo=None) to perform the parsing

The *repo* parameter will be passed to each action