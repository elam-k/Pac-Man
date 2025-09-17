import heapq


class node:
   def __init__(self, g, h, y, x, previous):
       self.previousNode = previous
       self.g = g # Distance between current node and start node
       self.h = h # Value from heuristic function - manhattan distance


       #Stores x and y values of the node
       self.y = y
       self.x = x
   def __lt__(self,other): # Magic method - defines the operator < to compare the f values of this node and another node. returns true if this node's f value is smaller
       return self.g + self.h < other.g + other.h


   def checkIfEqual (self, other): # Will check if the coordinates of two nodes match
       return self.x == other.x and self.y == other.y
   


class aStar:
   def __init__(self,maze,start,target): # Takes the maze and the start and target (tuples containing coordinates) as parameters
       self.grid = maze
       self.rows = len(self.grid)
       self.columns = len(self.grid[0])
       self.unvisitedList = [] # This will be a heap priority queue
       self.visitedList = [] # stores the list of visited nodes/path ######################################################################## PREVIOUSLY A SET
       self.startNode = node(0,0,start[1],start[0],None) # Passes the x and y indexes of start node to the node class
       self.targetNode = node(0,0,target[1],target[0],None) # Passes x and y indexes of target node to the node class
       self.finished = False
       self.unvisitedList.append(self.startNode) # Adds start node to the unvisited list


   def manhattanDistance(self,node1,node2):
       return abs(node1.x - node2.x) + abs(node1.y - node2.y) # Calculates the manhattan distance (h value)


   def checkIfCoordinatesValid(self,x,y):
       if self.grid[x][y] != 0: # Checks if the cell is a wall
           if self.rows > x >= 0 and self.columns > y >= 0: # Checks if the indexes are within the bounds of the maze
               return True # Returns true if coordinates are valid (within bounds and not a wall)
       return False


   def search(self): # Finds the shortest path from the start position to the end position
       if not self.checkIfCoordinatesValid(self.startNode.x,self.startNode.y): # If the start node isn't valid then the search will automatically stop
           return None
       while not self.finished:
          
           currentNode = heapq.heappop(self.unvisitedList) # Will return the node in the unvisited list with the smallest f-score 
           xPos = currentNode.x
           yPos = currentNode.y

           if currentNode.checkIfEqual(self.targetNode): #If the target node has been found, the shortest path will be identified
               self.finished = True
               return self.returnShortestPath(currentNode) # Shortest path will be created from tracking parent nodes
           self.visitedList.append((xPos,yPos)) # Marks the current node as visited ############################################################### self.visitedList.add((xPos,yPos))
           neighbourCoordinates = [(xPos+1,yPos),(xPos-1,yPos),(xPos,yPos+1),(xPos,yPos-1)] # Stores the list of neighbours' indexes
           for i, j in neighbourCoordinates:
               if (i,j) not in self.visitedList and self.checkIfCoordinatesValid(i,j):
                 heapq.heappush(self.unvisitedList, node(currentNode.g + 1, self.manhattanDistance(node(0, 0, j, i, None), self.targetNode), j, i, currentNode))

           if len(self.unvisitedList) == 0: #If the unvisited list is empty, end the search
               self.finished = True
               return None

   def returnShortestPath(self,node): # Traces the target node back to the current position and returns an array containing the shortest path
       shortestPath = [] # Stores the list of paths
       parentNode = node
       startNodeFound = False
       while not startNodeFound: # Loops while the start node has not been reached
           shortestPath.append((parentNode.x,parentNode.y)) # Adds coordinates to the shortest path
           parentNode = parentNode.previousNode
           if parentNode == None: # Starting node has been found if it has no previous node
               startNodeFound = True
       shortestPath = shortestPath[::-1] # Reverses the array so that the order of the path is from the start to end (ghost to Pac-Man)
       shortestPath.pop(0) # Remove this and add back later - error to log (ghost did not move because start coordinates in shortest path is ghost's current position)
       return shortestPath