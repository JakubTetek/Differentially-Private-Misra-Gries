"""This is a test script for the Misra-Gries sketch. There is a small probability that 
this test will fail even if the sketch is correct, as it is a probabilistic structure."""

from math import log
import unittest
import numpy as np
from misra_gries import DPMisraGries


def item_frequencies(input_list):
    """Return a dictionary with the frequencies of the items in the input list"""
    freq = {}
    for item in input_list:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1

    return freq

class TestMisraGries(unittest.TestCase):

    def test_misra_gries1(self):
        """This test with put into the sketch at most sketch_size items
        The answers (non-private) should be exact."""
        input_size = 10000
        alpha = 1.5
        sketch_input_unfiltered = np.random.zipf(alpha, input_size)
        sketch_input = list(filter(lambda x: x < 1000, sketch_input_unfiltered))

        sketch = DPMisraGries(1000)

        for item in sketch_input:
            sketch.update(item)

        freq = item_frequencies(sketch_input)
        freq_sketch = sketch.get_counts()

        for item in freq.keys():
            self.assertEqual(freq_sketch[item], freq[item])

    def test_misra_gries2(self):
        """This test will put into the sketch more than sketch_size items.
        It checks that the answers are within the error bounds.
        The test is repeated 100 times."""
        for _ in range(100):
            sketch_size = 100
            sketch = DPMisraGries(sketch_size)

            input_size = 10000
            alpha = 1.5
            sketch_input = np.random.zipf(alpha, input_size)

            for item in sketch_input:
                sketch.update(item)

            eps = 1
            delta = input_size/10
            freq = item_frequencies(sketch_input)
            freq_sketch = sketch.privately_release(eps, delta)

            for item in freq:
                if item not in freq_sketch:
                    freq_sketch[item] = 0

            for item in freq.keys():
                self.assertLessEqual(freq_sketch[item] - freq[item], 20*eps)
                self.assertGreaterEqual(freq_sketch[item] - freq[item], - input_size/sketch_size - 20*eps - 1 - log(3/delta))

if __name__ == '__main__':
    unittest.main()
