import pygame
from GUI import *
from pygame.locals import(QUIT)
pygame.init()
from account_system import *
from leaderboard import *


SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #screen display
CLOCK = pygame.time.Clock()


def main(screen): # Main script controlling the display and events
   currentDisplay = "login" # This will be altered later as buttons are pressed and the user is taken to different pages
   operating = True

   # creates objects of classes for different pages
   loginSystem = login(screen)
   signupSystem = signup(screen)
   mainMenuSystem = mainMenu(screen)
   singleplayerGame = singleplayer(screen) # Consider moving or creating a start method (better)
   forgotPasswordSystem = forgotPass(screen)
   gameLeaderboard = leaderboard(screen)

   while operating:
       for event in pygame.event.get():
           if event.type == QUIT:
               operating = False
               pygame.quit() #prevents infinite loop
           if currentDisplay == "login":
               loginSystem.handleInputs(event)
           elif currentDisplay == "signup":
               signupSystem.handleInputs(event)
           elif currentDisplay == "mainmenu":
               pass
           elif currentDisplay == "forgotpass":
               forgotPasswordSystem.handleInputs(event)
              
       if currentDisplay == "login":
           loginSystem.drawInputs()
       elif currentDisplay == "signup":
           signupSystem.drawInputs()
       elif currentDisplay == "forgotpass":
           forgotPasswordSystem.drawInputs()
       elif currentDisplay == "mainmenu":
           pass

       CLOCK.tick(30)
       pygame.display.flip()
      
       if currentDisplay == "login":
           loginSystem.drawDisplay()
           currentDisplay = loginSystem.checkIfButtonPressed()

       elif currentDisplay == "signup":
           signupSystem.drawDisplay()
           currentDisplay = signupSystem.checkIfButtonPressed()

       elif currentDisplay == "mainmenu":
           mainMenuSystem.drawDisplay()
           currentDisplay = mainMenuSystem.checkIfButtonPressed()
           if currentDisplay == "singleplayer": # Starts the game, resets the statistics for the new game
               singleplayerGame.startGame()
               # Stores username to allow the game to update user's statistics at the end of the round
               if loginSystem.username != None:
                   singleplayerGame.username = loginSystem.username
               elif signupSystem.username != None:
                   singleplayerGame.username = signupSystem.username
               else:
                   singleplayerGame.username = forgotPasswordSystem.username

       elif currentDisplay == "forgotpass":
           forgotPasswordSystem.drawDisplay()
           currentDisplay = forgotPasswordSystem.checkIfButtonPressed()

       elif currentDisplay == "singleplayer":
           singleplayerGame.drawCharacters()
           currentDisplay = singleplayerGame.checkIfGameOver()

       if currentDisplay == "singleplayer":
           singleplayerGame.updateDisplay()

       elif currentDisplay == "leaderboard":
           gameLeaderboard.drawDisplay()
           currentDisplay = gameLeaderboard.checkIfButtonPressed()

if __name__ == "__main__":
   pacman = main(SCREEN)