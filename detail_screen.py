# Import
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
import re


class RegisterHandler:
    def __init__(self):
        self.registered = False     # Boolean for if user successfully registers an account

    def send_user_data(self):
        """
        Sends user data to database - Email, password, first name, last name, phone number, address.
        """
        # Defines acceptable inputs for email
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        # Defines acceptable inputs for phone number --> Format accepted = '+447222555555' or '+44 7222 555 555' or '(0722) 5555555'
        phone_number_regex = r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$'
        
        if ((re.fullmatch(email_regex, str(self.register_email.get())))
            and
            (re.fullmatch(phone_number_regex, str(self.register_phone_number.get())))
        ):
            connection = sqlite3.connect("sql_database_bookings.db")    # Connects to database                               
            crsr = connection.cursor()      # Creates a cursor for the database
            insert_to = f"""    \
                INSERT INTO Customer_details    \
                (Email,Password,First_name,Last_name,Phone_number,Address)  \
                VALUES("{self.register_email.get()}",  \
                "{self.register_password.get()}",   \
                "{self.register_first_name.get()}", \
                "{self.register_last_name.get()}",   \
                "{self.register_phone_number.get()}",   \
                "{self.register_address.get()}")   \
            """                         # Sends user data to database
            crsr.execute(insert_to)     # Executes sql command                           
            connection.commit()         # Commits insert to database
            connection.close()          # Closes connection
            self.window.destroy()       # Closes window
            self.registered = True      # Sets registered to True

        # If user entered data does not comply with both regex statements, displays error message box
        else:
            messagebox.showinfo(                      # Creates a message box for invalid entries
                "ERROR", "Invalid entry detected."  
            )    


    def register_user(
        self
    ):
        """
        Registers customer information to database.
        """
        self.window = Tk()
        self.window.geometry("1536x864")
        self.window.title("Register")
        self.window.configure(
            background = "#CEEAF6"
        ) 

        self.register_email = StringVar()           # Email input defined as StringVar
        email = EntryPlaceholders(                  # Creates username entrybox
            self.window,
            placeholder = "Email",
            textvariable = self.register_email
        )
        email.place(
            x = 680, y = 150,
            width = 203, height = 41
        )

        self.register_password = StringVar()        # Password input defined as StringVar
        password = EntryPlaceholders(               # Creates password entrybox
            self.window,
            placeholder = "Password",
            textvariable = self.register_password
        )
        password.place(
            x = 680, y = 200,
            width = 203, height = 41
        )

        self.register_first_name = StringVar()      # First name input defined as StringVar
        first_name = EntryPlaceholders(             # Creates first name entrybox
            self.window,
            placeholder = "First name",
            textvariable = self.register_first_name
        )
        first_name.place(
            x = 680, y = 250,
            width = 203, height = 41
        )

        self.register_last_name = StringVar()       # Last name input defined as StringVar
        last_name = EntryPlaceholders(              # Creates last name entrybox
            self.window,
            placeholder = "Last name",
            textvariable = self.register_last_name
        )
        last_name.place(
            x = 680, y = 300,
            width = 203, height = 41
        )

        self.register_phone_number = StringVar()    # Phone number input defined as StringVar
        phone_number = EntryPlaceholders(           # Creates phone number entrybox
            self.window,
            placeholder = "Phone number",
            textvariable = self.register_phone_number
        )
        phone_number.place(
            x = 680, y = 350,
            width = 203, height = 41
        )

        self.register_address = StringVar()         # Address input defined as StringVar
        address = EntryPlaceholders(                # Creates address entrybox
            self.window,
            placeholder = "Address",
            textvariable = self.register_address
        )
        address.place(
            x = 680, y = 400,
            width = 203, height = 41
        )

        login_button = Button(                              # Creates a button for registering an account
            self.window,
            text = "Register",
            background = "white",
            command = lambda: self.send_user_data(),
        )
        login_button.place(
            x = 680, y = 450,
            width = 100, height = 41
        )

        self.window.mainloop()


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
        Remove placeholder text if present.
        """
        if self.get() == self.placeholder:      # If when clicked, the contents of the entry box are still the placeholder text
            self.delete( 0, "end")              # ... it gets removed

    def add_placeholder(self, event):
        """
        Add placeholder text if the entrybox is empty.
        """
        if self.placeholder and self.get() == "":   # If placeholder and contents of entry box are empty / nothing
            self.insert(0, self.placeholder)        # ... inserts placeholder back into entry box                                     