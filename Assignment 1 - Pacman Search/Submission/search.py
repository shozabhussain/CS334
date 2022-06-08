# M.Shozab Hussain
# 23100174
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

	def getSuccessors(self, state):
		"""
		  state: Search state

		For a given state, this should return a list of triples, (successor,
		action, stepCost), where 'successor' is a successor to the current
		state, 'action' is the action required to get there, and 'stepCost' is
		the incremental cost of expanding to that successor.
		"""
		util.raiseNotDefined()

	def getCostOfActions(self, actions):
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
		"""
	#print("Start:", problem.getStartState())
	# print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
	# print("Start's successors:", problem.getSuccessors(problem.getStartState()))
			
	"Start of Your Code"
 
	visited = []
	path = []
	stack = util.Stack()
	stack.push( (problem.getStartState(), path) )

	while True:
     
		if stack.isEmpty():
			return
		
		else:
			item = stack.pop()
			currentState = item[0]
			path = item[1]

			if problem.isGoalState(currentState):
				return path

			elif currentState in visited:
				continue

			else:
				visited.append(currentState)
				children = problem.getSuccessors(currentState)

				for child in children:
					childState = child[0]
					childAction = child[1]
					stack.push( (childState, path+[childAction]) )

# ________________________________________________________________

class _RecursiveDepthFirstSearch(object):
	'''
		=> Output of 'recursive' dfs should match that of 'iterative' dfs you implemented
		above. 
		Key Point: Remember in tutorial you were asked to expand the left-most child 
		first for dfs and bfs for consistency. If you expanded the right-most
		first, dfs/bfs would be correct in principle but may not return the same
		path. 

		=> Useful Hint: self.problem.getSuccessors(node) will return children of 
		a node in a certain "sequence", say (A->B->C), If your 'recursive' dfs traversal 
		is different from 'iterative' traversal, try reversing the sequence.  

	'''
	def __init__(self, problem):
		" Do not change this. " 
		# You'll save the actions that recursive dfs found in self.actions. 
		self.actions = [] 
		# Use self.explored to keep track of explored nodes.  
		self.explored = set()
		self.problem = problem

	def RecursiveDepthFirstSearchHelper(self, node):
		'''
		args: start node 
		outputs: bool => True if path found else Fasle.
		'''
		"Start of Your Code"

		if self.problem.isGoalState(node):
			self.actions.reverse()
			return True

		children = self.problem.getSuccessors(node)
   
		for child in reversed(children):
			childState = child[0]
			childAction = child[1]
			
			if childState not in self.explored:
				self.explored.add(childState)
				self.actions.append(childAction)
				if self.RecursiveDepthFirstSearchHelper(childState) == True:
					return True
				self.actions.pop()
    
		return False


def RecursiveDepthFirstSearch(problem):
	" You need not change this function. "
	# All your code should be in member function 'RecursiveDepthFirstSearchHelper' of 
	# class '_RecursiveDepthFirstSearch'."

	node = problem.getStartState() 
	rdfs = _RecursiveDepthFirstSearch(problem)
	path_found = rdfs.RecursiveDepthFirstSearchHelper(node)
	return list(reversed(rdfs.actions)) # Actions your recursive calls return are in opposite order.
# ________________________________________________________________


def depthLimitedSearch(problem, limit = 210):

	"""
	Search the deepest nodes in the search tree first as long as the
	nodes are not not deeper than 'limit'.

	For medium maze, pacman should find food for limit less than 130. 
	If your solution needs 'limit' more than 130, it's bogus.
	Specifically, for:
	'python pacman.py -l mediumMaze -p SearchAgent -a fn=dls', and limit=130
	pacman should work normally.  

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.
	Autograder cannot test this function.  

	Hints: You may need to store additional information in your frontier(queue).

		"""

	"Start of Your Code"
	visited = []
	path = []
	depth = 0
	stack = util.Stack()
	stack.push( (problem.getStartState(), path, depth) )
	
	while True:

		if stack.isEmpty():
			return

		else:
			item = stack.pop()
			currentState = item[0]
			path = item[1]
			depth = item[2]
	
			if problem.isGoalState(currentState):
				return path

			elif currentState in visited:
				continue

			elif depth > limit:
				depth = depth -1
				continue

			elif depth <= limit:
				depth = depth + 1
				visited.append(currentState)
				children = problem.getSuccessors(currentState)
				
				for child in children:
					childState = child[0]
					childAction = child[1]
					stack.push( (childState, path+[childAction], depth))
	"End of Your Code"

# ________________________________________________________________

class _RecursiveDepthLimitedSearch(object):
	'''
		=> Output of 'recursive' dfs should match that of 'iterative' dfs you implemented
		above. 
		Key Point: Remember in tutorial you were asked to expand the left-most child 
		first for dfs and bfs for consistency. If you expanded the right-most
		first, dfs/bfs would be correct in principle but may not return the same
		path. 

		=> Useful Hint: self.problem.getSuccessors(node) will return children of 
		a node in a certain "sequence", say (A->B->C), If your 'recursive' dfs traversal 
		is different from 'iterative' traversal, try reversing the sequence.  

	'''
	def __init__(self, problem):
		" Do not change this. " 
		# You'll save the actions that recursive dfs found in self.actions. 
		self.actions = [] 
		# Use self.explored to keep track of explored nodes.  
		self.explored = set()
		self.problem = problem
		self.current_depth = 0
		self.depth_limit = 204 # For medium maze, You should find solution for depth_limit not more than 204.

	def RecursiveDepthLimitedSearchHelper(self, node):
		'''
		args: start node 
		outputs: bool => True if path found else Fasle.
		'''

		"Start of Your Code"

		if self.problem.isGoalState(node):
			self.actions.reverse()
			return True

		children = self.problem.getSuccessors(node)
		self.current_depth = self.current_depth + 1
   
		for child in children:
			childState = child[0]
			childAction = child[1]
			
			if childState not in self.explored and self.current_depth <= self.depth_limit:
				self.explored.add(childState)
				self.actions.append(childAction)
				if self.RecursiveDepthLimitedSearchHelper(childState) == True:
					return True
				self.actions.pop()
			else:
				self.current_depth = self.current_depth - 1
				continue
    
		return False
		"End of Your Code"


def RecursiveDepthLimitedSearch(problem):
	"You need not change this function. All your code in member function RecursiveDepthLimitedSearchHelper"
	node = problem.getStartState() 
	rdfs = _RecursiveDepthLimitedSearch(problem)
	path_found = rdfs.RecursiveDepthLimitedSearchHelper(node)
	return list(reversed(rdfs.actions)) # Actions your recursive calls return are in opposite order.
# ________________________________________________________________


def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""

	"Start of Your Code"
	visited = []
	path = []
	queue = util.Queue()
	queue.push( (problem.getStartState(), path) )
	
	while True:
		
		if queue.isEmpty():
			return

		else:
			item = queue.pop()
			currentState = item[0]
			path = item[1]
	
			if problem.isGoalState(currentState):
				return path

			elif currentState in visited:
				continue

			else:
				visited.append(currentState)
				children = problem.getSuccessors(currentState)
	
				for child in children:
					childState = child[0]
					childAction = child[1]
					queue.push( (childState, path+[childAction]) )
 
	"End of Your Code"


def uniformCostSearch(problem):
	"""Search the node of least total cost first.
	   You may need to pay close attention to util.py.
	   Useful Reminder: Note that problem.getSuccessors(node) returns "cost". 

	   Key Point: If a node is already present in the queue with higher path cost 
	   (or higher priority), you'll update its cost (or priority) 
	   (Similar to pseudocode in figure 3.14 of your textbook.). 
	   Be careful, autograder cannot catch this bug.
	"""

	"Start of Your Code"
 
	visited = []
	path = []
	queue = util.PriorityQueue()
	queue.push( (problem.getStartState(), []), path )
	
	while True:
     
		if queue.isEmpty():
			return

		else:
			item, priority = queue.pop()
			currentState = item[0]
			path = item[1]
	
			if problem.isGoalState(currentState):
				return path

			elif currentState in visited:
				continue

			else:
				visited.append(currentState)
				children = problem.getSuccessors(currentState)
	
				for child in children:
					childState = child[0]
					childAction = child[1]
					queue.push( (childState, path+[childAction]), problem.getCostOfActions(path+[childAction]))
	

	"End of Your Code"

def nullHeuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	'''
	Pay clos attention to util.py- specifically, args you pass to member functions. 

	Key Point: If a node is already present in the queue with higher path cost 
	(or higher priority), you'll update its cost (or priority) 
	(Similar to pseudocode in figure 3.14 of your textbook.). 
	Be careful, autograder cannot catch this bug.

	'''
	"Start of Your Code"
	visited = []
	path = []
	queue = util.PriorityQueue()
	queue.push( (problem.getStartState(), path), 0+heuristic(problem.getStartState(), problem) )

	while True:

		if queue.isEmpty():
			return

		else:
			item, priority = queue.pop()
			currentState = item[0]
			path = item[1]

			if problem.isGoalState(currentState):
				return path

			elif currentState in visited:
				continue

			else:
				visited.append(currentState)
				children = problem.getSuccessors(currentState)

				for child in children:
					childState = child[0]
					childAction = child[1]
					queue.push( (childState, path+[childAction]), problem.getCostOfActions(path+[childAction])+heuristic(childState, problem))
	
	"End of Your Code"


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
rdfs = RecursiveDepthFirstSearch
dls = depthLimitedSearch
rdls = RecursiveDepthLimitedSearch
astar = aStarSearch
ucs = uniformCostSearch
