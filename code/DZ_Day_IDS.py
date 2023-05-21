from collections import defaultdict
import time

class State:
    pos: int
    doneRecipes = []
    doneDevotees = []
    path = []
    nodeTime: int
    hardNodes = {}

    def __init__(self, _pos_, _doneRecipes_, _doneDevotees_, _path_, _nodeTime_, _hardNodes_):
        self.pos = _pos_
        self.doneRecipes = _doneRecipes_
        self.doneDevotees = _doneDevotees_
        self.path = _path_
        self.nodeTime = _nodeTime_
        self.hardNodes = _hardNodes_

def printPathOfGoalState(goalState):
    counter = 0
    for i in goalState.path:
        counter = counter + 1
        if (counter != len(goalState.path)):
            print(i, end = "->")
        else:
            print(i)

def createGraph(graph, edge):
    graph[edge[0]].append(edge[1])
    graph[edge[1]].append(edge[0])

def checkSeenRecipes(recipes, DoneRecipes):
    counter = 0
    for i in recipes:
        for j in DoneRecipes:
            if (i == j):
                counter = counter + 1
    if (counter == len(recipes)):
        return True
    else:
        return False

def checkDuplicateState(visited, newState):
    for state in visited:
        counter = 0
        if (state.pos == newState.pos):
            counter = counter + 1
        if (len(set(state.doneRecipes) & set(newState.doneRecipes)) == len(state.doneRecipes) and len(set(state.doneRecipes) & set(newState.doneRecipes)) == len(newState.doneRecipes)):
            counter = counter + 1
        if (len(set(state.doneDevotees) & set(newState.doneDevotees)) == len(state.doneDevotees) and len(set(state.doneDevotees) & set(newState.doneDevotees)) == len(newState.doneDevotees)):
            counter = counter + 1
        if (counter == 3):
            return False
    return True

def checkExistHardNode(state):
    for i in state.hardNodes:
        if (i == state.pos):
            return True
    return False

def checkGoalState(state, allDevotees):
    if (len(set(state.doneDevotees) & set(allDevotees)) == len(state.doneDevotees) and len(set(state.doneDevotees) & set(allDevotees)) == len(allDevotees)):
        return state

def findNextStates(state, graph, visited, recipes, devotees):
    allNewStates = []
    if(checkExistHardNode(state)):
        if (state.nodeTime < state.hardNodes.get(state.pos) - 1):
            newState = State(state.pos, state.doneRecipes, state.doneDevotees, state.path, state.nodeTime + 1, state.hardNodes)
            numOfState[0] = numOfState[0] + 1
            allNewStates.append(newState)
            return allNewStates
    for node in graph.get(state.pos):
        newPos: int
        newDoneRecipes = []
        newDoneDevotees = []
        newPath = []
        newHardNodes = {}

        newPos = node

        newDoneRecipes = state.doneRecipes.copy()
        if (recipes[node] == 1):
            newDoneRecipes.append(node)
        newDoneRecipes = list(dict.fromkeys(newDoneRecipes))
        
        newDoneDevotees = state.doneDevotees.copy()
        for j in devotees:
            if (checkSeenRecipes(devotees[j], newDoneRecipes) == True and j == newPos):
                newDoneDevotees.append(j)
        newDoneDevotees = list(dict.fromkeys(newDoneDevotees))

        newPath = state.path.copy()
        newPath.append(node)

        newHardNodes = state.hardNodes.copy()
        for k in newHardNodes:
            if (k == node):
                newHardNodes[k] = newHardNodes[k] + 1
        newState = State(node, newDoneRecipes, newDoneDevotees, newPath, 0, newHardNodes)
        
        if (checkDuplicateState(visited, newState)):
            allNewStates.append(newState)
            numOfState[0] = numOfState[0] + 1
            
    return allNewStates

def DFS(state, graph, visited, allRecipes, devotees, allDevotees, counter):
    goalState1 = checkGoalState(state, allDevotees)
    if (goalState1 != None):
        return goalState1
    if (counter <= 0):
        return None
    nextStates = findNextStates(state, graph, visited, allRecipes, devotees)
    visited.append(state)
    for i in nextStates:
        goalState2 = DFS(i, graph, visited.copy(), allRecipes, devotees, allDevotees, counter - 1)
        if(goalState2 != None):
            return goalState2
    return None

def IDS(firstState, graph, visited, allRecipes, devotees, allDevotees):
    counter = 0
    while (True):
        goalState = DFS(firstState, graph, visited, allRecipes, devotees, allDevotees, counter)
        visited.clear()
        if (goalState != None):
            return goalState
        counter = counter + 1
    return None

start = time.time()
fileDZ = open("input2.txt", "r")
graph = defaultdict(list)
hardNodes = []
devotees = {}

line = fileDZ.readline()
n, m = line[0:-1].split(" ")
for i in range(0, int(m)):
    line = fileDZ.readline()
    line = line[0:-1].split(" ")
    line = list(map(int, line))
    createGraph(graph, line)

h = fileDZ.readline()[0:-1]
line = fileDZ.readline()
hardNodes = line[0:-1].split(" ")

allRecipes = []
allDevotees = []
for k in range(0, int(n) + 1):
    allRecipes.append(0)
s = fileDZ.readline()[0:-1]
for i in range(0, int(s)):
    line = fileDZ.readline()
    elements = line[0:-1].split(" ")
    p = elements[0]
    q = elements[1]
    allDevotees.append(int(p))
    recipes = elements[2:]
    recipes = list(map(int, recipes))
    for j in recipes:
        allRecipes[j] = 1
    devotees[int(p)] = recipes

v = fileDZ.readline()
fileDZ.close()

dictHardNodes = {}
for i in hardNodes:
    dictHardNodes[int(i)] = 0

numOfState = [0]
startPlace = []
startPlace.append(int(v))
firstState = State(int(v), [], [], startPlace, 0, dictHardNodes)
numOfState[0] = numOfState[0] + 1
visited = []

goalState = IDS(firstState, graph, visited, allRecipes, devotees, allDevotees)
printPathOfGoalState(goalState)
end = time.time()
print("time execution :", (end-start) * 10**3, "ms")
print("number of seen states : ", numOfState[0])