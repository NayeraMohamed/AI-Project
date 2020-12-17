from collections import deque
class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function
    parentS = None  #for BDS search
    parentE = None  #for BDS search

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    startNode = None
    goalNode = None

    def __init__(self, mazeStr, heristicValue=None):

        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        rows = mazeStr.split()
        rowsNumber, colsNumber = (len(rows), int(len(rows[0]) / 2) + 1)
        maze = [[Node(None) for j in range(colsNumber)] for i in range(rowsNumber)]
        idCounter = 0
        heristicCounter = 0
        for i in range(rowsNumber):
            columnCounter = 0
            for j in range(colsNumber):
                maze[i][j].id = idCounter
                maze[i][j].value = rows[i][columnCounter]
                if heristicValue is not None:
                    maze[i][j].hOfN = heristicValue[heristicCounter]
                    heristicCounter += 1
                idCounter += 1
                columnCounter += 2 #to ignore column separators(',')
                #first row
                if i == 0:
                    maze[i][j].down = maze[i + 1][j]
                    if j != 0:
                        maze[i][j].left = maze[i][j - 1]
                    if j is not colsNumber - 1:
                        maze[i][j].right = maze[i][j + 1]
                #last row
                elif i == rowsNumber - 1:
                    maze[i][j].up = maze[i-1][j]
                    if j != 0:
                        maze[i][j].left = maze[i][j - 1]
                    if j is not colsNumber - 1:
                        maze[i][j].right = maze[i][j + 1]
                #first column
                elif j == 0:
                    maze[i][j].up = maze[i - 1][j]
                    maze[i][j].down = maze[i + 1][j]
                    maze[i][j].right = maze[i][j + 1]
                #last column
                elif j == colsNumber - 1:
                    maze[i][j].up = maze[i - 1][j]
                    maze[i][j].down = maze[i + 1][j]
                    maze[i][j].left = maze[i][j - 1]
                #cells at the center
                else:
                    maze[i][j].up = maze[i - 1][j]
                    maze[i][j].down = maze[i + 1][j]
                    maze[i][j].left = maze[i][j - 1]
                    maze[i][j].right = maze[i][j + 1]

                if maze[i][j].value == 'S':
                    self.startNode = maze[i][j]
                if maze[i][j].value == 'E':
                    self.goalNode = maze[i][j]
        #clearing path and full path from previous calls
        self.path.clear()
        self.fullPath.clear()

    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        limit = 50
        # if a path is found, backtrack to construct the correct path
        if (self.RecursiveDLS(self.startNode, limit)):
            node = self.goalNode
            while node != self.startNode:
                self.path.append(node.id)
                node = node.previousNode
            self.path.append(self.startNode.id)
            self.path.reverse()
        else:
            self.fullPath.clear()
        return self.path, self.fullPath

    def RecursiveDLS(self, node, limit):
        self.fullPath.append(node.id)
        if node == self.goalNode:
            return True
        if limit <= 0:
            return False
        children = [node.up, node.down, node.left, node.right]
        for child in children:
            if child is not None and child.value != '#':
                if child.id not in self.fullPath:
                    # save parent info to use it while backtracking
                    child.previousNode = node
                    if (self.RecursiveDLS(child, limit - 1)):
                        return True
        return False

    def BDSpathConstruction(self, intersection):
        pathS= []
        pathE= []
        finalpath =[]
        intersection2=intersection
        #finalpath.append(self.startNode.id)
        
        while intersection != self.startNode:
            pathS.append(intersection.parentS.id)
            intersection=intersection.parentS

        intersection=intersection2
        while intersection != self.goalNode:
            pathE.append(intersection.parentE.id)
            intersection=intersection.parentE
            
        pathS.reverse()   
        finalpath =finalpath+ pathS
        finalpath.append(intersection2.id)
        finalpath=finalpath+pathE
        #finalpath.append(self.goalNode.id)
            
        return finalpath

    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        Qs = deque()
        Qe = deque()
        visitedS=[]
        visitedE= []
        
        Qs.append(self.startNode)
        visitedS.append(self.startNode.id)
        Qe.append(self.goalNode)
        visitedE.append(self.goalNode.id)
        while Qs and Qe:
            if Qs:
                current=Qs.popleft()
                if current.value=='#':
                    continue
                if current == self.goalNode or current.id in visitedE:
                    self.path= self.BDSpathConstruction(current)
                    E = visitedE
                    S= visitedS
                    setE= set(E)
                    setS= set(S)
                    differentnodes = list(setE - setS)
                    self.fullPath= S+ differentnodes
                    
                    #self.fullPath=list(set().union(visitedS,visitedE))
                    return self.path , self.fullPath
                neighbors=[current.up, current.down, current.left, current.right]
                for n in neighbors:
                    if n==None or n.value=='#':
                        continue
                    else:
                        if n.id not in visitedS:
                            visitedS.append(n.id)
                            n.parentS=current
                            Qs.append(n)
                    
            if Qe:
                current=Qe.popleft()
                if current.value=='#':
                    continue
                if current == self.startNode or current.id in visitedS:
                    self.path= self.BDSpathConstruction(current)
                    #visitedE.reverse()
                    E = visitedE
                    S= visitedS
                    setE= set(E)
                    setS= set(S)
                    differentnodes = list(setE - setS)
                    self.fullPath= S+ differentnodes
             
                    #self.fullPath=list(set().union(visitedS,visitedE))
                    return self.path , self.fullPath
                neighbors=[current.up, current.down, current.left, current.right]
                for n in neighbors:
                    if n==None or n.value=='#':
                        continue
                    else:
                        if n.id not in visitedE:
                            visitedE.append(n.id)
                            n.parentE=current
                            Qe.append(n)

        return self.path, self.fullPath


    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        open = [self.startNode]
        closed = []
        while len(open) > 0:
            currentNode = open.pop(0)
            self.fullPath.append(currentNode.id)
            # If goal is reached, then build Path
            if currentNode == self.goalNode:
                pathh = []
                self.totalCost=0
                while currentNode != self.startNode:
                    pathh.append(currentNode.id)
                    self.totalCost += currentNode.hOfN
                    currentNode = currentNode.previousNode
                pathh.append(self.startNode.id)
                self.totalCost +=self.startNode.hOfN
                self.path = pathh[::-1]
                return self.path, self.fullPath, self.totalCost

            # If we didn't reach the goalNode, then loop on the children
            neighbors = [currentNode.up, currentNode.down, currentNode.left, currentNode.right]
            for child in neighbors:
                if (child == None or child.value == '#'):
                    continue
                # checking if it's not found in open and closed lists, checking with id bec it's a unique value
                if child in open:
                    openContains = True
                else:
                    openContains = False

                if child in closed:
                    closedContains = True
                else:
                    closedContains = False
                if (openContains == False and closedContains == False):
                    open.append(child)
                    child.previousNode = currentNode
            if len(open) > 0:
                # sorting ascendingly based on heristic Value
                open.sort(key=lambda x: x.hOfN)
            closed.append(currentNode)
        # No solution found
        self.path = []
        self.fullPath = []
        self.totalCost = 0
        return self.path, self.fullPath, self.totalCost

def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BDS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                            , 100, 2, 15, 60, 100, 30, 2
                                                                                                            , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                            , 100, 100, 3, 15, 30, 100, 2
                                                                                                           , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.BFS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################

main()
