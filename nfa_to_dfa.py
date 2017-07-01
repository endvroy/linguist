from collections import defaultdict
from dfa import DFA


def epsilon_closure(nfa, states):
    closure = set(states)
    working_set = set(states)

    while True:
        new_working_set = set()
        for s in working_set:
            for new_state in nfa.trans_matrix[s][nfa.epsilon]:
                if new_state not in closure:
                    closure.add(new_state)
                    new_working_set.add(new_state)
        if new_working_set:
            working_set = new_working_set
        else:
            break

    return closure


def next_set(nfa, states, char):
    """the set immediately obtained from state in states on char, without epsilon closure"""
    next_states = set()
    for state in states:
        if char in nfa.trans_matrix[state]:
            next_states |= nfa.trans_matrix[state][char]
    return next_states


def subset_cons(nfa):
    trans_matrix = {}
    accepting_states = set()
    starting_state = frozenset(epsilon_closure(nfa, {nfa.starting_state}))
    work_list = [starting_state]

    while work_list:
        states = work_list.pop()
        trans_matrix[states] = {}

        for char in nfa.alphabet:
            next_states = next_set(nfa, states, char)
            new_states = epsilon_closure(nfa, next_states)

            if new_states:
                new_states = frozenset(new_states)
                for state in new_states:
                    if state in nfa.accepting_states:
                        accepting_states.add(new_states)

                trans_matrix[states][char] = new_states
                if new_states not in trans_matrix.keys():
                    work_list.append(new_states)

    return trans_matrix, starting_state, accepting_states


def relabel_states(trans_matrix, starting_state, accepting_states):
    name_map = {}
    for i, state in enumerate(trans_matrix.keys()):
        name_map[state] = i
    new_matrix = {}
    new_accepting_states = set()
    for state in trans_matrix.keys():
        new_matrix[name_map[state]] = {}
        for c, s in trans_matrix[state].items():
            new_matrix[name_map[state]][c] = name_map[s]
    for state in accepting_states:
        new_accepting_states.add(name_map[state])

    return new_matrix, name_map[starting_state], new_accepting_states


def dict_to_dfa_matrix(d: dict):
    def none():
        return None

    matrix = {}
    for k in d:
        matrix[k] = defaultdict(none)
    for start, v in d.items():
        for char, end in v.items():
            matrix[start][char] = end

    return matrix


def nfa_to_dfa(nfa):
    trans_matrix, starting_state, accepting_states = relabel_states(*subset_cons(nfa))
    dfa_matrix = dict_to_dfa_matrix(trans_matrix)
    return DFA(dfa_matrix,
               starting_state,
               accepting_states,
               nfa.alphabet)
