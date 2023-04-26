# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.Qvalues = util.Counter()
        #self.actions
        #self.accumTestRewards
        self.getActionCalled = 0
        self.DebugCount = 0
        """self.episodeRewards
        self.episodesSoFar
        self.episodeStartTime
        self.lastAction
        self.Qvalues = util.Counter()
             actionFn = lambda state: state.getLegalActions()
        
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)"""

        
        
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #compute Q value no max just the value of the Q node
        #self.values[(state,action)] = (1-(self.alpha)) + self.alpha*(self.accumTrainRewards[(state,action)]+2)
        #print("75", self.Qvalues[(state,action)])
        return self.Qvalues[(state,action)]
        #util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        #get all possible actions
        #returning Qvalue of best action
        #add terminal check?
        #what does getLegalActions return in a terminal state
        #None, 0 or exit?
        '''def isTerminal(state):
            PossibleActions = self.getLegalActions(state)
            print("96 ", state, PossibleActions)
            ActionLen = len(PossibleActions)
            FirstArg = PossibleActions[0]
            if((ActionLen == 1) & (FirstArg == 'exit')):
                return True
            else:
                return False'''
        Actions = self.getLegalActions(state)
        print("95 state " ,state, "actions", Actions)
        if (state == 'TERMINAL_STATE'):
            return 0.0
        else:
            QsPerAction = {}
            for actions in Actions:
                QsPerAction[actions]=self.getQValue(state, actions)
            QValuesList = list(QsPerAction.values())
            maxAction = max(QValuesList)
            return(maxAction)
        #if(Actions == 'exit'):
            #return 0.0
        if(Actions == 'exit'):
            return 0.0
        QsPerAction = {}
        for actions in Actions:
            #print("105", self.getQValue(state,actions) )
            QsPerAction[actions]=self.getQValue(state, actions)
        #print("105",QsPerAction)
        action = max(QsPerAction, key = QsPerAction.get)
        #QValuesList = list(QsPerAction.values())
        #maxQValue = 0
        #for i in range(0,len(QValuesList)):
         #   if (int(QValuesList[i]) > 0):
           #     maxQValue = QValuesList[i]
        return action
        #self.values[(state,action)] = (1-(self.alpha)) + self.alpha*(self.accumTrainRewards[(state,action)]+2)
        #hold = self.util.experinces.get_experinces()
        #util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        #returning best action
        # include tie breaker for when all Qvalues are the same
        
        Actions = self.getLegalActions(state)
        #print("138", Actions)
        if (Actions == 'exit'):
            return None
        else:
          #fill up dictionary with action:Qvalues
          QsPerAction = {}
          for actions in Actions:
            QsPerAction[actions]=self.getQValue(state, actions)
            #print("146", QsPerAction)
          #return None
          AllEqual = 1
          #QsPerAction = {'south':1, 'north':4, 'west':3, 'east':5}
          maxKey = max(QsPerAction, key = QsPerAction.get)
          #print("143 Maxkey", maxKey)
          action = maxKey
          QValueList = list(QsPerAction.values())
          # check and see if every Q value is the same
          for i in range(1,len(QValueList)):
              #print("i ",i)
              #print(QValueList[0], QValueList[i])
              #enter the if statement only when there is a non match
              #meaning not every Qvalue is the same
              if(QValueList[0] != QValueList[i]):
                  AllEqual = 0
          if (AllEqual == 1):
                  #know that all equal so now need to chose some random action
                 # print("in Allequal")
                  action = random.choice(Actions)
          return action
    
         # return QsPerAction[maxKey]
        #util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        Actions = self.getLegalActions(state)
       # print("181", Actions)
        doRandom = util.flipCoin(self.epsilon)
        
        if (doRandom):
          if (self.getLegalActions == None):
            action = None
          else:
            action = random.choice(Actions)
        else:
            action = self.computeActionFromQValues(state)
        return action
       # action = None
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #action = self.getAction(state)
       # self.accumTestRewards 
        #ActionToDo = self.getAction(state)
        #reward, NextState = self.doAction(state,action)
        #if ((state == (0,1))&(action == 'north')):
        self.DebugCount = self.DebugCount + 1
        #if (self.DebugCount == 100):
            #print("214 debug")
            #print("qvalues ", self.Qvalues)
        
        firsterm = (1-self.alpha)*(self.getQValue(state,action))
        secondterm = (reward+(self.discount*(self.computeValueFromQValues(nextState))))
        #if (self.DebugCount == 1):
           # print("action ", action, "state ", state)
          #  print(firsterm + (self.alpha*secondterm))
        self.Qvalues[(state,action)] = firsterm + (self.alpha*secondterm)
        #if (self.DebugCount == 100):
          #  print(self.Qvalues)
       # print("209", self.Qvalues)
        #util.raiseNotDefined()
        return self.Qvalues

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        Actions = QLearningAgent.getAction(self,state)
        print("qlearning 275 ",Actions)
        if (Actions == 0):
            action = None
        else:
          randActionList = []
          for i in range(0,100):
              randActionList.append(0)
          for i in range(0,(int(self.epsilon*100))):
              randActionList.append(1)
          random.shuffle(randActionList)
        #print(randActionList)

class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter() # differnt keys for features

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        #util.__mul__()
        def dotProduct(x, y):
            sum = 0
            if len(x) > len(y):
                x, y = y, x
            for key in x:
                if key not in y:
                    continue
                sum += x[key] * y[key]
            return sum
        w = self.getWeights()
        features = IdentityExtractor.getFeatures(self,state,action)
        print("w",w)
        print("features", features)
        Qsa = dotProduct( w,features)
        return Qsa
    #util.__mul__(w,features)
        #if use getFeatures need to define over in Feature Extractor
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        #gradient descent from lecture
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        look = self.getQValue(nextState,action)
        print(look)
        difference = (reward + ((0.8)*self.getQValue(nextState,action)))-(self.getQValue(state,action))
        self.weights[(state,action)]= (self.weights[(state,action)])+(self.alpha*difference*IdentityExtractor.getFeatures(self,state,action))
        #util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            #debug can moniter wieghts
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
