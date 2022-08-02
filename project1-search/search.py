# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()			# create FIFO Queue for frontier
    expanded_nodes = []				# list of nodes that have been expanded
    start_node = problem.getStartState()	# starting postition
    frontier.push((start_node,[]))		# push (starting position, []) tuple into Queue.  Empty list will be the path to goal
    while not frontier.isEmpty():
        node = frontier.pop()			# pop next element in the frontier queue
        if problem.isGoalState(node[0]):
            return node[1]			# if current node is the goal, return path to goal (second element of the node tuple)
        if node[0] not in expanded_nodes:
            expanded_nodes.append(node[0])		# add visited node to expanded node list
            possible_moves = problem.expand(node[0]) 	# list of possible moves from current node
            _length = len(possible_moves)
            for i in range(_length):
               frontier.push((possible_moves[i][0], node[1]+[possible_moves[i][1]]))	# node variable is tuple and 2nd element keeps track of the path
        
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
    
def compute_priority(state, action_cost, path_cost, heuristic=nullHeuristic):
    """ Computes priority for a given state using action cost and specified heuristic.

	    Args - state is (x,y) location, action_cost is the cost of the specified action
		   which comes from the expand() function, and path_cost is the cost of a 
                   specific path from the start node to the node whose priority is being 
                   computed
	    Returns - priority to be stored in queue
    """
    return heuristic(state, problem) + action_cost + path_cost

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    class Node:
        """ 
        Attributes:
            state is (x,y) location in the pacman grid
            path is the path taken to get to current state
            cost is the the total cost along the path
        """
        def __init__(self, state, path, cost):
            self.state = state
            self.path = path
            self.cost = cost

    node = Node(problem.getStartState(), (), 0) # Initial cost is 0
    frontier = util.PriorityQueue()
    frontier.push(node, 1)		# arbitrary priority for first node
    expanded = []
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return list(node.path)
        if node.state not in expanded:
            expanded.append(node.state)
            child_nodes = problem.expand(node.state)
            for child in child_nodes:
                action_cost = child[2]
                priority = heuristic(child[0], problem) + action_cost + node.cost
                frontier.push(Node(child[0], node.path + (child[1],), node.cost + action_cost), priority)
    return None

def isCycle(node_state, ):
    '''
    Args:
      node_state: (x,y) location in the grid
      expanded: list of previously expanded locations
   
   Returns:
      Boolean True if the state in the given node appears previously in expanded data structure
      Boolean False otherwise
    '''
    if node_state in expanded:
        return True
    else:
        return False
    
    
''' The following code can be added to the end of search.py to
add iterative deepening as one of the available search algorithms.'''

def iterativeDeepeningSearch(problem):
    '''Implements iterative deepening search to find an optimal solution
    path for the given problem. 

    This is done by repeatedly running a depth-limited version of
    depth-first search for increasing depths.  A depth-limited search
    only expands a node--retrieves its children and adds them to the
    frontier--if the path to the node has a number of actions that is
    no more than the given depth.  If a node would have been expanded
    except for the depth limit, we say that the search has been "cut
    off" for that depth limit.  As suggested by the slides, we will
    run this search for depth limits of 1, 2, 3, etc., until either a
    solution is found or a depth-limited search has been run without
    being cut off for a given depth limit and without finding a
    solution, in which case no goal node can be reached and
    iterativeDeepeningSearch should return None.

    Args:
      problem: A SearchProblem instance that defines a search problem.

    Returns: 
      A list of actions that is as short as possible for reaching a
        goal node, or None if no goal node is reachable from the initial 
        state.

    '''
    depth_limit = 0
    while True:
        depth_limit += 1
        # print(f'Search to depth {depth_limit}')
        result = limitedDepthFirstSearch(problem, depth_limit)
        if result != "cutoff":
            return result

def limitedDepthFirstSearch(problem, depth_limit=1):
    '''Runs depth-first search with a depth bound.

    Args:
      problem: A SearchProblem instance that defines a search problem.
      depth_limit: A node will not be expanded if the path to the node
        has a length exceeding the depth value, which is expected to
        be a positive integer.

    Returns:
      A path to a goal node, if one is found, or the string "cutoff" if no
      goal was found and the search was cut off for the given depth limit,
      or None if no goal was found and the search was not cut off.
    '''
    class Node:
        """ 
        A visited attribute was added to the node class.  This functions similarly as the 
        expanded data structure used in other search algorithms we have used.  The main 
        thing is that the visited attribute of node objects will keep track of (x, y) 
        locations that the node object has expanded along its path.  It is worth noting
        that the visited attribute will be unique to each node object.
        """
        def __init__(self, state, path, visited):
            self.state = state
            self.path = path
            self.visited = visited
           
    node = Node(problem.getStartState(), (), ())
    frontier = util.Stack()
    frontier.push(node)
    #expanded = []
    result = None
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return list(node.path)
        if len(node.path) > depth_limit:
            result = "cutoff"
        elif not isCycle(node.state, node.visited):
            node.visited = node.visited + (node.state,)
            #expanded.append(node.state)
            child_nodes = problem.expand(node.state)
            for child in child_nodes:
                frontier.push(Node(child[0], node.path + (child[1],), node.visited))
    return result

def isCycle(node_state, node_visited):
    '''
    Args:
      node_state:  current state ((x, y) location) of node
      node_visited: tuple of (x, y) locations that a node has visited on its path

    Returns:
      False if the current state of node object has *not* been visited on node's path
      True otherwise

    Note that this function does not just check if a state has been visited, but rather
    checks if a state has been visited by a particular node object.  So one state may be 
    attained by different node objects 
    '''
    if node_state not in node_visited:
        return False
    else:
        return True
    

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
