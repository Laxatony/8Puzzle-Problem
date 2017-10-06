import msvcrt
import sys
import copy
import random
import math
import time
from heapq import heappush, heappop                                             

g_GoalState = []
g_totalCreatedNode = 0
g_totalStep = 0

def Manhattan_Distance(state):
	#calculate the Manhattn Distance of each tiles from current state to goal state

	global g_GoalState
	
	totalCost = 0
	for num in range(1,9):
		goalIndex = g_GoalState.index(num)
		curIndex = state.index(num)
		(goal_coordX, goal_coordY) = (int(goalIndex / 3), goalIndex % 3)
		(cur_coordX, cur_coordY) = (int(curIndex / 3), curIndex % 3)
		totalCost += abs(goal_coordX-cur_coordX) + abs(goal_coordY-cur_coordY)
	return totalCost

class stateNode:
	def __init__(self, parentState, state, step):
		self.parentState = parentState
		self.state = state
		self.gCost = step
		self.hCost = Manhattan_Distance(state)
		self.fCost = self.gCost + self.hCost
		
		self.alternativeCost = 0
		
	def getGCost(self):
		return self.gCost
		
	def setAlternativeCost(self, cost):
		self.alternativeCost = cost
	def getAlternativeCost(self, cost):
		return self.alternativeCost


def setGoalState(puzzle):
	
	goalState = []
	totalCount = 0
	
	for i, num in enumerate(puzzle):
		for j in range(i+1, len(puzzle)):
			if puzzle[j] != 0 and num > puzzle[j]:
				totalCount += 1
				
	if totalCount % 2 == 0:
		goalState = [1,2,3,\
					 4,5,6,\
					 7,8,0]
	else:
		goalState = [1,2,3,\
					 8,0,4,\
					 7,6,5]
					 
	return goalState
	
	
def printState(curState):
	for i in range(0,3):
		print(curState[i*3], curState[i*3+1], curState[i*3+2])
	print('\n')
		
def printStateNode(curStateNode):	
	printState(curStateNode.state)
	print("f(n) = g(n) + h(n) => ", curStateNode.fCost , " = ", curStateNode.gCost, " + ", curStateNode.hCost)
	print('\n')

def expendAvailabelStateNode(curStateNode):
	# This function is used for expend next candidate states.
	# The state will be put into a priority queue. 
	
	global g_totalCreatedNode
	
	successors = []
	# use heappush(g_myPQ_bestState, (curStateNode.fCost, curStateNode.hCost, curStateNode))
	zeroIndex = curStateNode.state.index(0)
	
	coordX = int(zeroIndex / 3)
	coordY = zeroIndex % 3
	
	# get available moving position
	available_coordinate = []
	for x in range(coordX-1, coordX+2):
		for y in range(coordY-1, coordY+2):
			if x >= 0 and x <= 2 and y >=0 and y <= 2 \
			   and (x,y) != (coordX, coordY) and (abs(x-coordX) + abs(y-coordY)) == 1:
				available_coordinate.append((x,y))
	
	# switch zero with data in moving position
	for position in available_coordinate:
		nextState = copy.deepcopy(curStateNode.state)
		nextState[3*coordX+coordY] = nextState[3*position[0]+position[1]]
		nextState[3*position[0]+position[1]] = 0
		
		nextStateNode = stateNode(curStateNode.state, nextState, curStateNode.getGCost()+1)	
		heappush(successors, (nextStateNode.fCost, nextStateNode.hCost, nextStateNode.gCost, nextStateNode.state, nextStateNode))
		g_totalCreatedNode += 1
		
	return successors

def eight_puzzle_RBFS(curStateNode, fLimit):
	# execute RBFS algorithm for problem
	global g_GoalState
	global g_totalStep
	global g_totalCreatedNode

	if curStateNode.state == g_GoalState:
		return True, curStateNode.fCost

	successors_PQ = expendAvailabelStateNode(curStateNode)
	#print("successor num:", len(successors_PQ))
	if len(successors_PQ) == 0:
		return False, math.inf

	isTrue = False
	while not isTrue:
		bestSuccessor_PQ = heappop(successors_PQ)
		g_totalStep += 1
		bestSuccessor = bestSuccessor_PQ[4]
		bestCost = bestSuccessor.fCost
		if bestCost > fLimit:
			return False, bestCost
			
		secondSuccessor_PQ = successors_PQ[0]
		secondSuccessor = secondSuccessor_PQ[4]
		bestSuccessor.alternativeCost = secondSuccessor.fCost
	
		
		isTrue, bestCost = eight_puzzle_RBFS(bestSuccessor, min(fLimit, bestSuccessor.alternativeCost))
		bestSuccessor.fCost = bestCost
		heappush(successors_PQ, (bestSuccessor.fCost, bestSuccessor.hCost, bestSuccessor.gCost, bestSuccessor.state, bestSuccessor))
		g_totalCreatedNode += 1
		
		if isTrue:
			return True, bestCost
			
def main():
	# read test puzzles from disk
	# run each puzzle and save the performance result into a txt file
	
	global g_GoalState
	global g_totalCreatedNode
	global g_totalStep
	
	'''
	f = open('testPuzzle.txt', 'w')
	for i in range(0,10):
		puzzle = random.sample(range(0,9), 9)
		f.write(str(puzzle) + "\n")
	f.close()
	'''
	
	puzzles= []
	f = open('testPuzzle.txt', 'r')
	for line in f:
		line = line[1:-2]
		line = line.split(', ')
		line = list(map(int, line))
		puzzles.append(line)
	f.close()
	

	f = open('8puzzle_result_RBFS.txt', 'w')
	for i, puzzle in enumerate(puzzles):
		print("Testing Case:", i+1 , " .....")
		start_time = time.time()
		g_GoalState = setGoalState(puzzle)
		curStateNode = stateNode([], puzzle, 0)
	
		#print("Initial puzzle:")
		#printState(curStateNode.state)
	
		#print("Goal State:", goalState)
	
		result, bestCost = eight_puzzle_RBFS(curStateNode, math.inf)
		
		end_time = time.time()
		exTime = end_time - start_time
		exeLog = ""
		exeLog = str(i+1) + " Total Cost: " + str(bestCost) + " Executeion Time: " \
				 + str(exTime) + " NodeCreated: " + str(g_totalCreatedNode) + " Steps: " + str(g_totalStep) + "\n"
		f.write(exeLog)
		g_totalCreatedNode  = 0
		g_totalStep = 0
	f.close()	
	print("Done")
	
if __name__ == '__main__':
	main()