# Linguist

## Introduction

Linguist is an LALR(1)[1] compiler-compiler[2] that is built upon itself. In Linguist, you can define your own language by supplying the corresponding syntax rules and grammar rules. Linguist generates a parser with the supplied rules, which can then parse the input expression and generate its result.

Linguist is implemented in `Python3`.

## Usage

**1. Define Lexical Rules**

Lexical rules can be added with `lb.lex(name, pattern, skip=True)`.

If `lb.lex` is defined as a decorator (`@`) of a function, the function is associated to the rule. This function **must** have the signature `fn(lexeme)`, where `lexeme` is the captured text. The return value of the function will be the value of the token. If no action is specified, `lexeme` itself is returned.

**2. Define Grammar Rules**

Grammar rules can be added with `lb.rule(bnf)`. 

If `lb.rule` is defined as a decorator (`@`) of a function, the function is associated to **each** rule specified in `bnf`. This function **must** have the signature `fn(data_list, repo)`, where `repo` is the external repository, such as a symbol table. If no funciton is decorated is specified, **None** is returned.

**3. Language Builder**

After the lexical rules and grammatical rules are specified, call `build()` to build the scanner and the parser for the specified language. To tokenize the input, use `scanner.tokens(text)`. To parse the tokens, use `parser.parse(tokens, repo)`.

Note that the parameter `repo` should be passed to **each action**.

## Example

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
result = parser.parse(tokens)   # result = 23

tokens = scanner.tokens('(3 + 4) * 5')
result = parser.parse(tokens)   # result = 35
~~~~

## Reference

1. LALR Parsing: [https://web.stanford.edu/class/archive/cs/cs143/cs143.1128/handouts/140%20LALR%20Parsing.pdf](https://web.stanford.edu/class/archive/cs/cs143/cs143.1128/handouts/140%20LALR%20Parsing.pdf)
2. Compiler-compiler - Wikipedia: [https://en.wikipedia.org/wiki/Compiler-compiler](https://en.wikipedia.org/wiki/Compiler-compiler)
