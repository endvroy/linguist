from bisect import bisect_right
from functools import reduce


def make_markers(m):
    return sorted(list(set(m)))


class CharClassifier:
    def __init__(self, markers):
        self.markers = make_markers(markers)

    def classify(self, char):
        return bisect_right(self.markers, ord(char))

    def all_classes(self):
        return range(len(self.markers) + 1)

    def copy(self):
        return CharClassifier(self.markers)


def merge_2_markers(a, b):
    ret = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            ret.append(a[i])
            i += 1
        elif a[i] > b[j]:
            ret.append(b[j])
            j += 1
        else:
            ret.append(a[i])
            i += 1
            j += 1
    if i < len(a):
        ret += a[i:]
    else:
        ret += b[j:]
    return ret


def map_char_class(original_markers, new_markers):
    class_map = {0: list(range(0, bisect_right(new_markers, original_markers[0])))}
    for i in range(len(original_markers) - 1):
        class_map[i + 1] = list(range(class_map[i][-1] + 1,
                                      bisect_right(new_markers, original_markers[i + 1])))
    class_map[len(original_markers)] = list(range(class_map[len(original_markers) - 1][-1] + 1,
                                                  len(new_markers) + 1))
    return class_map


def merge_markers(markers):
    markers = list(markers)
    new_markers = reduce(merge_2_markers, markers)
    class_maps = [map_char_class(x, new_markers) for x in markers]
    return new_markers, class_maps


def merge_classifiers(classifiers):
    classifiers = list(classifiers)
    new_markers, class_maps = merge_markers(x.markers for x in classifiers)
    new_classifier = CharClassifier(new_markers)
    return new_classifier, class_maps
