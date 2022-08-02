# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util
import math

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # Number of iterations is a parameter of ValueIterationAgent object
        # Iterate num. of iterations many times.  For each iteration,
        # compute Q-value for each action from each non-terminal state and
        # choose the max Q-value from a each state, and update 
        # self.values (a Counter object) which is essentially a dictionary

        # Is there a better way to do this?

        for i in range(self.iterations):
            values_copy = self.values.copy()
            for state in self.mdp.getStates():
                if not self.mdp.isTerminal(state):
                    _QVal = [] # list representing Q-values for each (state, action) pair for a given state
                    for action in self.mdp.getPossibleActions(state):
                        _QVal.append(self.computeQValueFromValues(state, action))
                    max_QValue = max(_QVal)
                    values_copy[state] = max_QValue
            self.values = values_copy

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
          Return Q-value of (state, action) pair
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        # Q-value is sum of expected utilities for successor states from 'state'
        
        # For given (state, action) pair, get transition states and their probabilities
        transitionStates_and_Probs = \
            self.mdp.getTransitionStatesAndProbs(state, action)

        # Now, create a list of expected utilities of successor states for 
        # each (state, action) pair produced by getTransitionStatesAndProbs.
 
        sum = 0 
        for successorState, prob_ofSuccessor in transitionStates_and_Probs:
            reward = self.mdp.getReward(state, action, successorState)
            sum += prob_ofSuccessor * (reward + self.discount*self.values[successorState])
        return sum

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        
        # For each possible action for a given state, compute Q-value of the 
        # (state, action) pair.  Return action with highest Q-value.
   
        actions = self.mdp.getPossibleActions(state)
        bestAction, max_QValue = None, -(math.inf)
        #max_QValue = -(math.inf)

        # Special case where, for a given state, there are no possible actions
        if not actions: return None 

        # Compare each Q-value for a (state, action) pair across all possible
        # actions. Action from the optimal policy will be the action whose
        # Q-value is the largest, and this is the action that is returned

        for action in actions:
            _QVal = self.computeQValueFromValues(state, action)
            if _QVal > max_QValue: # Strict inequality to break ties
                max_QValue, bestAction = _QVal, action
        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        stateList = self.mdp.getStates() # Obtain list of states
        _length = len(stateList)
        for i in range(self.iterations):
            state = stateList[i % _length]
            if not self.mdp.isTerminal(state): # If 'state' is terminal, do nothing
                action = self.computeActionFromValues(state) # best action in 'state'
                QValue = self.computeQValueFromValues(state, action)
                self.values[state] = QValue # Update value for 'state'

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        return None
