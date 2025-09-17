import pygame
from GUI import *
from pygame.locals import(QUIT)
from sprite import *
from maze import *
from password import *
from game import *
import re
import random
import mysql.connector
import bcrypt
from twilio.rest import Client


pygame.init()
 
class accountSystem:
   def __init__(self,screen):
       self.screen = screen
       self.titleFont = pygame.font.SysFont("arialunicode",50)
       self.titleImg = None
       self.mycursor = None
       self.db = None
       self.connectToDatabase()
       self.accountSid = 'AC1db93e46c5d5343d965e9809e0d5c3d4'
       self.authToken = '40e31e0bdbd2db3f2c34abf330d87126'
       self.twilioPhoneNumber = '+17246232868'
       self.client = Client(self.accountSid,self.authToken)
       self.username = None
       self.errorMessageSendCodeFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessageSendCodeImg = self.errorMessageSendCodeFont.render("Code failed to send", True, "Red")
    #   self.nextPage = None


   def connectToDatabase(self): # Connects the program to the database
    self.db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = SQLdatabasepassword,
        database = "PacManDB"
    )
    self.mycursor = self.db.cursor()

   def drawDisplay(self): # Draws the screen to be displayed to the user
       self.screen.fill((0,0,0))
       self.titleImg = self.titleFont.render("Pac-Man",True,"Red")
 
   def handleInputs(self):
       pass
 
   def checkIfButtonPressed(self):
       pass
 
   def drawInputs(self):
       pass
 
class oneTimePassword(accountSystem):

    def __init__(self,screen,currentpage,status):
        super().__init__(screen)
        self.submitButton = button("red", 275, 440, 200, 100, 22,self.screen,'Submit')
        self.codeInput = InputBox(275,360)
        self.codeFont = pygame.font.SysFont("arialunicode",30)
        self.codeImg = None
        self.errorMessageCodeFont = pygame.font.SysFont("arialunicode",20)
        self.errorMessageCodeImg = self.errorMessageCodeFont.render("Incorrect code entered", True, "Red")
        self.verificationCode = None
        self.currentPage = currentpage
        self.nextPage = status 

    def drawDisplay(self): # Draws the screen to be displayed to the user
        self.screen.fill((0,0,0))
        self.titleImg = self.titleFont.render("Pac-Man",True,"Red")
        self.codeImg = self.codeFont.render("Code",True,"Red")
        self.screen.blit(self.titleImg,(275,135))
        self.screen.blit(self.codeImg,(305,310))
        self.submitButton.draw(self.screen)
    
    def handleInputs(self,event): # Processes the input text entered into the input boxes
        self.codeInput.handleEvent(event)

    def drawInputs(self): # Draws the input boxes onto the screen alongside the text
        self.codeInput.draw(self.screen)

    def checkIfCodeIsValid(self): # Checks if the user has inputted the correct code
        userCodeInput = self.codeInput.getInputText()
        if userCodeInput == self.verificationCode:
           return True
        self.screen.blit(self.errorMessageCodeImg,(175,270))
        return False
   

    def checkIfButtonPressed(self): # Checks if a button has been pressed, taking appropriate action if so
        if self.submitButton.isClicked():
            if self.checkIfCodeIsValid():
               return self.nextPage # Will either return the user to the main menu or the password resetting page, depending on the previous page accessed by the user
            else:
               return self.currentPage
        else:
            return self.currentPage

    def sendCode(self,username):
        # Generate a random 6 digit number and convert it to a string to include in the message
        code = random.randint(100000,999999)
        self.verificationCode = str(code) 
        self.mycursor.execute("SELECT PhoneNumber FROM Users WHERE Username=%s",(username,))
        userPhoneNumber = self.mycursor.fetchone()[0]
        try:
            # Sends the code to the user's phone number
            message = self.client.messages.create(
                body = "Enter the following code into the window - " + self.verificationCode,
                from_= self.twilioPhoneNumber,
                to = userPhoneNumber
            )
            return True
        except:
            # Prevents the system from crashing if the api fails to send the message
            self.screen.blit(self.errorMessageSendCodeImg,(175,270)) 
            return False
 
