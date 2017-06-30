from collections import defaultdict


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


class RevIndex:
    def __init__(self, partitions):
        self.p_map = {}
        self.p_id = 0
        for partition in partitions:
            for state in partition:
                self.p_map[state] = self.p_id
            self.p_id += 1

    def find_part(self, state):
        if state is None:
            return -1
        else:
            return self.p_map[state]

    def mark_new_part(self, states):
        for state in states:
            self.p_map[state] = self.p_id
        self.p_id += 1


class DFA:
    def __init__(self):
        self.trans_matrix = {}
        self.accepting_states = set()
        self.starting_state = None
        self.alphabet = set()

    def _split(self, rev_index, partition):
        states = set(partition)
        sample = states.pop()
        first_set = {sample}
        second_set = set()
        while states:
            state = states.pop()
            for char in self.alphabet:
                if rev_index.find_part(self.trans_matrix[sample][char]) \
                        != rev_index.find_part(self.trans_matrix[state][char]):
                    second_set.add(state)  # char distinguishes this state
                    break
            else:
                first_set.add(state)  # no char distinguishes this state

        if second_set:  # partition split
            rev_index.mark_new_part(second_set)
            return {frozenset(first_set), frozenset(second_set)}
        else:
            return {frozenset(first_set)}

    def partition_states(self):
        partitions = set()
        new_partitions = {frozenset(self.accepting_states),
                          frozenset(set(self.trans_matrix.keys()) - self.accepting_states)}
        rev_index = RevIndex(new_partitions)
        while new_partitions != partitions:
            partitions = new_partitions
            new_partitions = set()
            for partition in partitions:
                new_partitions |= self._split(rev_index, partition)
        return partitions

    def minimize(self):
        pass
