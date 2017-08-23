import scanner.re_utils as re_utils
from scanner.scanner import CategoryInfo, scanner_builder
from lalr_parser.rule_set import LALRRuleSet, d, t, nt
from metachar import epsilon
from lalr_parser.parser import LALRParser

category_info = {
    2: CategoryInfo('NAME', -2),
    3: CategoryInfo('BLANK', -3, 'skip'),
    4: CategoryInfo('EQ', -4),
    5: CategoryInfo('ALT_DELIM', -5)}

NAME = 2
BLANK = 3
EQ = 4
ALT_DELIM = 5

a = re_utils.char_range('a', 'z')
b = re_utils.char_range('A', 'Z')
c = re_utils.char_member('_')
markers, accept = re_utils.merge_members([a, b, c])
first = re_utils.char_set(markers, accept, NAME)

digits = re_utils.char_range('0', '9')
markers, accept = re_utils.merge_members([a, b, c, digits])
following = re_utils.char_set(markers, accept, NAME)
following = re_utils.k_closure(following)
name = re_utils.cat([first, following])

blank = re_utils.alt([re_utils.atom(' ', BLANK),
                      re_utils.atom('\n', BLANK),
                      re_utils.atom('\t', BLANK)])

eq = re_utils.atom('=', EQ)

alt_delim = re_utils.atom('|', ALT_DELIM)

nfa = re_utils.alt([name, blank, eq, alt_delim])

scanner = scanner_builder(nfa, category_info)

rule_set = LALRRuleSet()
bnf, alt, dlist = rule_set.new_nt(3)
rule_set.mark_goal(bnf)

rule_actions = {}

rule_set.add_rule(bnf, d(t(NAME), t(EQ), nt(alt)))


def rule_bnf(data_list, repo):
    return data_list[0], data_list[2]


rule_actions[(bnf, 0)] = rule_bnf
rule_set.add_rule(alt, d(nt(alt), t(ALT_DELIM), nt(dlist)))


def rule_alt(data_list, repo):
    return data_list[0] + [data_list[2]]


rule_actions[(alt, 0)] = rule_alt

rule_set.add_rule(alt, d(nt(dlist)))


def rule_alt_base(data_list, repo):
    return [data_list[0]]


rule_actions[(alt, 1)] = rule_alt_base

rule_set.add_rule(dlist, d(nt(dlist), t(NAME)))


def rule_dlist(data_list, repo):
    return data_list[0] + (data_list[1],)


rule_actions[(dlist, 0)] = rule_dlist

rule_set.add_rule(dlist, d(t(epsilon)))


def rule_dlist_base(data_list, repo):
    return ()


rule_actions[(dlist, 1)] = rule_dlist_base

parser = LALRParser(rule_set, rule_actions)
