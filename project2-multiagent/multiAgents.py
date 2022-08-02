# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        """ How far is nearest ghost? Wouldn't want Pacman to die :(  """
        ghost_positions = childGameState.getGhostPositions()
        closest_ghost_distance = min([util.manhattanDistance(newPos, ghost) for ghost in ghost_positions])
        
        """ Does the next action increase my score? """
        score_difference = childGameState.getScore() - currentGameState.getScore()
        #print(f'The next action has a score difference of {score_difference}')
        
        """ How far is the closest food item? """
        pacman_position = currentGameState.getPacmanPosition()
        closest_food = min([util.manhattanDistance(pacman_position, food) for food in currentGameState.getFood().asList()])
        #print(f'Closest food is {closest_food} spots away')
        reciprocal_food = 1/closest_food
        
        """ Does the new action move pacman closer to food? """
        if closest_food > 1:
            new_food_distances = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
            if len(new_food_distances) == 0:
                new_closest_food = 0
            else:
                new_closest_food = min(new_food_distances)
            is_food_closer = closest_food - new_closest_food
        else:
            new_closest_food = 1
        is_food_closer = closest_food - new_closest_food

        """ Evaluate given conditions in the world """
        evaluation = 0
        if closest_ghost_distance <= 1:				# Ghost is very close! Avoid this at all costs
            evaluation += -25
        elif closest_ghost_distance <= 3 and closest_ghost_distance > 1:	# Ghost is getting close...
            evaluation += -10
        elif closest_ghost_distance > 3:			# Ghost is not too close
            evaluation += 5
        if score_difference > 0:				# Score will be increased by next move
            evaluation += 18
        elif reciprocal_food > 0 and is_food_closer > 2:	# Score won't increase, but Pacman is pretty close to food
             evaluation += 15
        elif is_food_closer < 2 and is_food_closer >= 0:	# Score is still not increasing and Pacman is honing in on food
             evaluation += 12
        else:							# Pacman is not getting close to food and score is not increasing	
             evaluation += -1
        #print(f'The evaluation function value is {evaluation}')
        return evaluation

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        s = gameState
        agent = 0 # Pacman goes first
        depth = self.depth

        # More-or-less repeat the maximizer minimax code from below
        # (with some simplifications) for the root node so that we can
        # obtain the action associated with the maximal minimax value.
        actions = s.getLegalActions(agent)
        newAgent = 1     # First ghost will be the next evaluator
        newDepth = depth # Depth remains the same until Pacman evaluates again

        # Create list of minimax values for all successors of current state.
        values = [self.minimax_value(s.getNextState(agent, action),
                                     newAgent, 
                                     newDepth)
                  for action in actions]
        
        # Return the action corresponding to the maximal minimax value.
        pairs = zip(values, actions) # creates a list of value/action pairs
        first = lambda pair: pair[0] # Function returning first element of pair
        return max(pairs, key=first)[1] 

    def minimax_value(self, s, agent, depth):
        '''Minimax helper function.

        Args:
          s: Game state for which minimax value is to be produced.
          agent: Number of agent evaluating the given state. 
            0 is Pacman, ghosts are 1 through (numAgents-1).
          depth: Number of levels remaining in search.  If 0, search is
            complete and evaluation function value is returned. 

        Returns: Real number that is the minimax value of the given
          state, where an evaluation function is used to produce the
          value of a terminal state or a state at maximum depth.  

        '''
        if s.isWin() or s.isLose() or depth <= 0:
            return self.evaluationFunction(s)
        actions = s.getLegalActions(agent)
        newAgent = (agent+1) % s.getNumAgents()
        newDepth = depth-1 if newAgent == 0 else depth

        # Create list of minimax values for all successors of current state.
        values = [self.minimax_value(s.getNextState(agent, action),
                                     newAgent, 
                                     newDepth)
                  for action in actions]

        # Return optimal value, where optimal depends on agent.
        return max(values) if agent==0 else min(values)

