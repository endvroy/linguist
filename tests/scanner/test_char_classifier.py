import unittest

from linguist.base.scanner.char_classifier import *


class TestClassifier(unittest.TestCase):
    def test_classify(self):
        classifier = CharClassifier([ord('y'), ord('y') + 1])
        self.assertEqual(0, classifier.classify('x'))
        self.assertEqual(1, classifier.classify('y'))
        self.assertEqual(2, classifier.classify('z'))

    def test_all_classes(self):
        classifier = CharClassifier([ord('y'), ord('y') + 1])
        self.assertEqual([0, 1, 2], list(classifier.all_classes()))

    def test_copy(self):
        classifier = CharClassifier([ord('y'), ord('y') + 1])
        copied = classifier.copy()
        copied.markers.append('x')
        self.assertEqual([ord('y'), ord('y') + 1, 'x'], copied.markers)
        self.assertEqual([ord('y'), ord('y') + 1], classifier.markers)


class TestMerge(unittest.TestCase):
    def test_merge_markers(self):
        a = [2, 4, 6, 7]
        b = [3, 4, 5, 9, 12]
        self.assertEqual([2, 3, 4, 5, 6, 7, 9, 12], merge_2_markers(a, b))
        a = [4, 6, 9, 12, 15]
        b = [3, 5, 8, 12]
        self.assertEqual([3, 4, 5, 6, 8, 9, 12, 15], merge_2_markers(a, b))

    def test_class_map(self):
        a = [2, 4, 6, 7]
        b = [3, 4, 5, 9, 12]
        new_markers = merge_2_markers(a, b)
        map_a = map_char_class(a, new_markers)
        map_b = map_char_class(b, new_markers)
        self.assertEqual({0: [0],
                          1: [1, 2],
                          2: [3, 4],
                          3: [5],
                          4: [6, 7, 8]}, map_a)
        self.assertEqual({0: [0, 1],
                          1: [2],
                          2: [3],
                          3: [4, 5, 6],
                          4: [7],
                          5: [8]}, map_b)


if __name__ == '__main__':
    unittest.main()