class login(accountSystem): 
 
   def __init__(self,screen):
       super().__init__(screen)
       self.usernameInput = InputBox(275, 250)
       self.passwordInput = InputBox(275, 350)
       self.signUpButton = button("red", 275, 590, 200, 100, 40,self.screen,'Sign Up')
       self.loginButton = button("red",275,460,200,100,40,self.screen,'Login')
       self.forgotPasswordButton = button("red",275,405,200,35,20,self.screen,'Forgot Password?')
       self.usernameFont = self.passwordFont = pygame.font.SysFont("arialunicode",30)
       self.usernameImg = self.passwordImg = None
       self.errorMessageUsernameFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessageUsernameImg = self.errorMessageUsernameFont.render("Username does not exist", True, "Red")
       self.errorMessagePasswordFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessagePasswordImg = self.errorMessagePasswordFont.render("Username or password is incorrect", True,"Red")
       self.errorMessageSendCodeFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessageSendCodeImg = self.errorMessageSendCodeFont.render("Code failed to send", True, "Red")
       self.oneTimePasswordSystem = oneTimePassword(screen,"login","mainmenu")
       self.display = "login"
   
   def drawDisplay(self):
       # Draws the buttons, text and input boxes onto the screen
       if self.display == "login":
        self.screen.fill((0,0,0))
        self.usernameImg, self.passwordImg = self.usernameFont.render("Username",True,"Red"),self.passwordFont.render("Password",True,"Red")
        self.screen.blit(self.usernameImg,(175,250))
        self.screen.blit(self.passwordImg,(175,350))
        self.titleImg = self.titleFont.render("Pac-Man",True,"Red")
        self.screen.blit(self.titleImg,(275,135))
        self.signUpButton.draw(self.screen)
        self.loginButton.draw(self.screen)
        self.forgotPasswordButton.draw(self.screen)
       elif self.display == "otp":
        self.oneTimePasswordSystem.drawDisplay()
 
   def handleInputs(self,event):
       if self.display == "login":
        self.usernameInput.handleEvent(event)
        self.passwordInput.handleEvent(event)
       elif self.display == "otp":
        self.oneTimePasswordSystem.handleInputs(event)

 
   def checkIfUsernameValid(self,username): # Checks if the username exists in the database
    self.mycursor.execute("SELECT COUNT(*) FROM Users WHERE Username=%s",(username,)) 
    count = self.mycursor.fetchone()[0]
    if count == 1: # There will be an entry in the database containing the provided username if the username is registered
        self.mycursor.fetchall()
        return True
    else:
        self.mycursor.fetchall()
        return False

 
   def checkIfPasswordValid(self,username,password): # Checks if the password is correct
    self.mycursor.execute("SELECT Password FROM USERS WHERE Username=%s",(username,))
    correctPass = self.mycursor.fetchone()[0]
    correctPassEncoded = correctPass.encode('utf-8')
    inputPassword = password.encode('utf-8')
    passwordValid = bcrypt.checkpw(inputPassword,correctPassEncoded) # Compares hashed password in DB with user inputted password
    if passwordValid:
        self.username = username # Saves the username for usage in managing account details throughout the program's runtime
        return True
    else:
        return False
 
   def checkIfButtonPressed(self):
    if self.display == "login":
       usernameInputText = self.usernameInput.getInputText()
       passwordInputText = self.passwordInput.getInputText()
       # Checks which button has been pressed and directs the user to the corresponding page
       if self.signUpButton.isClicked():
           return "signup"
       elif self.loginButton.isClicked():
           if self.checkIfUsernameValid(usernameInputText): #Checks if user exists in DB
               if self.checkIfPasswordValid(usernameInputText,passwordInputText): #Checks if the entered password is correct  
                   if self.oneTimePasswordSystem.sendCode(usernameInputText): # Delivers the random message to the phone number associated with the username used for login
                       self.display = "otp" # switches the display to the one time password screen if the code has been successfully sent
                   else:
                       self.screen.blit(self.errorMessageSendCodeImg, (175,300)) # Otherwise the user will be displayed a message indicating failure to send the message
               else:
                #Display Password error message if the entered password is incorrect
                   self.screen.blit(self.errorMessagePasswordImg,(175,300))
           else:
               self.screen.blit(self.errorMessageUsernameImg,(175,300))
           return "login"
       elif self.forgotPasswordButton.isClicked():
           return "forgotpass"
       else:
           return "login"
    elif self.display == "otp":
        return self.oneTimePasswordSystem.checkIfButtonPressed()
 
   def drawInputs(self):
    if self.display == "login":
       self.usernameInput.draw(self.screen)
       self.passwordInput.draw(self.screen)
    elif self.display == "otp":
       self.oneTimePasswordSystem.drawInputs()


 
