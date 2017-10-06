import msvcrt
import sys
import copy
import random
import time
from heapq import heappush, heappop
     
g_GoalState = []
g_myPQ_bestStateNode = []
g_historicalState = []
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
		
	def getGCost(self):
		return self.gCost

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
	# The state will be put into a priority queue is it hasn't be generated before. 
	
	global g_myPQ_bestStateNode
	global g_historicalState
	global g_totalCreatedNode
	
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
		
		if not nextState in g_historicalState:
			nextStateNode = stateNode(curStateNode.state, nextState, curStateNode.getGCost()+1)
			heappush(g_myPQ_bestStateNode, (nextStateNode.fCost, nextStateNode.hCost, nextStateNode.gCost, nextStateNode.state, nextStateNode))
			g_historicalState.append(nextStateNode.state)
			g_totalCreatedNode += 1

def eight_puzzle_AStar():
	# execute A* algorithm for problem
	global g_myPQ_bestStateNode
	global g_historicalState
	global g_totalStep

	if len(g_myPQ_bestStateNode) <= 0:
		return 0

	count = 0
	pqStruct = heappop(g_myPQ_bestStateNode)
	g_totalStep += 1
	curStateNode = pqStruct[4]
	while not curStateNode.state == g_GoalState:

		expendAvailabelStateNode(curStateNode)
		
		if len(g_myPQ_bestStateNode) <= 0:
			print("Fail to find a solution.")
			return -1
		else:
			pqStruct = heappop(g_myPQ_bestStateNode)
			g_totalStep += 1
			curStateNode = pqStruct[4]
			#printStateNode(curStateNode)
			
		count += 1
			
	#if curStateNode.hCost != 0:
	#	print("Issue!")
		
	return curStateNode
	
	
def main():
	# read test puzzles from disk
	# run each puzzle and save the performance result into a txt file 
	global g_myPQ_bestStateNode
	global g_historicalState
	global g_GoalState
	global g_totalCreatedNode
	global g_totalStep
	
	puzzles= []
	f = open('testPuzzle.txt', 'r')
	for line in f:
		line = line[1:-2]
		line = line.split(', ')
		line = list(map(int, line))
		puzzles.append(line)
	f.close()
	
	f = open('8puzzle_result_AStar.txt', 'w')
	for i, puzzle in enumerate(puzzles):
		print("Testing Case:", i+1 , " .....")
		start_time = time.time()
		
		g_GoalState = setGoalState(puzzle)
	
		curStateNode = stateNode([], puzzle, 0)
		heappush(g_myPQ_bestStateNode, (curStateNode.fCost, curStateNode.hCost, curStateNode.gCost, curStateNode.state, curStateNode))
		g_historicalState.append(curStateNode.state)
		g_totalCreatedNode += 1
	
		#print("Initial puzzle:")
		#printState(curStateNode.state)
	
		#print("Goal State:", goalState)
	
		resultStateNode = eight_puzzle_AStar()
		bestCost = resultStateNode.fCost
		
		end_time = time.time()
		exTime = end_time - start_time
		exeLog = ""
		exeLog = str(i+1) + " Total Cost: " + str(bestCost) + " Executeion Time: " \
				 + str(exTime) + " NodeCreated: " + str(g_totalCreatedNode) + " Steps: " + str(g_totalStep) + "\n"
		f.write(exeLog)
		g_myPQ_bestStateNode = []
		g_historicalState = []
		g_totalCreatedNode  = 0
		g_totalStep = 0
	f.close()	
	print("Done")
	
	
if __name__ == '__main__':
	main()