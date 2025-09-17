# source = https://storm-coder-dojo.github.io/activities/python/pacman.html



import pygame
from pygame.locals import(QUIT)
import random



class pacmanMaze:

  def __init__(self,screen,maze):


      self.maze = maze #Stores the array representing the maze
      self.screen = screen
      self.columns = len(self.maze[0])
      self.rows = len(self.maze)
      self.mazeRects = [] # Where the rectangles used to draw the maze will be stored
      self.pelletsRects = [] # Stores the rectangles to draw the pellets onto the screen
      self.pelletsIndexes = [] # Stores the coordinates of the pellets and the corresponding node's indexes on the maze
      self.fruitPositions = []


  def drawMaze(self):
      #Converts the maze into an array of rectangles to be drawn
      xPos = 30
      yPos = 10
      for i in range(0,self.rows): # Iterates through each row in the maze
          xPos = 30
          yPos += 30 # Starts a new row upon every increase in the y coordinate
          for j in range(0,self.columns): # Iterates through each column in the maze
              if self.maze[i][j] == 0: # Draws a wall
                  self.mazeRects.append(pygame.rect.Rect(xPos,yPos,30,30))
              elif self.maze[i][j] == 1: # Draws a pellet
                  self.pelletsRects.append(pygame.rect.Rect(xPos+(30/2),yPos+(30/2),5,5))
                  if random.randint(1,48) == 20: # Each pellet has a 1/20 chance of being a fruit
                   self.fruitPositions.append((xPos+(30/2),yPos+(30/2)))
                  self.pelletsIndexes.append([xPos,yPos,i,j])
              xPos += 30


  def updateMaze(self):
      #Redraws the maze for every event loop
      for element in range(0,len(self.mazeRects)):
          pygame.draw.rect(self.screen,(17, 72, 210),self.mazeRects[element]) # Draws a wall
      for element in range(0,len(self.pelletsRects)):
          if self.pelletsRects[element] != None: # ‘None’ means the pellet has been eaten
           if (self.pelletsRects[element].left,self.pelletsRects[element].top) in self.fruitPositions: # Checks if it is a fruit
               pygame.draw.rect(self.screen,(38, 130, 69),self.pelletsRects[element]) # Draws a fruit
           else:
               pygame.draw.rect(self.screen,(255,255,153),self.pelletsRects[element]) # Draws a pellet