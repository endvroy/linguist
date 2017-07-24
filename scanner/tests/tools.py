from graphviz import Digraph
from scanner.nfa import NFA
from scanner.dfa import DFA
from scanner.nfa_to_dfa import dict_to_dfa_matrix
from metachar import epsilon
import os


def build_test_nfa():  # example NFA on EC pp.51
    nfa = NFA()
    for i in range(10):
        nfa.add_state(i)
    nfa.mark_starting(0)
    nfa.mark_accepting(9, 1)

    nfa.add_transition(0, 1, 'a')
    nfa.add_transition(1, 2, epsilon)
    nfa.add_transition(2, 9, epsilon)
    nfa.add_transition(2, 3, epsilon)
    nfa.add_transition(3, 4, epsilon)
    nfa.add_transition(3, 6, epsilon)
    nfa.add_transition(4, 5, 'b')
    nfa.add_transition(5, 8, epsilon)
    nfa.add_transition(6, 7, 'c')
    nfa.add_transition(7, 8, epsilon)
    nfa.add_transition(8, 3, epsilon)
    nfa.add_transition(8, 9, epsilon)

    return nfa


def build_nfa1():  # NFA on page 151 of the Dragon Book
    nfa = NFA()
    for i in range(4):
        nfa.add_state(i)
    nfa.add_transition(0, 0, 'b')
    nfa.add_transition(0, 1, 'a')
    nfa.add_transition(1, 1, 'a')
    nfa.add_transition(1, 2, 'b')
    nfa.add_transition(2, 1, 'a')
    nfa.add_transition(2, 3, 'b')
    nfa.add_transition(3, 0, 'b')
    nfa.add_transition(3, 1, 'a')
    nfa.mark_starting(0)
    nfa.mark_accepting(3, 0)
    return nfa


def build_test_dfa():  # example DFA on page 56
    dfa = DFA(dict_to_dfa_matrix({0: {'f': 1},
                                  1: {'e': 2,
                                      'i': 4},
                                  2: {'e': 3},
                                  3: {},
                                  4: {'e': 5},
                                  5: {}}),
              0,
              {3: 42, 5: 42},
              {'f', 'e', 'i'})
    return dfa


def build_test_dfa_2():
    dfa = DFA(dict_to_dfa_matrix({0: {'a': 2,
                                      'i': 1,
                                      'f': 2},
                                  1: {'a': 2,
                                      'i': 2,
                                      'f': 3},
                                  2: {'a': 2,
                                      'i': 2,
                                      'f': 2},
                                  3: {'a': 2,
                                      'i': 2,
                                      'f': 2}}),
              0,
              {1: 'id', 2: 'id', 3: 'if'},
              {'a', 'i', 'f'})
    return dfa


def draw_nfa(nfa, name):
    os.makedirs('figures', exist_ok=True)
    fname = 'figures/{}'.format(name + '.gv')
    g = Digraph(format='png', filename=fname)
    g.attr(rankdir='LR')
    for start, v in nfa.trans_matrix.items():
        for char, end_set in v.items():
            for end in end_set:
                if char == epsilon:
                    g.edge(str(start), str(end), label=chr(0x03B5))  # epsilon
                else:
                    g.edge(str(start), str(end), label=char)

    for state in nfa.accepting_states:
        g.node(str(state), shape='doublecircle')

    g.body.append(f'labelloc="t";\nlabel="starting state = {nfa.starting_state}";')
    return g.render()


def draw_dfa(dfa, name):
    os.makedirs('figures', exist_ok=True)
    fname = 'figures/{}'.format(name + '.gv')
    g = Digraph(format='png', filename=fname)
    g.attr(rankdir='LR')
    for start, v in dfa.trans_matrix.items():
        for char, end in v.items():
            g.edge(str(start), str(end), label=char)

    for state in dfa.accepting_states:
        g.node(str(state), shape='doublecircle')

    g.body.append(f'labelloc="t";\nlabel="starting state = {dfa.starting_state}";')
    return g.render()
