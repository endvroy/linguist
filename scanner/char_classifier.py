from bisect import bisect_right
from functools import reduce


class CharClassifier:
    def __init__(self, markers):
        self.markers = sorted(markers)

    def classify(self, char):
        return bisect_right(self.markers, ord(char))


def merge_markers(a, b):
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


def merge_classifiers(classifiers):
    new_markers = reduce(merge_markers, (x.markers for x in classifiers))
    new_classifier = CharClassifier(new_markers)
    class_maps = [map_char_class(x.markers, new_markers) for x in classifiers]
    return new_classifier, class_maps
