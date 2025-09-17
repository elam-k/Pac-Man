import pygame
import mysql.connector
from GUI import *
from password import *


class leaderboard:
    def __init__(self, screen):
        self.screen = screen
        self.backButton = button("red", 270, 50, 200, 50, 22,self.screen,'Back')
        self.topTenPlayersFont = pygame.font.SysFont("arialunicode",50)
        self.topTenPlayersImg = []
        self.db = None
        self.mycursor = None
        self.connectToDatabase()

    def connectToDatabase(self): # Connects to database to fetch entries for the leaderboard
     self.db = mysql.connector.connect(
         host = "localhost",
         user = "root",
         password = SQLdatabasepassword,
         database = "PacManDB"
     )
     self.mycursor = self.db.cursor()

    def checkIfButtonPressed(self): # Checks if the back button has been pressed
       if self.backButton.isClicked():
          return "mainmenu"
       else:
          return "leaderboard"

    def drawDisplay(self): # Draws the background and buttons
        self.screen.fill((0,0,0))
        self.backButton.draw(self.screen)

        self.findTopEntries()

    def findTopEntries(self): # Gets the top ten users with the most wins
        
        self.connectToDatabase()

        entries = []
        self.mycursor.execute("SELECT Users.Username, Scores.Wins FROM Users INNER JOIN Scores on Scores.UserID = Users.UserID ORDER BY Scores.Wins DESC LIMIT 10;")
        for i in self.mycursor:
           entries.append(i)
        self.mycursor.fetchall()
        self.mycursor.close()

        self.createEntriesDisplay(entries)


    def createEntriesDisplay(self,entries): # Converts the entries from the database to text to be displayed onto the screen
        self.topTenPlayersImg = []

        for i in range(0,len(entries)):
           self.topTenPlayersImg.append(self.topTenPlayersFont.render(( str(i+1) + " Username: " + str(entries[i][0]) + " Wins: " + str(entries[i][1]) ),True,"Yellow"))
        self.displayEntries()
        

    def displayEntries(self): # Displays the entries onto the screen in descending order
       y = 125
       for i in self.topTenPlayersImg:
          self.screen.blit(i,(65,y))     
          y = y+50
           
        
