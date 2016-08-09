# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""
from game import Directions
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    node = (problem.getStartState(),[],0)
    frontier = util.Stack()
    frontier.push(node)
    explored = set([]) # use add to add element to the set
    
    while 1:
       if frontier.isEmpty() :
           print 'Failure in finding a solution'
           return []
       node = frontier.pop()
       if problem.isGoalState(node[0]):
           return node[1]
       if node[0] not in explored:            
           explored.add(node[0])
           successors = problem.getSuccessors(node[0])
           for fake_child in successors:
               child = (fake_child[0],node[1] + [fake_child[1]], node[2] + fake_child[2])
               frontier.push(child)
        
    
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()..
    node = (problem.getStartState(),[],0)
    if problem.isGoalState(node[0]) :
        return node[1]
    frontier = util.Queue()
    frontier.push(node)
    explored = set([]) # use add to add element to the set
    
    while 1:
        if frontier.isEmpty() :
            print 'Failure in finding a solution'
            return []
        node = frontier.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if node[0] not in explored:            
            explored.add(node[0])
            successors = problem.getSuccessors(node[0])
            for fake_child in successors:
                child = (fake_child[0],node[1] + [fake_child[1]], node[2] + fake_child[2])
                frontier.push(child)
                
"""
def  breadthFirstSearchForCorners(problem):
    node = [problem.getStartState()[0],[],problem.getStartState()[2][:],[]]
    #seperately are: position, path taken from start point, corners left, path taken before last time reach a corner 
    frontier =util.Queue()
    frontier.push (node)
    explore = set([])
    while 1:
        if frontier.isEmpty() :
            print 'Failure in finding a solution'
            return []
        node = frontier.pop()
        
        
        if (node[0] in node[2]) and node[0] not in node[3]:             
            node[3] = []             #explored clear
            node[2].remove(node[0])  #corners left minus 1
            
        if len(node[2])==0 :
            return node[1]
        
        for child in problem.getSuccessors(node[0]):
            if child[0] not in node[3]: 
                tmpPath = node[1]
                tmpPath.append(child[1])
                tmpExplored = node[3][:]
                tmpExplored.append(node[0])
                frontier.push([child[0], tmpPath, node[2],tmpExplored])

    
    frontier =util.Queue()
    frontier.push (node)
    
    while (len(node[2]) > 0):
        
        path = node[1]
        
        
        for child in problem.getSuccessors(node[0]):
            if child[0] not in node[3]: 
                tmpPath = node[1]
                tmpPath.append(child[1])
                tmpExplored = node[3][:]
                tmpExplored.append(node[0])
                frontier.push([child[0], tmpPath, node[2],tmpExplored])
        if (node[0] in node[2]) and node[0] not in node[3]:             
            node[3] = []             #explored clear
            node[2].remove(node[0])  #corners left minus 1
        
        if frontier.isEmpty():
            break
        node = frontier.pop()
    return node[1]
"""         

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    node = (problem.getStartState(),[],0)
    frontier = util.PriorityQueue()
    frontier.push(node,node[2])
    explored = set([]) # use add to add element to the set    
    while 1:
        if frontier.isEmpty() :
            print 'Failure in finding a solution'
            return []
        node = frontier.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if node[0] not in explored:            
            explored.add(node[0])
            successors = problem.getSuccessors(node[0])
            for fake_child in successors:
                child = (fake_child[0],node[1] + [fake_child[1]], node[2] + fake_child[2])
                frontier.push(child,child[2])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    node = (problem.getStartState(),[],0)
    frontier = util.PriorityQueue()
    frontier.push(node,node[2]+heuristic(node[0],problem))
    explored = set([]) # use add to add element to the set    
    while 1:
        if frontier.isEmpty() :
            print 'Failure in finding a solution'
            return []
        node = frontier.pop()
        if problem.isGoalState(node[0]):
            return node[1]
        if node[0] not in explored:            
            explored.add(node[0])
            successors = problem.getSuccessors(node[0])
            for fake_child in successors:
                child = (fake_child[0],node[1] + [fake_child[1]], node[2] + fake_child[2])                
                frontier.push(child,child[2]+heuristic(child[0],problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
