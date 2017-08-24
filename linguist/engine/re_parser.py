from linguist.base.scanner.scanner import CategoryInfo

import linguist.base.scanner.re_utils as re_utils
from linguist.engine.partial_builder import PartialBuilder

pb = PartialBuilder()
pb.goal('alt')


# alt
@pb.rule('alt = alt ALT_DELIM cat')
def rule_alt(data_list, repo):
    return re_utils.alt([data_list[0], data_list[2]])


@pb.rule('alt = cat')
def rule_alt_base(data_list, repo):
    return data_list[0]


# cat
@pb.rule('cat = cat cat_elmt')
def rule_cat(data_list, repo):
    return re_utils.cat(data_list)


@pb.rule('cat = cat_elmt')
def rule_cat_base(data_list, repo):
    return data_list[0]


@pb.rule('''cat_elmt = k_closure
                        | p_closure
                        | opt_closure
                        | basic_elmt''')
def rule_cat_elmt(data_list, repo):
    return data_list[0]


# k_closure
@pb.rule('k_closure = basic_elmt STAR')
def rule_k_closure(data_list, repo):
    return re_utils.k_closure(data_list[0])


# p_closure
@pb.rule('p_closure = basic_elmt PLUS')
def rule_p_closure(data_list, repo):
    return re_utils.p_closure(data_list[0])


# opt_closure
@pb.rule('opt_closure = basic_elmt QMARK')
def rule_opt_closure(data_list, repo):
    return re_utils.opt_closure(data_list[0])


# basic_elmt
@pb.rule('''basic_elmt = char_set
                        | grp''')
def rule_basic_elmt(data_list, repo):
    return data_list[0]


@pb.rule('basic_elmt = char')
def rule_basic_elmt_char(data_list, repo):
    return re_utils.atom(data_list[0], repo)


# char
@pb.rule('''char = literal
                    | esc_char''')
def rule_char(data_list, repo):
    return data_list[0]


# literal
@pb.rule('''literal = NOT_RESERVED
                        | CARET
                        | DASH''')
def rule_literal(data_list, repo):
    return data_list[0]


# esc_char
@pb.rule('''esc_char = BSLASH LPAREN
                        | BSLASH RPAREN
                        | BSLASH LBRACKET
                        | BSLASH RBRACKET
                        | BSLASH STAR
                        | BSLASH DOT
                        | BSLASH PLUS
                        | BSLASH QMARK
                        | BSLASH BSLASH
                        | BSLASH ALT_DELIM''')
def rule_esc_char(data_list, repo):
    return data_list[1]


# grp
@pb.rule('grp = LPAREN alt RPAREN')
def rule_grp(data_list, repo):
    return data_list[1]


# char_set
@pb.rule('''char_set = pos_set 
                        | neg_set''')
def rule_char_set(data_list, repo):
    return data_list[0]


# pos_set
@pb.rule('pos_set = LBRACKET pos_lang RBRACKET')
def rule_pos_set(data_list, repo):
    return re_utils.char_set(*data_list[1], repo)


# neg_set
@pb.rule('neg_set = LBRACKET CARET neg_lang RBRACKET')
def rule_neg_set(data_list, repo):
    return re_utils.neg_set(*data_list[2], repo)


# pos_lang
@pb.rule('''pos_lang = set_char remaining
                        | DASH remaining''')
def rule_pos_lang(data_list, repo):
    data_list[0] = re_utils.char_member(data_list[0])
    if data_list[1] is None:
        return data_list[0]
    else:
        return re_utils.merge_members(data_list)


@pb.rule('pos_lang = char_range remaining')
def rule_pos_lang_range(data_list, repo):
    if data_list[1] is None:
        return data_list[0]
    else:
        return re_utils.merge_members(data_list)


# neg_lang
@pb.rule('''neg_lang = set_char remaining
                        | DASH remaining
                        | CARET remaining''')
def rule_pos_lang(data_list, repo):
    data_list[0] = re_utils.char_member(data_list[0])
    if data_list[1] is None:
        return data_list[0]
    else:
        return re_utils.merge_members(data_list)


@pb.rule('neg_lang = char_range remaining')
def rule_pos_lang_range(data_list, repo):
    if data_list[1] is None:
        return data_list[0]
    else:
        return re_utils.merge_members(data_list)


# set_char
@pb.rule('''set_char = NOT_RESERVED
                        | esc_set_char
                        | LPAREN
                        | RPAREN
                        | LBRACKET
                        | STAR
                        | DOT
                        | PLUS
                        | QMARK
                        | ALT_DELIM''')
def rule_set_char(data_list, repo):
    return data_list[0]


# esc_set_char
@pb.rule('''esc_set_char = BSLASH RBRACKET
                            | BSLASH BSLASH
                            | BSLASH CARET
                            | BSLASH DASH''')
def rule_esc_set_char(data_list, repo):
    return data_list[1]


# remaining
@pb.rule('remaining = remaining char_range')
def rule_remaining_char_range(data_list, repo):
    if data_list[0] is None:
        return data_list[1]
    else:
        return re_utils.merge_members(data_list)


@pb.rule('''remaining = remaining set_char
                        | remaining CARET''')
def rule_remaining(data_list, repo):
    data_list[1] = re_utils.char_member(data_list[1])
    if data_list[0] is None:
        return data_list[1]
    else:
        return re_utils.merge_members(data_list)


pb.rule('remaining = ')


# char_range
@pb.rule('char_range = set_char DASH set_char')
def rule_char_range(data_list, repo):
    return re_utils.char_range(data_list[0], data_list[2])


# prepare the category info
category_info = [CategoryInfo('LPAREN', -1),
                 CategoryInfo('RPAREN', -2),
                 CategoryInfo('LBRACKET', -3),
                 CategoryInfo('RBRACKET', -4),
                 CategoryInfo('STAR', -5),
                 CategoryInfo('PLUS', -6),
                 CategoryInfo('QMARK', -7),
                 CategoryInfo('BSLASH', -8),
                 CategoryInfo('ALT_DELIM', -9),
                 CategoryInfo('CARET', -10),
                 CategoryInfo('DASH', -11),
                 CategoryInfo('DOT', -12),
                 CategoryInfo('NOT_RESERVED', -13)]

# prepare the NFAs
LPAREN = 0
RPAREN = 1
LBRACKET = 2
RBRACKET = 3
STAR = 4
PLUS = 5
QMARK = 6
BSLASH = 7
ALT_DELIM = 8
CARET = 9
DASH = 10
DOT = 11
NOT_RESERVED = 12

lparen = re_utils.atom('(', LPAREN)
rparen = re_utils.atom(')', RPAREN)
lbracket = re_utils.atom('[', LBRACKET)
rbracket = re_utils.atom(']', RBRACKET)
star = re_utils.atom('*', STAR)
plus = re_utils.atom('+', PLUS)
qmark = re_utils.atom('?', QMARK)
bslash = re_utils.atom('\\', BSLASH)
alt_delim = re_utils.atom('|', ALT_DELIM)
caret = re_utils.atom('^', CARET)
dash = re_utils.atom('-', DASH)
dot = re_utils.atom('.', DOT)
not_reserved = re_utils.dot(NOT_RESERVED)

# hack in the NFA list, category_info, and name_map
pb.nfa_list = [lparen,
               rparen,
               lbracket,
               rbracket,
               star,
               plus,
               qmark,
               bslash,
               alt_delim,
               caret,
               dash,
               dot,
               not_reserved]
pb.category_info = category_info

for i, cinfo in enumerate(category_info):
    pb.name_map[cinfo.name] = ('t', i)

re_scanner, re_parser = pb.build()