class signup(accountSystem):
 
   def __init__(self,screen):
       super().__init__(screen)
       self.create_account = button("red", 275, 440, 200, 100, 22,self.screen,'Create account')
       self.usernameSignupInput = InputBox(275,220)
       self.passwordSignupInput = InputBox(275,290)
       self.PhoneNumber_signup = InputBox(275,360)
       self.usernameFont = self.passwordFont = self.PhoneNumber_font = pygame.font.SysFont("arialunicode",30)
       self.usernameImg = self.passwordImg = self.PhoneNumber_img = None
       self.errorMessageUsernameFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessageUsernameImg = self.errorMessageUsernameFont.render("Username must be at least 6 characters and unused", True, "Red")
       self.errorMessagePasswordFont = pygame.font.SysFont("arialunicode",15)
       self.errorMessagePasswordImg = self.errorMessagePasswordFont.render("Password must be at least 8 characters, contain a capital letter, lowercase letter, number and symbol", True,"Red")
       self.errorMessagePhoneNumberFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessagePhoneNumberImg = self.errorMessagePhoneNumberFont.render("Phone number must be a valid UK number and unused", True, "Red")
      
 
   def drawDisplay(self):
       self.screen.fill((0,0,0))
       self.titleImg = self.titleFont.render("Pac-Man",True,"Red")
       self.usernameImg, self.passwordImg,self.PhoneNumber_img = self.usernameFont.render("Username",True,"Red"),self.passwordFont.render("Password",True,"Red"),self.PhoneNumber_font.render("Phone Number",True,"Red")
       self.screen.blit(self.usernameImg,(175,220))
       self.screen.blit(self.passwordImg,(175,290))
       self.screen.blit(self.PhoneNumber_img,(135,360))
       self.screen.blit(self.titleImg,(275,135))
       self.create_account.draw(self.screen)
 
   def handleInputs(self,event):
       self.usernameSignupInput.handleEvent(event)
       self.passwordSignupInput.handleEvent(event)
       self.PhoneNumber_signup.handleEvent(event)
 
   def drawInputs(self):
       self.usernameSignupInput.draw(self.screen)
       self.passwordSignupInput.draw(self.screen)
       self.PhoneNumber_signup.draw(self.screen)

 
   def checkIfButtonPressed(self):
       # Checks if create account button has been pressed and sends the user to the main menu if the inputs are valid
       usernameInputText = self.usernameSignupInput.getInputText()
       passwordInputText = self.passwordSignupInput.getInputText()
       phonenumberInputText = self.PhoneNumber_signup.getInputText()
       if self.create_account.isClicked():
           # Checks if all of the inputs are valid
           if self.checkIfUsernameValid(usernameInputText) and self.checkIfPasswordValid(passwordInputText) and self.checkIfPhoneNumberValid(phonenumberInputText):
               self.addDetailsToDatabase(usernameInputText,passwordInputText,phonenumberInputText) #Once the user has provided valid input in all three fields, the details are added to the database
               return "mainmenu"
           else:
               self.displayErrorMessage(self.checkIfUsernameValid(usernameInputText),self.checkIfPasswordValid(passwordInputText),self.checkIfPhoneNumberValid(phonenumberInputText))
               return "signup"
       else:
           return "signup"
 
   def displayErrorMessage(self,usernameValid,passwordValid,phonenumberValid):
       if not usernameValid:
           self.screen.blit(self.errorMessageUsernameImg,(175,270))
       if not passwordValid:
           self.screen.blit(self.errorMessagePasswordImg,(160,320))
       if not phonenumberValid:
           self.screen.blit(self.errorMessagePhoneNumberImg,(175,390))

   def checkIfPhoneNumberValid(self,phonenumber):
       # Checks if a valid UK phone number has been inputted
       phonenumberValid = re.search("^((\+44))?\d{4}?\d{6}$",phonenumber)
       # Returns true if the phone matches the regular expression, otherwise it displays an error message and returns false
       if phonenumberValid:
        self.mycursor.execute("SELECT COUNT(*) FROM Users WHERE PhoneNumber=%s",(phonenumber,))
        count = self.mycursor.fetchone()[0] # Gets the number of rows where the phone number matches the user-inputted phone number
        if count == 1: # Checks if the phone number exists in the database. Returns false if this is the case
            self.mycursor.fetchall()
            return False
        self.mycursor.fetchall()
        return True
       else:
           return False
 
   def checkIfPasswordValid(self,password):
       # Checks if password meets complexity requirements and displays error message if not
       passwordValid = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[?!@#%$]).{8,}$",password)
       if passwordValid:
           return True
       else:
           return False
 
   def checkIfUsernameValid(self,username):
       # Checks if the username is at least 6 characters and only contains letters & numbers
       usernameValid = re.search("^[A-Za-z0-9]*$",username)
       if len(username) >=6 and usernameValid:
        self.mycursor.execute("SELECT COUNT(*) FROM Users WHERE Username=%s",(username,))
        count = self.mycursor.fetchone()[0] # Gets the number of rows where the username matches the user-inputted username
        if count > 0: # Checks if the username exists in the database. Returns false if this is the case
            self.mycursor.fetchall()
            return False
        self.mycursor.fetchall()
        return True
       # Displays an error message otherwise
       else:
           return False

   def addDetailsToDatabase(self,username,password,phonenumber):
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    self.mycursor.execute("INSERT INTO Users (Username, Password, PhoneNumber) VALUES (%s,%s,%s)",(username,hashedPassword,phonenumber))
    scoreTableId = self.mycursor.lastrowid
    self.mycursor.execute("INSERT INTO Scores (UserID) VALUES (%s)",(scoreTableId,))
    self.username = username # Saves the username for usage in managing account details throughout the program's runtime
    self.db.commit()
 
   def createAccount(self):
       pass
 
   def verifyInput(self):
       pass
 
class forgotPass(accountSystem):
 
   def __init__(self,screen):
       super().__init__(screen)
       self.sendMessageButton = button("red", 275, 440, 200, 100, 22,self.screen,'Send message')
       self.phoneNumberInput = InputBox(275,360)
       self.phoneNumberFont = pygame.font.SysFont("arialunicode",30)
       self.phoneNumberImg = None
       self.userPhoneNumber = None
       self.updatePasswordButton = button("red", 275, 440, 200, 100, 22,self.screen,'Update password')
       self.newPasswordInput = InputBox(275,360)
       self.newPasswordFont = pygame.font.SysFont("arialunicode",30)
       self.newPasswordImg = None
       self.errorMessageSendCodeFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessageSendCodeImg = self.errorMessageSendCodeFont.render("Code failed to send", True, "Red")
       self.errorMessagePasswordFont = pygame.font.SysFont("arialunicode",15)
       self.errorMessagePasswordImg = self.errorMessagePasswordFont.render("Password must be at least 8 characters, contain a capital letter, lowercase letter, number and symbol", True,"Red")
       self.errorMessagePhoneNumberDBFont = pygame.font.SysFont("arialunicode",20)
       self.errorMessagePhoneNumberDBImg = self.errorMessagePhoneNumberDBFont.render("Phone number is not registered", True, "Red")
       self.oneTimePasswordSystem = oneTimePassword(screen,"forgotpass","forgotpass")
       self.display = "forgotpass"
 
   def drawDisplay(self):
    self.screen.fill((0,0,0))
    self.titleImg = self.titleFont.render("Pac-Man",True,"Red")
    self.screen.blit(self.titleImg,(275,135))
    if self.display == "forgotpass":
       self.phoneNumberImg = self.phoneNumberFont.render("Phone Number",True,"Red")
       self.screen.blit(self.phoneNumberImg,(305,310))
       self.sendMessageButton.draw(self.screen)
    elif self.display == "otp":
       self.oneTimePasswordSystem.drawDisplay() 
    elif self.display == "changepass":
        self.newPasswordImg = self.newPasswordFont.render("New Password",True, "Red")
        self.screen.blit(self.newPasswordImg,(305,310))
        self.updatePasswordButton.draw(self.screen)

   def checkIfPasswordValid(self,password):
       # Checks if password meets complexity requirements and displays error message if not
       passwordValid = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[?!@#%$]).{8,}$",password)
       if passwordValid:
           return True
       else:
           return False

   def handleInputs(self,event):
    if self.display == "forgotpass":
        self.phoneNumberInput.handleEvent(event)
    elif self.display == "otp":
        self.oneTimePasswordSystem.handleInputs(event)
    elif self.display == "changepass":
        self.newPasswordInput.handleEvent(event)
 
   def drawInputs(self):
    if self.display == "forgotpass":
        self.phoneNumberInput.draw(self.screen)
    elif self.display == "otp":
        self.oneTimePasswordSystem.drawInputs()
    elif self.display == "changepass":
        self.newPasswordInput.draw(self.screen)

   def checkIfPhoneInDB(self):
        self.mycursor.execute("SELECT COUNT(*) FROM Users WHERE PhoneNumber=%s",(self.phoneNumberInput.getInputText(),)) # Checks if the phone number exists in the database. Returns false if this is the case
        count = self.mycursor.fetchone()[0]
        if count == 1:
            self.mycursor.fetchall()
            return True
        else:
            self.mycursor.fetchall()
            return False

   def checkIfButtonPressed(self):
    if self.display == "forgotpass":
       if self.sendMessageButton.isClicked():
           if self.checkIfPhoneInDB(): # Given that the phone is in the database, the username will be fetched in order to send the code to the user
            self.userPhoneNumber = self.phoneNumberInput.getInputText()
            self.mycursor.execute("SELECT Username FROM Users WHERE PhoneNumber=%s",(self.phoneNumberInput.getInputText(),))
            username = self.mycursor.fetchone()[0]
            self.mycursor.fetchall()
            if self.oneTimePasswordSystem.sendCode(username):
                self.username = username # Saves the username for usage in managing account details throughout the program's runtime
                self.display = "otp" # Switches display to otp screen if message has been successfully sent
            else:
                self.screen.blit(self.errorMessageSendCodeImg,(175,300)) # Otherwise the user will be displayed a message indicating failure to send the message
           else:
            self.screen.blit(self.errorMessagePhoneNumberDBImg,(275,340))
       return "forgotpass"

    elif self.display == "otp":
        if self.oneTimePasswordSystem.submitButton.isClicked():
            if self.oneTimePasswordSystem.checkIfCodeIsValid():
                self.display = "changepass"

        return "forgotpass"
        
    elif self.display == "changepass":   
       if self.updatePasswordButton.isClicked():
        if self.checkIfPasswordValid(self.newPasswordInput.getInputText()):
            self.updatePassword()
            return "mainmenu"
        else:
            self.screen.blit(self.errorMessagePasswordImg,(160,270))
            return "forgotpass"
       else:
        return "forgotpass"


   def updatePassword(self):
    hashedPassword = bcrypt.hashpw(self.newPasswordInput.getInputText().encode('utf-8'),bcrypt.gensalt())
    self.mycursor.execute("UPDATE Users SET Password = %s WHERE PhoneNumber = %s",(hashedPassword,self.userPhoneNumber))
    self.db.commit()


class mainMenu:
   def __init__(self,screen):
       self.screen = screen
       self.singleplayerButton = button("red", 275, 125, 200, 100, 22,self.screen,'Singleplayer')
       self.leaderboardButton = button("red",275,350,200, 100, 22, self.screen,'Leaderboard')
 
   def drawDisplay(self):
       self.screen.fill((0,0,0))
       self.singleplayerButton.draw(self.screen)
       self.leaderboardButton.draw(self.screen)

   def checkIfButtonPressed(self): 
       if self.singleplayerButton.isClicked():
           return "singleplayer"
       elif self.leaderboardButton.isClicked():
          return "leaderboard"
       elif self.multiplayerButton.isClicked():
          return "mainmenu"
       elif self.settingsButton.isClicked():
          return "mainmenu"
       else:
           return "mainmenu"
 
 