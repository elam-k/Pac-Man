import pygame
from pygame.locals import (
   K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT
)
 
class button():
   def __init__(self, colour, x,y,width,height, font,screen,text=''):
       self.colour = colour
       self.x = x
       self.y = y
       self.width = width
       self.height = height
       self.text = text
       self.font = font
       self.screen = screen
 
   def draw(self,window):
      
       pygame.draw.rect(window, self.colour, (self.x,self.y,self.width,self.height),0)
       if self.text != '': #font and position of button
           font = pygame.font.SysFont('arialunicode', self.font)
           text = font.render(self.text, 1, (0,0,0))
           self.screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
 
   def isClicked(self):
       x_coord, y_coord = pygame.mouse.get_pos()
       if pygame.mouse.get_pressed()[0]:
           if x_coord >= self.x and x_coord <= self.x + self.width and y_coord >= self.y and y_coord <= self.y + self.height:
               return True
 
class InputBox():
  
 
   def __init__(self, x, y):
 
       self.font = pygame.font.Font(None, 32)
       self.inputBox = pygame.Rect(x, y, 140, 32)
       self.colour = pygame.Color('lightskyblue3')
       self.text = ''
       self.text_surface = self.font.render(self.text, True, (0,0,0))
       self.active = False
 
   def handleEvent(self, event):
 
       if event.type == pygame.MOUSEBUTTONDOWN:
           self.active = self.inputBox.collidepoint(event.pos) #checks if given that mouse is clicked,
                                                               #is the mouse inside the box
 
       if event.type == pygame.KEYDOWN:
           if self.active:
               if event.key == pygame.K_RETURN: #replace this part with method to check if input is valid
                   self.text = ''
               elif event.key == pygame.K_BACKSPACE:
                   self.text = self.text[:-1]
               else:
                   self.text += event.unicode
 
 
   def draw(self, screen): #Sets the font of the text and dimensions of the input box before drawing it on the pygame window
       txtSurface = self.font.render(self.text, True, self.colour)
       width = max(200, txtSurface.get_width()+10)
       self.inputBox.w = width
       screen.blit(txtSurface, (self.inputBox.x+5, self.inputBox.y+5))
       pygame.draw.rect(screen, self.colour, self.inputBox, 2)
       self.color = (0, 128, 255)
 
   def getInputText(self):
       return self.text
