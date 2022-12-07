# login_screen.py

# Joseph Wearn

# Import

from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import ImageTk, Image



ELEMENTS_FOLDER = "elements/"       # Defines file constants



# Defines classes and methods

class LoginHandler:
    def __init__(self):
        """
        Creates the login screen GUI & checks if username and password match for an account.
        """
        self.login_successful = False       # Boolean for successful login
        self.register_account = False       # Boolean for regiserting an account
        self.hidden = False                 # Boolean for whether password is hidden

    def register(self):
        """
        Method for when user successfully logs in - destroys window and register_account is True.
        """
        self.window.destroy()
        self.register_account = True

    def login(self):
        """
        Authenticates login for existing accounts.
        """
        self.credentials = [
            self.login_username.get(),
            self.login_password.get()
        ]                               # Username and password put into a list


        # SQL for selecting the email and password from database corresponding to the username input by user

        connection = sqlite3.connect("sql_database_bookings.db")    # Connects to database
        crsr = connection.cursor()              # Creates a cursor for the database
        retrieve_email_password = f"""  \
            SELECT Email, Password \
            FROM Customer_details \
            WHERE Email = ("{self.credentials[0]}") \
        """                                     # Defines SQL command
        crsr.execute(retrieve_email_password)   # Excutes SQL command
        output = crsr.fetchone()                # Fetches result and defines as output
        connection.close()                      # Closes connection to database

        # If username and password input by user match the username and password retrieved from database, successfully login
        if (self.credentials[0] == output[0]
            and self.credentials[1] == output[1]
        ):
            self.window.destroy()
            self.login_successful = True
        
        else:
            messagebox.showinfo(
                "ERROR", "Invalid entry detected."
            )                                        # Creates a message box for incorrect logins

    def login_visuals(self):
        """
        Creates login screen visuals using Tkinter.
        """

        self.window = Tk()                  # Instantiates Tkinter class (window)
        self.window.geometry("1536x864")    # Assigns geometry of window
        self.window.title("Login")          # Assigns title
        self.window.configure(              # Congifures background to match colour scheme
            bg = "#CEEAF6"
        )

        # Creates (image) frame for login
        login_frame_image = Image.open(
            ELEMENTS_FOLDER + "loginshape1.gif"
        )                                                      
        login_frame_imagetk = ImageTk.PhotoImage(
            login_frame_image
        )
        login_image_label = Label(
            image = login_frame_imagetk
        )
        login_image_label.place(
            x = 587.5, y = 292,
            width = 345, height = 296
        )

        # Shows the user icon on the username entrybox
        username_image = Image.open(
            ELEMENTS_FOLDER + "usernameImage.gif"
        )                                                       
        username_imagetk = ImageTk.PhotoImage(
            username_image
        )
        username_label = Label(
            image = username_imagetk
        )
        username_label.place(
            x = 640, y = 340,
            width = 40, height = 41
        )

        # Shows the key icon on the password entrybox
        password_image = Image.open(          
            ELEMENTS_FOLDER + "passwordImage.gif"
        )                                                       
        password_imagetk = ImageTk.PhotoImage(
            password_image
        )
        password_label = Label(
            image=password_imagetk
        )
        password_label.place(
            x = 640, y = 400, width = 40, height = 41
        )

        # Username input is defined as a StringVar
        self.login_username = StringVar()   
        # Creates username entrybox
        username = EntryPlaceholders(
            self.window,
            placeholder = "Email",
            textvariable = self.login_username
        )
        username.place(
            x = 680, y = 340,
            width = 203, height = 41
        )

        # Password input is defined as a StringVar
        self.login_password = StringVar()
        # Creates Password entrybox                      
        password = EntryPlaceholders(                          
            self.window,
            placeholder = "Password",
            textvariable = self.login_password
        )
        password.place(
            x = 680, y = 400,
            width = 203, height = 41
        )

        # Creates button to hide/show password
        password_visiblity_image = Image.open(
            ELEMENTS_FOLDER + "passwordImage2.gif"
        )                                                       
        password_visiblity_imagetk = ImageTk.PhotoImage(
            image = password_visiblity_image
        )
        password_visibility_button = Button(
            image = password_visiblity_imagetk,
            command = lambda: self.hide(password)
        )
        password_visibility_button.place(
            x = 841.5, y = 400,
            width = 40, height = 41
        )

        # Creates a button to login
        login_button = Button(
            self.window,
            text = "Login", bg = "white",
            command = lambda: self.login()
        )                                                      
        login_button.place(
            x = 784.7, y = 480,
            width = 100, height = 41
        )

        # Creates a button to register an account
        register_button = Button(
            self.window,
            text = "Register", bg = "white",
            command = lambda: self.register()
        )                                                       
        register_button.place(
            x = 641.5, y = 480,
            width = 100, height = 41
        )

        self.window.mainloop()

    def hide(self,
        password
    ):
        """
        This function is toggles between displaying plain text and '****' in the password entry box, called when the 
        'password_visibility_button' button is clicked.
        """

        if self.hidden == True:
            password.config(show = "")
            self.hidden = False
        elif self.hidden == False:
            password.config(show = "*")
            self.hidden = True

class EntryPlaceholders(Entry):
    def __init__(self, *args, **kwargs):
        """
        Extends generic Tkinter Entry class - when entry box is clicked, placeholder text is wiped. When no longer clicked, if the 
        entry box is empty, replaces placeholder text.
        """

        self.placeholder = kwargs.pop(      # Pops placeholder text from kwargs and stores as self.placeholder
            "placeholder", ""
        )                                   
        super().__init__(*args, **kwargs)   # Inherits __init__ from Tkinter Entry class   

        self.insert(                # Inserts placeholder text initially
            "end", self.placeholder
        )                               
        self.bind(                  # When clicked on, removes placeholder text
            "<FocusIn>", self.remove_placeholder
        )                               
        self.bind(                  # When clicked off, replaces placeholder text
            "<FocusOut>", self.add_placeholder
        )                               

    def remove_placeholder(self, event):
        """
        Removes placeholder text if present.
        """

        if self.get() == self.placeholder:      # If when clicked, the contents of the entry box are still the placeholder text
            self.delete( 0, "end")              # ... it gets removed

    def add_placeholder(self, event):
        """
        Adds placeholder text if the entrybox is empty.
        """
        
        if self.placeholder and self.get() == "":   # If placeholder and contents of entry box are empty / nothing
            self.insert(0, self.placeholder)        # ... inserts placeholder back into entry box                                     