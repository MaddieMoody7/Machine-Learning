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
        startState = self.mdp.getStartState()
        print("startState", startState)
        print("63", self.iterations)
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        i = 1
        #if (self.iterations == 0):
                #print("self.values 67",self.values)
        #intialize all state values to zero
        for state in self.mdp.getStates():
                #imagine state is S11
                self.values[state] = 0
        #start iterations
        #print("self.values 71", self.values)
        #before begin iterating newValue intialized
        #newValue = self.values
        while (i <= self.iterations):
            print("i ", i)
            #once iterating
            #print("self values 78", self.values)
            #self.values = newValue
            #create dict to hold new values for each state
            #so will do batch update at end of iteration
            newValue = {}
            policy = {}
            #prevValue = {}
            qNode = []
            if (i == 100 ):
                print("i " , i, "self.values 77", self.values, "policy ", policy)
        
            #get first state to compute new value from
            for state in self.mdp.getStates():

                #make sure not at end
                if self.mdp.isTerminal(state):
                    newValue[state]=0
                else:
                    #start iterating through possible actions for given state
                    for action in self.mdp.getPossibleActions(state):
                        #get new Q value for each state action
                        qNode.append(self.computeQValueFromValues(state,action))
                        #for each action compute the q value and store into qNode
                        #once all the q values for each action have been computed 
                        #find the max values
                        """do I want to store the action that gives the max value 
                        for use in creating a policy?
                        """
                    #newValue holds all the updated values for each state
                    newValue[state]=max(qNode)
                    #reset qNode values so ready for next action
                    qNode.clear()
                bestAction = self.computeActionFromValues(state)
                policy[state] = bestAction
            print("policy", policy)
            #once all the states have been updated put the new batch of files 
            #into the values dict
            #print("self.values 100", self.values, "newValue", newValue)
            #prevValue = self.values
            #print("114 policy ", policy)
            self.values = newValue
            #iterate through again
            i = i+1
        return self.values
    
                

            
        #self.computeQValueFromValues

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Qvalue = []
        #move through possible transitions ie what is the transition value for each s,a,s' value
        for sNext, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            # hold holds return pair of nestState prob pairs
            #reward function uses sNext and computes reward from that
            reward = self.mdp.getReward(state, action, sNext)
            # now that have all parts do the Bellmen eqt
            #major questions around using self.values here?
            #print("selfvalues 154", self.values)
            Qvalue.append(prob*(reward + (self.discount*(self.values[sNext]))))
            #print("selfvalues 156", self.values)
            # when/where to define sNext
            # sNext as self.Values
           
        return(sum(Qvalue))

        #util.raiseNotDefined()
    
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #print("incomputeAction")
        
        if (self.mdp.getPossibleActions(state) == 0):
            return None
        elif (self.mdp.isTerminal(state)):
            return None
        else:
            QValuesForActions = {}
            AllActions = self.mdp.getPossibleActions(state)
            for actions in AllActions:
                QValuesForActions[actions]=self.computeQValueFromValues(state,actions)
            maxAction = max(QValuesForActions, key = QValuesForActions.get)
            return(maxAction)



                

        #util.raiseNotDefined()

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

