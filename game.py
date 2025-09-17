import pygame
from pygame.locals import(QUIT)
from sprite import *
from maze import *
from astar import *
import mysql.connector
from password import *
import random
import time

class singleplayer:
   def __init__(self,screen):
       self.screen = screen
       self.maze = pacmanMaze(self.screen,[ # 19 x 19 maze
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
   [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
   [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
   [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
   [0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
   [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
   [0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
   [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
   [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
   [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
   [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
   [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
   [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
   [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
   [0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
   [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
   [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
  
       self.ghost = None # Stores ghost object
       self.score = 0
       self.lives = 3
       self.scoreFont = pygame.font.SysFont("arialunicode",30)
       self.scoreImg = None
       self.livesFont = pygame.font.SysFont("arialunicode",30)
       self.livesImg = None
       self.ghostAStar = None # Will hold the object of the a star class
       self.ghostPath = None # Will hold the shortest path from the ghost to Pac-Man
       self.pacman = None # Stores pacman object
       self.gameOverFont = pygame.font.SysFont("arialunicode",30)
       self.gameOverImg = None
       self.startTime = None # Stores the starting time of the game
       self.totalTime = None # Stores the total time taken for the round
       self.username = None
       self.mycursor = None
       self.db = None
       self.statisticsSaved = False
       self.connectToDatabase()
  

   def connectToDatabase(self):
    self.db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = SQLdatabasepassword,
        database = "PacManDB"
    )
    self.mycursor = self.db.cursor()

   def startGame(self): # Resets the statistics for a new game
       self.startTime = time.time() # Starts timer for the game
       self.score = 0
       self.lives = 3
       self.statisticsSaved = False
       self.maze.drawMaze()
       self.setPacmanNode()
       self.setGhostNode()

   def setPacmanNode(self):
       n = random.randint(0, len(self.maze.pelletsRects)) # Randomises Pac-man's position on the maze
       x,y = self.maze.pelletsIndexes[n][0],self.maze.pelletsIndexes[n][1] # Assigns position to pacman
       self.pacman = pacman(self.screen,x+7.5,y+7.5)
       self.pacman.node = n #Stores the index storing the coordinates of pacman on the maze
       self.initialisePacmanPosition(self.pacman.node)

   def setGhostNode(self):
       n = random.randint(0, len(self.maze.pelletsRects)) # Randomises ghost's position on the maze
       x,y = self.maze.pelletsIndexes[n][0],self.maze.pelletsIndexes[n][1] # Assigns position to ghost
       self.ghost = ghost(self.screen,x+7.5,y+7.5)
       self.ghost.node = n #Stores the index storing the coordinates of the ghost on the maze
       self.initialiseGhostPosition(self.ghost.node)

   def initialiseGhostPosition(self,n): # Assigns x and y coordinates of the node to the ghost's rect
       x,y = self.maze.pelletsIndexes[n][0],self.maze.pelletsIndexes[n][1] 
       self.ghost.xPos,self.ghost.yPos = x,y
       self.ghost.rect = pygame.Rect(x+7.5,y+7.5,self.ghost.width,self.ghost.height) 
       self.updateGhostStartAndTargetNodes()

   def initialisePacmanPosition(self,n): # Assigns x and y coordinates of the node to pac-man's rect
       x,y = self.maze.pelletsIndexes[n][0],self.maze.pelletsIndexes[n][1]
       self.pacman.xPos,self.pacman.yPos = x,y
       self.pacman.rect = pygame.Rect(x+7.5,y+7.5,self.pacman.width,self.pacman.height)

   def updatePacManDirection(self):  # Updates Pac-Man's directions
       # Left = 1, Right = -1, Up = 2, Down = -2
       self.pacman.updateDirection()
       i,j = self.maze.pelletsIndexes[self.pacman.node][2],self.maze.pelletsIndexes[self.pacman.node][3]
       if self.pacman.movingToTarget:
        self.movePacman(self.pacman.direction,self.pacman.targetPosition)

       if self.pacman.direction == 1: #Moves to the left
        if self.maze.maze[i][j-1] == 1: # Checks if the move is valid (i.e there is an empty spot and not a wall). Won't need to check if out of bounds as Pac-Man cannot reach the 'bounds', or walls
            for n in range (0,len(self.maze.pelletsIndexes)):
                if self.maze.pelletsIndexes[n][2] == i and self.maze.pelletsIndexes[n][3] == j-1: # Gets the index of the new coordinates to store in pacman node
                     self.updatePacManTargetPosition(n)

       elif self.pacman.direction == -1: #Moves to the right
        if self.maze.maze[i][j+1] == 1:
            for n in range (0,len(self.maze.pelletsIndexes)):
                if self.maze.pelletsIndexes[n][2] == i and self.maze.pelletsIndexes[n][3] == j+1: # Gets the index of the new coordinates to store in pacman node
                     self.updatePacManTargetPosition(n)

       elif self.pacman.direction == 2: #Moves up
        if self.maze.maze[i-1][j] == 1:
            for n in range (0,len(self.maze.pelletsIndexes)):
                if self.maze.pelletsIndexes[n][2] == i-1 and self.maze.pelletsIndexes[n][3] == j: # Gets the index of the new coordinates to store in pacman node
                     self.updatePacManTargetPosition(n)

       elif self.pacman.direction == -2: #Moves down
        if self.maze.maze[i+1][j] == 1:
            for n in range (0,len(self.maze.pelletsIndexes)):
                if self.maze.pelletsIndexes[n][2] == i+1 and self.maze.pelletsIndexes[n][3] == j: # Gets the index of the new coordinates to store in pacman node
                     self.updatePacManTargetPosition(n)

   def updatePacManTargetPosition(self,n):
       self.pacman.targetPosition = self.maze.pelletsIndexes[n][0],self.maze.pelletsIndexes[n][1]
       self.pacman.node = n # Updates the node of Pac-Man
       self.pacman.movingToTarget = True # Indicates that Pac-Man is currently moving to its target position

   def movePacman(self,direction,targetposition):
    # Left = 1, Right = -1, Up = 2, Down = -2
    if self.pacman.xPos != targetposition[0] or self.pacman.yPos != targetposition[1]: # Checks whether Pac-Man has reached its target position
        if abs(direction) == 1: # Pacman to move left or right
            if abs(targetposition[0] - self.pacman.xPos) <= self.pacman.speed:
                self.pacman.xPos += (-direction*(abs(targetposition[0] - self.pacman.xPos))) #Ensures that Pac-Man does not overshoot the target
            else:
                self.pacman.xPos += (-direction*self.pacman.speed) # Will update pacman's x position. use of minus sign will ensure that x position is correctly updated

        elif abs(direction) == 2: # Pacman to move up or down
            if abs(targetposition[1] - self.pacman.yPos) <= self.pacman.speed:
                self.pacman.yPos += (-direction/2*(abs(targetposition[1] - self.pacman.yPos))) #Ensures that Pac-Man does not overshoot the target position
            else:
                self.pacman.yPos += (-direction/2*self.pacman.speed) # Will update pacman's y position. use of minus sign will ensure that y position is correctly updated

        self.pacman.rect = pygame.Rect(self.pacman.xPos+7.5,self.pacman.yPos+7.5,self.pacman.width,self.pacman.height) #Moves Pac-Man to the new node. Called upon every event loop to refresh Pac-Man's position
    else:
        self.pacman.movingToTarget = False # Indicates that Pac-Man has reached its target
        self.pacman.direction == 0 # Stops Pac-Man from moving once they have reached the target position
        self.pacman.targetPosition = None # Will ensure that the code does not loop back here once target position has been reached


   def updateGhostStartAndTargetNodes(self): # Continuously updates the a star algorithm with the ghost and pac-man's new coordinates as the game progresses
       self.ghostAStar = aStar(self.maze.maze,(self.maze.pelletsIndexes[self.ghost.node][2],self.maze.pelletsIndexes[self.ghost.node][3]),(self.maze.pelletsIndexes[self.pacman.node][2],self.maze.pelletsIndexes[self.pacman.node][3]))

   def updateGhostPath(self): # Updates the ghost's path to pac-man and changes the ghost's target position accordingly
       self.ghostPath = self.ghostAStar.search()
       if self.ghostPath and self.ghost.movingToTarget == False:
           targetPositionIndexes = self.ghostPath.pop(0)
           self.updateGhostTargetPosition(targetPositionIndexes)
       else:
           self.updateGhostTargetPosition()


   def updateGhostTargetPosition(self,targetPositionIndexes=None): # Updates the ghost's target position if it isn't moving
       if self.ghost.movingToTarget == True:
           self.moveGhost(self.ghost.targetPosition) # Ghost continues moving towards target
       elif targetPositionIndexes != None:
           for n in range (0,len(self.maze.pelletsIndexes)):
            if self.maze.pelletsIndexes[n][2] == targetPositionIndexes[0] and self.maze.pelletsIndexes[n][3] == targetPositionIndexes[1]: # Matches up the ghost's indexes with the pellet's indexes
               self.ghost.targetPosition = self.maze.pelletsIndexes[n][0],self.maze.pelletsIndexes[n][1] # Stores the coordinates of the ghost's target position
               self.ghost.node = n # Updates the node of the ghost
               self.ghost.movingToTarget = True # Indicates that the ghost is currently moving to its target position - in this case, pac-man's position
               
   def moveGhost(self,targetPosition): # Moves the ghost to its target position
       if self.ghost.xPos != targetPosition[0]: # Checks if ghost has reached its x position
            if self.ghost.xPos > targetPosition[0]: # Checks which direction the ghost will need to move (left or right)
                direction = -1
            else:
                direction = 1
            if abs(targetPosition[0] - self.ghost.xPos) <= self.ghost.speed:
                self.ghost.xPos += direction*abs(targetPosition[0] - self.ghost.xPos) # Updates x coordinate of ghost, slowing down if the ghost is close to its target
            else:
                self.ghost.xPos += direction*self.ghost.speed  # Updates x coordinate of ghost with its speed

 
       elif self.ghost.yPos != targetPosition[1]:
            if self.ghost.yPos > targetPosition[1]: # Checks which direction the ghost will need to move (up or down)
                direction = -1
            else:
                direction = 1

            if abs(targetPosition[1] - self.ghost.yPos) <= self.ghost.speed:
                self.ghost.yPos += direction*abs(targetPosition[1] - self.ghost.yPos) # Updates y coordinate of ghost, slowing down if the ghost is close to its target
            else:
                self.ghost.yPos += direction*self.ghost.speed  # Updates y coordinate of ghost with its speed

       else:
           self.ghost.movingToTarget = False # Indicates that the ghost has reached its target
           self.ghost.targetPosition = None
       self.ghost.rect = pygame.Rect(self.ghost.xPos+7.5,self.ghost.yPos+7.5,self.ghost.width,self.ghost.height)
       
   def updateDisplay(self):
       self.screen.fill((0,0,0))
       self.scoreImg = self.scoreFont.render(("Score: "+str(self.score)),True,"yellow")
       self.livesImg = self.livesFont.render(("Lives: "+str(self.lives)), True, "yellow")
       self.screen.blit(self.scoreImg,(200,690))
       self.screen.blit(self.livesImg,(400,690))
       self.maze.updateMaze()
       self.drawCharacters()
       self.updatePacManDirection() 
       
       self.consumePellet()
       self.ghost.freezeGhost()
    
       self.updateLives()
       self.checkIfGameOver()

       self.updateGhostStartAndTargetNodes()
       self.updateGhostPath()


   def consumePellet(self): # Removes a pellet from the maze upon collision. Adds points to the total score
       for element in range (0,len(self.maze.pelletsRects)):
           if self.maze.pelletsRects[element] != None: # Checks if there is a pellet located at that given position
               if self.pacman.rect.colliderect(self.maze.pelletsRects[element]): #Checks for a collision with pellet
                   if (self.maze.pelletsRects[element].left,self.maze.pelletsRects[element].top) in self.maze.fruitPositions: #Checks if pac-man has collided with a fruit
                       self.updatePoints(5) # 5 points for a fruit
                       self.ghost.fruitConsumed = True
                   else:
                       self.updatePoints(random.randint(1,3)) # 1-3 points for pellets
                   self.maze.pelletsRects[element] = None
    
   def updatePoints(self,score):
       #Update the points and draw the points on screen
       self.score += score
              
   def collisionCheck(self): # Checks whether the ghost and Pac-Man have collided
       if self.pacman.xPos < self.ghost.xPos + self.pacman.width and self.pacman.xPos + self.ghost.width > self.ghost.xPos and self.pacman.yPos < self.pacman.height + self.ghost.yPos and self.ghost.yPos < self.ghost.height + self.pacman.yPos:
           return True
       return False
   
   def updateLives(self): # Takes a life from Pac-Man and resets the sprite’s positions if they come into collision
       if self.collisionCheck():
           self.lives -= 1
           self.restartCharacters() # Add to key algorithms document

   def restartCharacters(self): # Resets the positions of Pac-Man and the ghost
        self.setPacmanNode()
        self.setGhostNode()

   def drawCharacters(self): # Draws the characters onto the screen - called continuously to update their positions on the maze
       self.pacman.drawCharacter()
       self.ghost.drawCharacter()

   def checkIfGameOver(self): # Checks if pac-man has won/lost and returns to the main menu if so
       if self.lives == 0: 
           self.endGame(False)
           return "mainmenu"
       else:
           gameWon = True
           for element in range(0,len(self.maze.pelletsRects)): # Checks if all pellets have been eaten
               if self.maze.pelletsRects[element] != None:
                   gameWon = False # Game continues if not all pellets have been eaten
           if gameWon:
               self.endGame(True)
               return "mainmenu"
           else:
               return "singleplayer"
   
   def endGame(self,gameWon): # Carries out actions at the end of a game
       self.pacman.activeStatus = False
       self.endGameMessage()
       self.totalTime = time.time() - self.startTime
       pygame.time.wait(3000)  # Game over message will display for 3 seconds
       if self.statisticsSaved == False:
           self.updateUserStatistics(gameWon)
           self.statisticsSaved = True
       
   def updateUserStatistics(self, gameWon): # Updates the user's statistics at the end of a game
       # Statistics to update regardless of winning or lossing
       self.mycursor.execute("UPDATE Scores INNER JOIN Users on Scores.UserID = Users.UserID SET TotalGamesPlayed = TotalGamesPlayed+1, TotalPoints = TotalPoints+%s, TimePlayed = TimePlayed + %s WHERE Users.Username = %s",(self.score,self.totalTime,self.username,))
       if gameWon: # Increase the win count if the user has won
           self.mycursor.execute("UPDATE Scores INNER JOIN Users on Scores.UserID = Users.UserID SET Wins = Wins+1, AverageScore = (AverageScore*(TotalGamesPlayed-1)+%s)/TotalGamesPlayed, AverageRoundLength = (AverageRoundLength*(TotalGamesPlayed-1)+%s)/TotalGamesPlayed WHERE Users.Username = %s",(self.score, self.totalTime, self.username))
       else: # Otherwise, increase the loss count
           self.mycursor.execute("UPDATE Scores INNER JOIN Users on Scores.UserID = Users.UserID SET Losses = Losses+1, AverageScore = (AverageScore*(TotalGamesPlayed-1)+%s)/TotalGamesPlayed, AverageRoundLength = (AverageRoundLength*(TotalGamesPlayed-1)+%s)/TotalGamesPlayed WHERE Users.Username = %s",(self.score, self.totalTime, self.username))
       self.db.commit()

   def endGameMessage(self): # Displays "Game over" to the player once it has ended
       self.gameOverImg = self.gameOverFont.render("Game over",True,"yellow")
       self.screen.blit(self.gameOverImg,(300,720))