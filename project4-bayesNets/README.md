The goal of this project was to write code to implement inference techniques for a Bayesian Pacman.  Inference is being done for a Pacman-esque world where the map is entirely invisible, and Pacman has to find his destination (called the 'Food House') while avoiding a trap (called the 'Ghost House') using information about his surroundings.

In the bayesAgent.py file, code to build a Bayes net, with corresponding probability tables, was written.

Additionally, the factorOperations.py file contains code that combines, eliminates, and normalizes factors (i.e., conditional probabilities).

Lastly, in the inference.py file,  one can find code that performs inference by the variable elimination in order to help Bayesian Pacman find the Food House.
