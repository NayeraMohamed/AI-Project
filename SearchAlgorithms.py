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

    def __init__(self, value):
        self.value = value
        #split string to construct 2d nodes array then loop and fill properties of each node


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

        #will need obj from class Node to access the maze array and set startNode and goalNode here
        
        '''self.startNode.id=mazeStr[0]
        self.startNode.hOfN=heristicValue[0]

        res=mazeStr.find('E')
        self.goalNode.id=mazeStr[res]
        self.startNode.hOfN=heristicValue[res];'''
        pass

    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        return self.path, self.fullPath

    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        return self.path, self.fullPath

    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        open = [self.startNode]
        closed = []
        self.fullPath.append(self.startNode)
        while len(open) > 0:
            #sorting ascendingly based on heristic Value
            open.sort(key=lamda, x:x.hOfN, reverse=False)
            currentNode=open.pop(0)
            #if goal is reached, then build Path
            if currentNode==self.goalNode:
                #Missing how to construct Fullpath?
                pathh=[]
                #fullPa=[]?
                while currentNode != self.startNode:
                    pathh.append(currentNode.id)
                    #fullPa.append()?
                    self.totalCost:=self.totalCost+currentNode.hOfN
                    currentNode=currentNode.previousNode
                self.path=pathh[::-1]
                return self.path, self.fullPath, self.totalCost

            #If we didn't reach the goalNode, then loop on the children
            neighbors = [currentNode.up, currentNode.down, currentNode.right, currentNode.left]
            for child in neighbors:
                #checking if it's not found in open and closed lists, checking with id bec it's a unique value
                #bool openContains =any(node for node in open if node.id == child.id) (another syntax if the other didn't work)
                #bool closedContains =any(node for node in closed if node.id == child.id) (another syntax)
                bool openContains = any(node.get('id') == child.id for node in open)
                bool closedContains = any(node.get('id') == child.id for node in closed)
                if(openContains==False AND closedContains==False):
                    open.append(child)
                    self.fullPath.append(child)
                    child.previousNode=currentNode
            closed.append(currentNode)
        return None


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
