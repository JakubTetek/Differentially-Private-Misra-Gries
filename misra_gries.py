"""
This module implements a differentially private version of the Misra-Gries sketch.
This algorithm has been described by Christian Lebeda and Jakub Tetek in the paper TODO

It implements one class: DPMisraGries
"""

from math import log
from random import shuffle
from numpy.random import laplace


class DPMisraGries:
    """
    This class implements a differentially private version of the Misra-Gries sketch.

    It implements the following methods:
        __init__(k) - this method inicializes the sketch with size k
        update(x) - this method adds the element x to the sketch
        get_counts() - this method returns the counts stored by the sketch.
            !!! THIS VIOLATES PRIVACY. USE WITH CAUTION !!!
        privately_release(epsilon, delta) - this privately releases the approximate histogram
            This method is (epsilon,delta)-differentially private for the given values of parameters
            May be used multiple times (subject to deteriorating privacy by composition)
            !!! Read the caveates about our implementation in the README !!!
    """

    def __init__(self, sketch_size):
        self.sketch_size = sketch_size
        self.counters = {}
        self.input_size = 0
        self.nonzeroes = 0

        for i in range(sketch_size):
            # In the paper, we use unique elements at initialization.
            # However, this is hard to implement in Python, so we use
            # items 1...sketch_size instead.
            # This has the drawback that we may return an item that was never
            # inserted into the sketch.
            self.counters[i] = 0

    def update(self, item):
        """Calling update(x) adds the element x to the sketch"""
        self.input_size += 1
        if item in self.counters:
            self.counters[item] += 1
            if self.counters[item] == 1:
                self.nonzeroes += 1

        elif self.nonzeroes < self.sketch_size:
            # we remove the item with a zero count that has the smallest key
            zero_keys = set()
            for key in self.counters:
                if self.counters[key] == 0:
                    zero_keys.add(key)

            assert len(zero_keys) == self.sketch_size - self.nonzeroes
            min_key = min(zero_keys)

            del self.counters[min_key]
            
            # now we can add the new item
            self.counters[item] = 1
            self.nonzeroes += 1

        else:
            for key in self.counters:
                self.counters[key] = max(0,self.counters[key] - 1)
                if self.counters[key] == 0:
                    self.nonzeroes -= 1

            

    def get_counts(self):
        """This method returns the counts stored by the sketch.
        !!! THIS VIOLATES PRIVACY. USE WITH CAUTION !!!"""
        return self.counters

    def privately_release(self, epsilon, delta):
        """This releases the approximate histogram in a differentially private manner

        This method is (epsilon,delta)-differentially private for the given values of parameters.
        May be used multiple times (subject to deteriorating privacy by composition).

        
        !!! Read the caveates about our implementation in the README !!!
        """
        privatized_counters = {}

        global_laplace = laplace(0, 1/epsilon)

        key_value_pairs = list(self.counters.items())
        # need to permute the values as the order may depend on the order
        #   in which we entered things into the counters dictionary
        shuffle(key_value_pairs)
        for key, value in key_value_pairs:
            new_value = value + global_laplace + laplace(0, 1/epsilon)
            if new_value >= 1+2*log(3/delta): # TODO check that this matches the final value in the paper
                privatized_counters[key] = new_value

        return privatized_counters
