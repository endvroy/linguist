# Linguist

## Introduction

Linguist is an LALR(1)[1] compiler-compiler[2] that is built upon itself. In Linguist, you can define syntax rules and grammar rules for your language. With these rules, Linguist can parse the input expression and generate its result.

The implementation of Linguist is in `Python3`, please make sure you have `Python3` installed.

## Features

**1. Define Lexical Rules**

Lexical rules can be added with `lb.lex(name, pattern, skip=True)`.

If `lb.lex` is defined as a decorator (`@`) of a function, the function is associated to the rule. This function **must** have the signature `fn(lexeme)`, where `lexeme` is the captured text. If no action is specified, `lexeme` itself is returned.

**2. Define Grammar Rules**

Grammar rules can be added with `lb.rule(bnf)`. 

If `lb.rule` is defined as a decorator (`@`) of a function, the function is associated to **each** rule specified in `bnf`. This function **must** have the signature `fn(data_list, repo)`, where `repo` is the external repository specified before the parsing, like a symbol table. If no action is specified, **None** is returned.

**3. Language Builder**

The function `build()` can build the scanner and the parser of your language. To scan the expression in text, use `scanner.tokens(text)`. To parse the expression, use `parser.parse(tokens, repo=None)`.

Note that the parameter `repo` should be passed to **each action**.

## How To Use

This section shows sample code for using Linguist. You can refer to this section when you create your own language.

**1. Import Linguist**

~~~~python
from linguist import LangBuilder
~~~~

**2. Define Lexical Rules**

~~~~python
lb = LangBuilder()

# add a lexical rule by specifying its regular expression
lb.lex('PLUS', r'\+')   
lb.lex('MINUS', '-')
lb.lex('TIMES', r'\*')
lb.lex('DIVIDE', '/')
lb.lex('LPAREN', r'\(')
lb.lex('RPAREN', r'\)')

# add skipped tokens
lb.lex('BLANK', '[ \n\t]+', skip=True) 

# add a lexical rule and associate with an action
@lb.lex('NUM', '[0-9]+')
def rule_NUM(lexeme):
    return int(lexeme)
~~~~

**3. Add Grammar Rules**
~~~~ python
lb.goal('expr') # set the goal symbol

# add a grammar rule and associate with an action
@lb.rule('expr = expr PLUS term')   
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
~~~~

**4. Build Language**
~~~~python
scanner, parser = lb.build()    # build the language
~~~~

**5. Test On Expressions**
~~~~python
tokens = scanner.tokens('3 + 4 * 5')
result = parser.parse(tokens)   # Result is 23

tokens = scanner.tokens('(3 + 4) * 5')
result = parser.parse(tokens)   # Result is 35
~~~~

## Reference

1. A Tutorial Explaining LALR(1) Parsing: [https://web.cs.dal.ca/~sjackson/lalr1.html](https://web.cs.dal.ca/~sjackson/lalr1.html)
2. Compiler-compiler - Wikipedia: [https://en.wikipedia.org/wiki/Compiler-compiler](https://en.wikipedia.org/wiki/Compiler-compiler)
