# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if (scores[index] == bestScore) ]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    #print legalMoves[chosenIndex]
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    
    utility=0
    utilityGhost=0
    ScaryDistance=0
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    oldFood = currentGameState.getFood()
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    oldGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
    Capsules = currentGameState.getCapsules()
    self.walls = currentGameState.getWalls()
    top, right = self.walls.height-2, self.walls.width-2
    corners = ((1,1), (1,top), (right, 1), (right, top))
    
    x = newPos[0]
    y = newPos[1]
   
    #The effect of the Ghosts
    #Consider Capsules
    #we have to use oldScaredTimes or it will screw
    if oldScaredTimes[0] == 0:
        for Capsule in Capsules:
            utility= utility- manhattanDistance(Capsule,newPos)*50
        for GhostStates in newGhostStates:
            GhostPosition =GhostStates.getPosition()
            if manhattanDistance(GhostPosition, newPos)<2 :
                ScaryDistance = -9999
            else :
            # Stops Pacman from stopping
           
                if (action==Directions.STOP) :
                    utility = -9999
                    return successorGameState.getScore()+utility

                if oldFood[x][y] == True:
                    utility=9999
                    return successorGameState.getScore()+utility
                ScaryDistance = ScaryDistance + manhattanDistance(GhostPosition, newPos)
    else:
        for GhostStates in newGhostStates:
            GhostPosition =GhostStates.getPosition()
            utilityGhost = utilityGhost- manhattanDistance(GhostPosition,newPos)
        return utilityGhost
    
   

        
    
    utility=utility + ScaryDistance
    if newFood[x][y] == False  :     
        i=0
        while i<max([manhattanDistance(newPos,corners[1]),manhattanDistance(newPos,corners[2]),manhattanDistance(newPos,corners[3]),manhattanDistance(newPos,corners[0])]):
            i=i+1
            for j in range(i):
                k=i-j
                if (x-j>0) :
                    if (y+k<=top) and newFood[x-j][y+k]==True:
                        utility = utility-manhattanDistance(newPos,(x-j,y+k))*2                   
                        #print 'The food is in ', x-j, y+k
                        return successorGameState.getScore()+utility
                    if (y-k>0) and newFood[x-j][y-k]==True:
                        utility = utility-manhattanDistance(newPos,(x-j,y-k))*2                   
                        #print 'The food is in ', x-j, y-k
                        return successorGameState.getScore()+utility
                if (x+j<=right):
                    if (y+k<=top) and newFood[x+j][y+k]==True:
                        utility = utility-manhattanDistance(newPos,(x+j,y+k))*2                   
                        #print 'The food is in ', x+j,y+k
                        return successorGameState.getScore()+utility
                    if (y-k>0) and newFood[x+j][y-k]==True:
                        utility = utility-manhattanDistance(newPos,(x+j,y-k))*2                   
                        #print 'The food is in ', x+j, y-k
                        return successorGameState.getScore()+utility
                      
        
        """
        i=0
        while (x+i<=right) and (y+i<=top) : 
            i = i+1
            #x-i column
            for index in range(2*i) :
                j=y-i+index
                if (x-i>0) :
                    if (newFood[x-i][j] == True)  and (j>0) :
                        utility = utility-manhattanDistance(newPos,(x-i,j))*3                  
                        print 'The food is in ', x-i, j
                        return successorGameState.getScore()+utility
            #x+i column
                if (x+i<=right) :
                    if (newFood[x+i][j] == True) and (j>0) :
                        utility =utility- manhattanDistance(newPos,(x+i,j)) *3                   
                        print 'The food is in ', x+i, j
                        return successorGameState.getScore()+utility
            #y-i row
            for index in range(2*i) :
                j=x-i+index
                if (y-i>0):
                    if (newFood[j][y-i] == True) and (j>0)  :
                        utility = utility-manhattanDistance(newPos,(j,y-i))*3                   
                        print 'The food is in ',j,y-i
                        return successorGameState.getScore()+utility
            #y+i column
                if (y+i<=top):
                    if (newFood[j][y+i] == True)  and (j>0) :
                        utility = utility-manhattanDistance(newPos,(j,y+i)) *3              
                        print 'The food is in ', j,y+i
                        return successorGameState.getScore()+utility
            
            
            
                
      """          
            

    "*** YOUR CODE HERE ***"
    return successorGameState.getScore()+utility
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
  def maxValue(self,gameState,currentDepth,agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        u=-99999
        legalActions= gameState.getLegalActions(agentIndex)
        #print 'agentIndex', agentIndex, 'depth', currentDepth
        for action in legalActions:
            u=max([u,self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,1)])
            #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u, ' action', action           
        return u
    
  def minValue (self,gameState,currentDepth,agentIndex):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        u=99999
        nextIndex = (agentIndex+1) % gameState.getNumAgents()
        legalActions= gameState.getLegalActions(agentIndex)
        
        if agentIndex==gameState.getNumAgents()-1 :
            """ 
            the last agent
            """
            if currentDepth == self.depth:
                """ 
                the last depth
                """
                scores=[]
                for action in legalActions:
                    successor=gameState.generateSuccessor(agentIndex,action)
                    if (successor.isWin()) or (successor.isLose()):
                        return self.evaluationFunction(successor)
                    else:
                        scores.append(self.evaluationFunction(successor))
                        
                #print 'I am the last agent, hahaha', legalActions
                #print 'agentIndex', agentIndex, 'depth', currentDepth
                #print 'The score is', scores
                bestScore= min(scores)
                #print bestScore
                return  min(u,bestScore)
            else:
                """ 
                not the last depth
                """
                #print 'agentIndex', agentIndex, 'depth', currentDepth
                for action in legalActions:              
                    u=min(u,self.maxValue(gameState.generateSuccessor(agentIndex,action),currentDepth+1,nextIndex))
                    #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u,'action', action
                 
        else:
            """
            no the last agent
            """
            #print 'agentIndex', agentIndex, 'depth', currentDepth
            for action in legalActions:
                u=min(u,self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,nextIndex))
                #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u,'action', action
        return u
    
    
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #  gameState.isWin()
    #print gameState.getNumAgents()
    legalMoves = gameState.getLegalActions(0)
    scores = [self.minValue(gameState.generateSuccessor(0,action),1,1) for action in legalMoves]
    bestScore = max(scores)
    
    bestIndices = [index for index in range(len(scores)) if (scores[index] == bestScore) ]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    #print 'hahahahahhahahahahahaha The best score of the move is', bestScore, 'The best move is ', legalMoves[chosenIndex]
    return legalMoves[chosenIndex]

  

    
      

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    scores = [self.minValue(gameState.generateSuccessor(0,action),1,1,-99999,99999) for action in legalMoves]
    bestScore = max(scores)
    
    bestIndices = [index for index in range(len(scores)) if (scores[index] == bestScore) ]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    #print 'hahahahahhahahahahahaha The best score of the move is', bestScore, 'The best move is ', legalMoves[chosenIndex]
    return legalMoves[chosenIndex]

  def maxValue(self,gameState,currentDepth,agentIndex,alpha,beta):
        a=alpha
        b=beta
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        u=-99999
        legalActions= gameState.getLegalActions(agentIndex)
        #print 'agentIndex', agentIndex, 'depth', currentDepth
        for action in legalActions:
            u=max([u,self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,1,a,b)])
            if u>=b :
                
                #print 'prune' 'agentIndex', agentIndex, 'depth', currentDepth
                return u
            a= max(a,u)
            #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u, ' action', action           
        return u

  def minValue (self,gameState,currentDepth,agentIndex,alpha,beta):
        a= alpha
        b= beta
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        u=99999
        nextIndex = (agentIndex+1) % gameState.getNumAgents()
        legalActions= gameState.getLegalActions(agentIndex)
        if agentIndex!=1:
            """ first consider the circumstance father is still MIN
            	in this circumstance we don't have to do anything with a and b
            """                   
            if agentIndex==gameState.getNumAgents()-1 :
                """ not the first the last agent   """
                if currentDepth == self.depth:
                    """ not the first  the last agent the last depth  """
                    scores=[]
                    for action in legalActions:
                        successor=gameState.generateSuccessor(agentIndex,action)
                        if (successor.isWin()) or (successor.isLose()):
                            return self.evaluationFunction(successor)
                        else:
                            scores.append(self.evaluationFunction(successor))                        
                #print 'I am the last agent, hahaha', legalActions
                #print 'agentIndex', agentIndex, 'depth', currentDepth
                #print 'The score is', scores
                    bestScore= min(scores)
                #print bestScore
                    return  min(u,bestScore)
                else:
                    """ not the first the last agent not the last depth  """
                    #print 'agentIndex', agentIndex, 'depth', currentDepth
                    for action in legalActions:              
                        u=min(u,self.maxValue(gameState.generateSuccessor(agentIndex,action),currentDepth+1,nextIndex,a,b))
                        #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u,'action', action
                 
            else:
                """not the first not the last agent
                	with father MIN and son MIN
                """
                #print 'agentIndex', agentIndex, 'depth', currentDepth
                for action in legalActions:
                    u=min(u,self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,nextIndex,a,b))
                    #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u,'action', action
            return u
        else:
            """ the first agent """
            if agentIndex== gameState.getNumAgents()-1 :
                """ the first agent and also the last
                	which means its father and son are MAX
                """
                if currentDepth == self.depth:
                    """ the first agent the last and the last depth
                		will not have to update a,b
                	"""
                    scores=[]
                    for action in legalActions:
                        successor=gameState.generateSuccessor(agentIndex,action)
                        if (successor.isWin()) or (successor.isLose()):
                            return self.evaluationFunction(successor)
                        else:
                            scores.append(self.evaluationFunction(successor))
                    bestScore = min(scores)
                    return min (u,bestScore)
                else:
                    """ the first agent the last and  not the last depth
                		with father MAX with son MAX
                	"""
                    for action in legalActions:
                        u=min (u,self.maxValue(gameState.generateSuccessor(agentIndex,action),currentDepth+1,nextIndex,a,b))
                        if u<= a :
                            
                            #print 'prune' 'agentIndex', agentIndex, 'depth', currentDepth
                            return u
                        b = min (u,b)
                    return u           
            else:
                """ the first agent but not the last
                	with father MAX son MIN
                	rather simple......
                """
                
                for action in legalActions:
                    u=min(u,self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,nextIndex,a,b))
                    if u <= a  :
                        
                        #print 'prune' 'agentIndex', agentIndex, 'depth', currentDepth
                        return u
                    b= min(u,b)
                return u     
    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
    
  """
  def maxValue(self,gameState,currentDepth,agentIndex,alpha,beta):
        a=alpha
        b=beta
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        u=-99999
        legalActions= gameState.getLegalActions(agentIndex)
        #print 'agentIndex', agentIndex, 'depth', currentDepth
        for action in legalActions:
            u=max([u,self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,1,a,b)])
            #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u, ' action', action           
        return u

  def minValue (self,gameState,currentDepth,agentIndex,alpha,beta):
        a= alpha
        b= beta
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        u=99999
        nextIndex = (agentIndex+1) % gameState.getNumAgents()
        legalActions= gameState.getLegalActions(agentIndex)
        length = len(legalActions)
        if agentIndex!=1:
            """ first consider the circumstance father is still MIN
            	in this circumstance we don't have to do anything with a and b
            """                   
            if agentIndex==gameState.getNumAgents()-1 :
                """ not the first the last agent   """
                if currentDepth == self.depth:
                    """ not the first  the last agent the last depth  """
                    scores=0
                    for action in legalActions:
                        successor=gameState.generateSuccessor(agentIndex,action)
                        scores= self.evaluationFunction(successor) + scores                       
                #print 'I am the last agent, hahaha', legalActions
                #print 'agentIndex', agentIndex, 'depth', currentDepth
                #print 'The score is', scores
                    bestScore = scores/ float(length)
                #print bestScore
                    return  bestScore
                else:
                    """ not the first the last agent not the last depth  """
                    #print 'agentIndex', agentIndex, 'depth', currentDepth
                    u=0
                    for action in legalActions:              
                        u=self.maxValue(gameState.generateSuccessor(agentIndex,action),currentDepth+1,nextIndex,a,b) + u
                    u = u/ float(length)
                        #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u,'action', action
                 
            else:
                """not the first not the last agent
                	with father MIN and son MIN
                """
                #print 'agentIndex', agentIndex, 'depth', currentDepth
                u=0
                for action in legalActions:
                    u= u+ self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,nextIndex,a,b)
                u = u/ float(length)
                    #print 'agentIndex', agentIndex, 'depth', currentDepth, 'myScore', u,'action', action
            return u
        else:
            """ the first agent """
            if agentIndex== gameState.getNumAgents()-1 :
                """ the first agent and also the last
                	which means its father and son are MAX
                """
                if currentDepth == self.depth:
                    """ the first agent the last and the last depth
                		will not have to update a,b
                	"""
                    scores= 0
                    for action in legalActions:
                        successor=gameState.generateSuccessor(agentIndex,action)
                        scores = scores + self.evaluationFunction(successor)
                    bestScore = scores / float(length)
                    return  bestScore
                else:
                    """ the first agent the last and  not the last depth
                		with father MAX with son MAX
                	"""
                    u=0
                    for action in legalActions:
                        u= u+ self.maxValue(gameState.generateSuccessor(agentIndex,action),currentDepth,nextIndex,a,b)
                    u = u/ float(length)
                    return u           
            else:
                """ the first agent but not the last
                	with father MAX son MIN
                	rather simple......
                """
                u=0
                for action in legalActions:
                    u= u + self.minValue(gameState.generateSuccessor(agentIndex,action),currentDepth,nextIndex,a,b)
                u = u / float(length)
                return u

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    scores = [self.minValue(gameState.generateSuccessor(0,action),1,1,-99999,99999) for action in legalMoves]
    bestScore = max(scores)
    
    bestIndices = [index for index in range(len(scores)) if (scores[index] == bestScore) ]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    #print 'hahahahahhahahahahahaha The best score of the move is', bestScore, 'The best move is ', legalMoves[chosenIndex]
    return legalMoves[chosenIndex]
    
    

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    weight={'ghost2':20,'C&SG':80,'beans':0,'farGhost':0,'score':5}
    utility=0
    Food = currentGameState.getFood()
    Pos = currentGameState.getPacmanPosition()
    x = Pos[0]
    y = Pos[1]
    GhostStates = currentGameState.getGhostStates()
    #print GhostStates, 'GhostStates!!!!!!!!!'
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    #print ScaredTimes, 'ScatedTimes!!!!!!!!!'
    Capsules = currentGameState.getCapsules()
    
    walls = currentGameState.getWalls()
    top, right = walls.height-2, walls.width-2
    corners = ((1,1), (1,top), (right, 1), (right, top))
    
    
   
    
    """
    Find the closest scared ghost first then eat it
    
    """
    GhostNotScared=[]
    GhostScared=[]
    for GhostState in GhostStates:
        index=GhostStates.index(GhostState)
        if ScaredTimes[index] == 0:
            GhostNotScared = [manhattanDistance(Pos,GhostState.getPosition())for GhostState in GhostStates]
            
        else:
            GhostScared = [manhattanDistance(Pos,GhostState.getPosition())for GhostState in GhostStates]
    if GhostNotScared!=[]:
        closestGhostNotScared = min(GhostNotScared)
        if closestGhostNotScared ==1:
            utility = -9999 # death threat
            return utility # run as far away as possible
        else :
            ghostx,ghosty= GhostStates[GhostNotScared.index(closestGhostNotScared)].getPosition()
            if ((ghostx==x) or (ghosty==y)) and closestGhostNotScared==2 :
                wallx = int((ghostx+ x) /2)
                wally = int ((ghosty+y) /2)
                if walls[wallx][wally] == False:
                    utility   = utility + closestGhostNotScared *weight['ghost2'] # very dangerous, if no wall is there
                else:
                    utility = utility + closestGhostNotScared * weight['farGhost']  # medium threat
    if GhostScared!=[]:
        """
    	eat scared ghosts if someone is scared
    	"""
        closestGhostScared = min(GhostScared)
        if closestGhostScared < right/2:
            utility = utility - weight['C&SG']*closestGhostScared # chase it if it is no too far   
    else :
        #print 'SCARED!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        """
    	eat capsules if no one is scared
    	"""
        CapsuleDistance=[]
        CapsuleDistance =[manhattanDistance(Pos,Capsule)for Capsule  in Capsules]
        if CapsuleDistance!=[] :
            closestCapsule = min (CapsuleDistance)
            utility= utility- closestCapsule*weight['C&SG']
            #print 'capsules!!!!!!!!!'
    """
    for action in currentGameState.getLegalActions(0):
        newx,newy=currentGameState.generateSuccessor(0,action).getPacmanPosition()
        if Food[newx][newy]==True:
    """
                 
    i=0
    while i<max([manhattanDistance(Pos,corners[1]),manhattanDistance(Pos,corners[2]),manhattanDistance(Pos,corners[3]),manhattanDistance(Pos,corners[0])]):
        i=i+1
        for j in range(i):
            k=i-j
            if (x-j>0) :
                if (y+k<=top) and Food[x-j][y+k]==True:
                    utility = utility-manhattanDistance(Pos,(x-j,y+k))*weight['beans']                   
                    #print 'The food is in ', x-j, y+k
                    return utility+currentGameState.getScore()*weight['score']
                if (y-k>0) and Food[x-j][y-k]==True:
                    utility = utility-manhattanDistance(Pos,(x-j,y-k))*weight['beans']                   
                    #print 'The food is in ', x-j, y-k
                    return utility+currentGameState.getScore()*weight['score']
            if (x+j<=right):
                if (y+k<=top) and Food[x+j][y+k]==True:
                    utility = utility-manhattanDistance(Pos,(x+j,y+k))*weight['beans']                   
                    #print 'The food is in ', x+j,y+k
                    return utility+currentGameState.getScore()*weight['score']
                if (y-k>0) and Food[x+j][y-k]==True:
                    utility = utility-manhattanDistance(Pos,(x+j,y-k))*weight['beans']                   
                    #print 'The food is in ', x+j, y-k
                    return utility+currentGameState.getScore()*weight['score']
    return utility+currentGameState.getScore()*weight['score']

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

