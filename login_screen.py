# login_screen.py

# Joseph Wearn

# Import

from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import ImageTk, Image  

# Defines file constants

ELEMENTS_FOLDER = "elements/"

# Classes

class LoginHandler():

    def __init__(self):
        """
        Creates the login screen GUI & checks if username and password match for an account.
        """
        self.login_successful = False
        self.register_account = False
        self.hidden = False

    def register(self):
        self.window.destroy()
        self.register_account = True

    def login(self):    
        """
        Authenticates login for existing accounts.
        """

        self.credentials = [self.login_username.get(),self.login_password.get()] 

        connection = sqlite3.connect("sql_database_bookings.db")
        crsr = connection.cursor()
        sql_command = f'SELECT Email, Password FROM Customer_details WHERE Email = ("{self.credentials[0]}")' # {self.login_username.get()}
        crsr.execute(sql_command)
        output = crsr.fetchone()
        connection.close()

        if self.credentials[0] == output[0] and self.credentials[1] == output[1]:
            self.window.destroy()
            self.login_successful = True

    def login_visuals(self):
        """
        Creates login screen visuals using Tkinter.
        """
        self.window = Tk()
        self.window.geometry("1536x864")
        self.window.title("Login")
        self.window.configure(background = "#CEEAF6")

        loginframeimage = Image.open(ELEMENTS_FOLDER + "loginshape1.gif")                  #Creates (image) frame for login
        loginframeimagetk = ImageTk.PhotoImage(loginframeimage)
        loginimagelabel = Label(image = loginframeimagetk)
        loginimagelabel.place(x = 587.5, y = 292, width = 345, height =296)

        username_image = Image.open(ELEMENTS_FOLDER + "usernameImage.gif")                #Shows the user icon on the username entrybox
        username_imagetk = ImageTk.PhotoImage(username_image)
        username_label = Label(image = username_imagetk)
        username_label.place(x = 640, y = 340, width = 40, height =41)

        password_image = Image.open(ELEMENTS_FOLDER + "passwordImage.gif")                #Shows the key icon on the password entrybox
        password_imagetk = ImageTk.PhotoImage(password_image)
        password_label = Label(image = password_imagetk)
        password_label.place(x = 640, y = 400, width = 40, height =41)

        self.login_username = StringVar()
        username = Entry(self.window, textvariable = self.login_username)             #Creates username entrybox
        username.insert(0, "Email")
        username.place(x = 680, y = 340, width = 203, height = 41)

        self.login_password = StringVar()
        password = Entry(self.window, textvariable = self.login_password)             #Creates password entrybox
        password.insert(0, "Password")
        password.place(x = 680, y = 400, width = 203, height = 41)

        password_visiblity_image = Image.open(ELEMENTS_FOLDER + "passwordImage2.gif")              #Creates button to hide/show password - nonfunctional presently
        password_visiblity_imagetk = ImageTk.PhotoImage(image = password_visiblity_image)
        password_visibility_button = Button(image = password_visiblity_imagetk, command = lambda: self.hide(password))
        password_visibility_button.place(x = 841.5, y = 400, width = 40, height =41)

        login_button = Button(self.window, text = "Login", bg = "white", command = lambda: self.login())        #Creates a button to login
        login_button.place(x = 784.7, y = 480, width = 100, height = 41)

        register_button = Button(self.window, text = "Register", bg = "white", command = lambda: self.register())        #Creates a button to login
        register_button.place(x = 641.5, y = 480, width = 100, height = 41)

        self.window.mainloop()

    def hide(self, password):
        if self.hidden == True:
            password.config(show = '')
            self.hidden = False
        elif self.hidden == False:
            password.config(show = '*')
            self.hidden = True