import math
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

    	# Initialize alpha, beta and v 
        alpha = -math.inf
        beta = math.inf
        v = -math.inf

        # Initialize state, agent, depth, and actions
        s = gameState
        agent = 0 			# Pacman evaluates first
        depth = self.depth	
        actions = s.getLegalActions(agent)

        # Check if s is a winning state
        if s.isWin() or s.isLose() or depth <= 0:	# Check for leaves (winning/losing leaf, or max search depth leaf)
            return self.evaluationFunction(s)

        newAgent = 1			# First ghost evaluates after Pacman
        newDepth = depth		# Depth is decremented when Pacman evaluates
       
        for action in actions:
            newDepth = depth-1 if newAgent == 0 else depth	# Depth is decremented when Pacman evaluates
            new_v = self.min_value(newDepth,
                                   newAgent,
                                   s.getNextState(agent, action),
                                   alpha,
                                   beta)
            if new_v > v:
                best_move = (new_v, action)
                v = new_v
            alpha = max(v, alpha)

        return best_move[1]

    def max_value(self, depth, agent, s, alpha, beta):
        ''' Alpha-Beta pruning max agent helper function
            This function is called when it is Pacman's turn to evaluate!
    
    Args:
      depth -Number of levels remaining in search.  If 0, search is
            complete and evaluation function value is returned. 
      agent - Number of agent evaluating the given state. 
            0 is Pacman, ghosts are 1 through (numAgents-1).
      s - Game state for which max value is to be produced.
      alpha- Max agent's best option on path to root
      beta - Min agent's best option on path to root

    Returns: A real number v representing maximum utility action score for max agent 
        '''
        if s.isWin() or s.isLose() or depth <= 0:	# Check for leaves (winning/losing leaf, or max search depth leaf)
            return self.evaluationFunction(s)
        v = -math.inf					# Initialize v (value) to negative infinity
        actions = s.getLegalActions(agent)		# List of legal actions for given agent
        newAgent = (agent+1) % s.getNumAgents()		# New agent will always be a ghost in the max_value function
        newDepth = depth-1 if newAgent==0 else depth	# Decrement depth when it is Pacman's turn to evaluate next

        for action in actions:
            v = max(v, self.min_value(newDepth, 
                                      newAgent,
                                      s.getNextState(agent, action),
                                      alpha,
                                      beta))
            if v > beta:				# If value is better than Min Agent's best move, return value
                #print('okay')
                return v
            alpha = max(alpha, v)			# Update alpha
            #print(f'Max agent has alpha of {alpha} and value of {v}')
        return v 

        
    def min_value(self, depth, agent, s, alpha, beta):  
        ''' Alpha-Beta pruning min agent helper function
    
        Args:
          depth -Number of levels remaining in search.  If 0, search is
                 complete and evaluation function value is returned. 
          agent - Number of agent evaluating the given state. 
                  0 is Pacman, ghosts are 1 through (numAgents-1).
           s - Game state for which min value is to be produced.
           alpha- Max agent's best option on path to root
           beta - Min agent's best option on path to root

        Returns: A real number v representing minimum utility action score for min agent 
        '''
        if s.isWin() or s.isLose() or depth <= 0:	# Check for leaves (winning/losing leaf, or max search depth leaf)
            return self.evaluationFunction(s)
        v = math.inf					# Initialize v to positive infinity
        actions = s.getLegalActions(agent)		# List of legal actions for given agent
        newAgent = (agent+1) % s.getNumAgents()
        newDepth = depth-1 if newAgent==0 else depth	# Decrement depth on Pacman's turn

        if newAgent == 0:				# Max Agent evaluates next
            for action in actions:
                v = min(v, self.max_value(newDepth, 
                                          newAgent,
                                          s.getNextState(agent, action),
                                          alpha,
                                          beta))
                if v < alpha:
                    #print('okay')
                    return v
                beta = min(beta, v)
                #print(f'Min Agent has value of {v} and beta of {beta}')
            return v

        else:						# Min Agent's (ghost) turn to evaluate next
            for action in actions:
                v = min(v, self.min_value(newDepth, 
                                          newAgent,
                                          s.getNextState(agent, action),
                                          alpha,
                                          beta))
                if v < alpha:
                    #print('okay')
                    return v				# If value is better than Max Agent's best move, then return value
                beta = min(beta, v)			# Update beta
                #print(f'Min Agent has value of {v} and beta of {beta}')
            return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4).  Helps model behavior of agents that 
      can potentially make suboptimal choices (i.e. the ghosts in Pacman)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        s = gameState
        agent = 0 	# Pacman goes first
        depth = self.depth

        actions = s.getLegalActions(agent)
        newAgent = 1	 # Next evaluator is a ghost
        newDepth = depth # Depth is decremented when Pacman evalutes

        # Create list of expectimax values for all successors of current state
        values = [self.expectimax_value(s.getNextState(agent, action),
                                        newAgent,
                                        newDepth)
                  for action in actions]

        # Return the action corresponding to the maximal expectimax value
        pairs = zip(values, actions)	# Creates list of value/action pairs
        first = lambda pair: pair[0]	# Function returning first element of a pair
        return max(pairs, key=first)[1]
    
    def expectimax_value(self, s, agent, depth):
        """ Expectimax helper function.

        Args:
            s: Game state for which expectimax value is to be produced
            agent: Number of agent evaluating the given state
                0 is Pacman, ghosts are 1 through (numAgents-1)
            depth: Number of levels remaining in search.  If 0, search is complete
                  and evaluation function value is returned

        Returns:  Real number that is the expectimax values of the given state,
            where an evaluation function is used to produce the value of a terminal
            state or a state at maximum depth
        """

        if s.isWin() or s.isLose() or depth <= 0:  # Check state to see if it is a leaf node in the search tree
            return self.evaluationFunction(s)
        actions = s.getLegalActions(agent)	# List of possible actions
        newAgent = (agent+1) % s.getNumAgents()
        newDepth = depth-1 if newAgent == 0 else depth	# Decrement depth when it is Pacman's turn
 
        # Create list of expectimax values for all successors of current state
        values = [self.expectimax_value(s.getNextState(agent, action),
                                         newAgent,
                                         newDepth)
                  for action in actions]
        if agent == 0:	# Max agent A.K.A. Pacman's turn to evaluate, return maximum score
            return max(values)
        else:	# Min agent A.K.A ghost's turn to evaluate, return expected value over all possible moves
            probability = (1 / len(actions))	# Ghosts choose a move uniformly at random from their possible moves
            expected_value = 0
            for val in values:
                expected_value += val*probability
            return expected_value


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
