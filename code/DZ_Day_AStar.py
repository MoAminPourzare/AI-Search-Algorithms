from collections import defaultdict
import time

class State:
    pos: int
    doneRecipes = []
    doneDevotees = []
    path = []
    nodeTime: int
    hardNodes = {}
    heuristic: int

    def __init__(self, _pos_, _doneRecipes_, _doneDevotees_, _path_, _nodeTime_, _hardNodes_, _heuristic_):
        self.pos = _pos_
        self.doneRecipes = _doneRecipes_
        self.doneDevotees = _doneDevotees_
        self.path = _path_
        self.nodeTime = _nodeTime_
        self.hardNodes = _hardNodes_
        self.heuristic = _heuristic_

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

def calculateNumOfRecipes(allRecipes):
    recipes = []
    for i in range(len(allRecipes)):
        if (allRecipes[i] == 1):
            recipes.append(i)
    return recipes

def findGoalState(nextStates, allDevotees):
    for state in nextStates:
        if (len(set(state.doneDevotees) & set(allDevotees)) == len(state.doneDevotees) and len(set(state.doneDevotees) & set(allDevotees)) == len(allDevotees)):
            return state

def lenUniqueDevRecSeen(newDoneDevotees, newDoneRecipes):
    temp = []
    temp.extend(newDoneDevotees)
    temp.extend(newDoneRecipes)
    temp = list(dict.fromkeys(temp))
    return len(temp)


def findNextStates(state, graph, visited, recipes, devotees, uniqueDevRec):
    allNewStates = []
    if(checkExistHardNode(state)):
        if (state.nodeTime < state.hardNodes.get(state.pos) - 1):
            newState = State(state.pos, state.doneRecipes, state.doneDevotees, state.path, state.nodeTime + 1, state.hardNodes, state.heuristic + 1)
            numOfState[0] = numOfState[0] + 1
            allNewStates.append(newState)
            return allNewStates
    for node in graph.get(state.pos):
        newPos: int
        newHeuristic: int
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
        
        UniqueDevRecSeen = lenUniqueDevRecSeen(newDoneDevotees, newDoneRecipes)

        newHeuristic = len(newPath) + (uniqueDevRec - UniqueDevRecSeen)
        newState = State(node, newDoneRecipes, newDoneDevotees, newPath, 0, newHardNodes, newHeuristic)

        if (checkDuplicateState(visited, newState)):
            allNewStates.append(newState)
            numOfState[0] = numOfState[0] + 1
            
    return allNewStates

def findBestState(listOfStates):
    minHeuristic = 1000
    indexOfMinH: int
    counter = 0
    for state in listOfStates:
        if (state.heuristic < minHeuristic):
            minHeuristic = state.heuristic
            indexOfMinH = counter
        counter = counter + 1
    return indexOfMinH

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

startPlace = []
startPlace.append(int(v))

uniqueDevotees = allDevotees.copy()
uniqueRecipes = calculateNumOfRecipes(allRecipes)

uniqueRecipes.extend(uniqueDevotees)

uniqueRecipes = list(dict.fromkeys(uniqueRecipes))
numOfState = [0]
firstState = State(int(v), [], [], startPlace, 0, dictHardNodes, len(uniqueRecipes))
numOfState[0] = numOfState[0] + 1
visited = []
listOfStates = []
listOfStates.append(firstState)
while listOfStates:
    indexOfMinH = findBestState(listOfStates)
    visited.append(listOfStates[indexOfMinH])
    nextStates = findNextStates(listOfStates[indexOfMinH], graph, visited, allRecipes, devotees, len(uniqueRecipes))
    del listOfStates[indexOfMinH]
    goalState = findGoalState(nextStates, allDevotees)
    if (goalState != None):
        printPathOfGoalState(goalState)
        break
    for k in nextStates:
        listOfStates.append(k)

end = time.time()
print("time execution :", (end-start) * 10**3, "ms")
print("number of seen states : ", numOfState[0])