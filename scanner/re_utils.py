from metachar import epsilon
from scanner.char_classifier import CharClassifier, make_markers, merge_classifiers
from scanner.nfa import NFA
from scanner.char_classifier import merge_markers


def atom(char, category):
    nfa = NFA()
    nfa.classifier = CharClassifier([ord(char), ord(char) + 1])
    nfa.add_state(0)
    nfa.add_state(1)
    nfa.add_transition(0, 1, 1)
    nfa.mark_starting(0)
    nfa.mark_accepting(1, category)
    return nfa


def char_set(markers, accept, category):
    nfa = NFA()
    nfa.classifier = CharClassifier(markers)
    nfa.add_state(0)
    nfa.add_state(1)
    for domain in accept:
        nfa.add_transition(0, 1, domain)
    nfa.mark_starting(0)
    nfa.mark_accepting(1, category)
    return nfa


def neg_set(markers, accept, category):
    nfa = NFA()
    nfa.classifier = CharClassifier(markers)
    nfa.add_state(0)
    nfa.add_state(1)
    for domain in range(len(markers) + 1):
        if domain not in accept:
            nfa.add_transition(0, 1, domain)
    nfa.mark_starting(0)
    nfa.mark_accepting(1, category)
    return nfa


def char_member(char):
    markers = make_markers([ord(char), ord(char) + 1])
    accept = {1}
    return markers, accept


def char_range(start, end):
    markers = make_markers([ord(start), ord(end) + 1])
    accept = {1}
    return markers, accept


def merge_members(mags):
    markers, class_maps = merge_markers(x[0] for x in mags)
    accept = set()
    for i, mag in enumerate(mags):
        acc_set = mag[1]
        for acc in acc_set:
            for new_acc in class_maps[i][acc]:
                accept.add(new_acc)
    return markers, accept


def dot(category):
    nfa = NFA()
    nfa.classifier = CharClassifier([0])
    nfa.add_state(0)
    nfa.add_state(1)
    nfa.add_transition(0, 1, 1)
    nfa.mark_starting(0)
    nfa.mark_accepting(1, category)
    return nfa


def cat(nfa_list):
    nfa_list = list(nfa_list)
    cat_nfa = NFA()
    cat_classifier, class_maps = merge_classifiers(nfa.classifier for nfa in nfa_list)
    cat_nfa.classifier = cat_classifier
    for i, z in enumerate(zip(nfa_list, class_maps)):
        nfa, class_map = z  # add everything to cat_nfa
        for start, d in nfa.trans_matrix.items():
            cat_nfa.add_state((i, start))
            for char, end_set in d.items():
                if char == epsilon:
                    for end in end_set:
                        cat_nfa.add_transition((i, start), (i, end), epsilon)
                else:
                    for domain in class_map[char]:
                        for end in end_set:
                            cat_nfa.add_transition((i, start), (i, end), domain)
                            # cat_nfa.alphabet |= nfa.alphabet

    for i in range(len(nfa_list) - 1):  # link these nfa
        this = nfa_list[i]
        next_ = nfa_list[i + 1]
        for state in this.accepting_states:
            cat_nfa.add_transition((i, state),
                                   (i + 1, next_.starting_state),
                                   epsilon)

    cat_nfa.mark_starting((0, nfa_list[0].starting_state))
    for state, category in nfa_list[-1].accepting_states.items():
        cat_nfa.mark_accepting((len(nfa_list) - 1, state), category)

    return cat_nfa


def alt(nfa_list):
    nfa_list = list(nfa_list)
    alt_nfa = NFA()
    alt_classifier, class_maps = merge_classifiers(nfa.classifier for nfa in nfa_list)
    alt_nfa.classifier = alt_classifier
    for i, z in enumerate(zip(nfa_list, class_maps)):
        nfa, class_map = z
        for start, d in nfa.trans_matrix.items():
            alt_nfa.add_state((i, start))
            for char, end_set in d.items():
                if char == epsilon:
                    for end in end_set:
                        alt_nfa.add_transition((i, start), (i, end), epsilon)
                else:
                    for domain in class_map[char]:
                        for end in end_set:
                            alt_nfa.add_transition((i, start), (i, end), domain)
        # alt_nfa.alphabet |= nfa.alphabet
        for state, category in nfa.accepting_states.items():
            alt_nfa.mark_accepting((i, state), category)

    alt_nfa.add_state(1)  # starting state
    for i, nfa in enumerate(nfa_list):
        alt_nfa.add_transition(1,
                               (i, nfa.starting_state),
                               epsilon)

    alt_nfa.mark_starting(1)

    return alt_nfa


def k_closure(nfa: NFA):
    c_nfa = nfa.copy()
    for state in c_nfa.accepting_states:
        c_nfa.add_transition(c_nfa.starting_state,
                             state,
                             epsilon)
        c_nfa.add_transition(state,
                             c_nfa.starting_state,
                             epsilon)
    return c_nfa


def p_closure(nfa):
    nfa1 = nfa.copy()
    nfa2 = nfa.copy()
    return cat([nfa1, k_closure(nfa2)])


def opt_closure(nfa):
    opt_nfa = nfa.copy()
    for state in opt_nfa.accepting_states:
        opt_nfa.add_transition(opt_nfa.starting_state,
                               state,
                               epsilon)
    return opt_nfa
