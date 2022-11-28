# Differentially Private Misra-Gries Sketch
This is a Python implementation of a differentially private Misra-Gries sketch, as described in the paper [1] paper by Christian Lebeda and Jakub Tětek.

## How to use
In the file misra_gries.py, we implement one class: DPMisraGriesSketch. It has the following methods:

* \__init__(k) - this method inicializes the sketch with size k
* update(x) - this method adds the element x to the sketch
* get_counts() - this method returns the counts stored by the sketch.  
&nbsp;&nbsp;&nbsp;&nbsp;    !!! THIS VIOLATES PRIVACY. USE WITH CAUTION !!!
* privately_release(epsilon, delta) - this privately releases the approximate histogram  
&nbsp;&nbsp;&nbsp;&nbsp;    This method is (epsilon,delta)-differentially private for the given values of parameters  
&nbsp;&nbsp;&nbsp;&nbsp;    May be used multiple times (subject to deteriorating privacy by composition)  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    !!! Subject to the caveats below. !!!

We also implement two simple tests in the file test.py.

## Caveats of this implementatoin
In this implementation, we ignore issues with floating points. If this algorithm is to be used, it should be re-implemented using a library that implements the Laplace mechanism. We also do not use cryptography-grade randomness, which also possibly leaks some information.


[1] TODO
