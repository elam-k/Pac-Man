import pygame
pygame.init()


class sprite:
   def __init__(self,x,y,speed,screen,colour,width,height):
       self.xPos = x
       self.yPos = y
       self.speed = speed
       self.screen = screen
       self.colour = colour
       self.rect = None
       self.width = width
       self.height = height
       self.targetPosition = None
       self.node = None # Stores the Current position, maybe rename to currentNode
       self.movingToTarget = False # True while sprite has not reached target node


   def drawCharacter(self): # Draws the sprite onto the screen
       self.screen.fill(self.colour, self.rect)


class pacman(sprite):

   def __init__(self,screen,x,y):
       super().__init__(x,y,5,screen,"yellow",15,15)
       self.activeStatus = True # Determines whether or not Pac-Man is alive
       #spawn pacman on random point in maze equal to 1
       self.rect = pygame.Rect(self.xPos,self.yPos,self.width,self.height) #20,20
       self.direction = 0  # Left = 1, Right = -1, Up = 2, Down = -2

   def updateDirection(self): # Updates Pac-Man's directions

       keys = pygame.key.get_pressed()

       if keys[pygame.K_LEFT]:
           self.direction = 1

       if keys[pygame.K_RIGHT]:
           self.direction = -1

       if keys[pygame.K_UP]:
           self.direction = 2

       if keys[pygame.K_DOWN]:
           self.direction = -2


class ghost(sprite):

   def __init__(self,screen,x,y):
       super().__init__(x,y,2,screen,"red",20,20)
       self.fruitConsumed = False
       self.rect = pygame.Rect(self.xPos,self.yPos,self.width,self.height)

   def updatePosition(self): # Updates the ghost's coordinates
       self.rect = pygame.Rect(self.xPos,self.yPos,self.width,self.height)

   def freezeGhost(self): # Freezes the ghost if a fruit has been consumed
       if self.fruitConsumed == True:
           self.speed = 0
