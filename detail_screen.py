# Import
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
import re

class RegisterHandler():

    def __init__(self):
        self.registered = False

    def send_user_data(self):
        """
        Sends user data to database.
        """
        # Defines acceptable inputs for email
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # Defines acceptable inputs for phone number --> Format accepted = '+447222555555' or '+44 7222 555 555' or '(0722) 5555555'
        phone_number_regex = r'^(((\+44\s?\d{4}|\(?0\d{4}\)?)\s?\d{3}\s?\d{3})|((\+44\s?\d{3}|\(?0\d{3}\)?)\s?\d{3}\s?\d{4})|((\+44\s?\d{2}|\(?0\d{2}\)?)\s?\d{4}\s?\d{4}))(\s?\#(\d{4}|\d{3}))?$'
        if(re.fullmatch(email_regex, str(self.register_email.get()))) and (re.fullmatch(phone_number_regex, str(self.register_phone_number.get()))):
            connection = sqlite3.connect("sql_database_bookings.db")
            crsr = connection.cursor()
            sql_command = f'INSERT INTO Customer_details (Email,Password,First_name,Last_name,Phone_number,Address) VALUES ("{self.register_email.get()}","{self.register_password.get()}","{self.register_first_name.get()}","{self.register_last_name.get()}", {self.register_phone_number.get()},"{self.register_address.get()}")'
            crsr.execute(sql_command)
            connection.commit()
            connection.close()
            self.window.destroy()
            self.registered = True
        
        # If user entered data does not comply with both regex statements, displays error message box
        else:
            messagebox.showinfo('ERROR','Invalid entry detected.')
            
        

    def register_user(self):
        """
        Registers customer information to database.
        """
        self.window = Tk()
        self.window.geometry("1536x864")
        self.window.title("Register")
        self.window.configure(background = "#CEEAF6")

        self.register_email = StringVar()
        email = Entry(self.window, textvariable = self.register_email)             #Creates username entrybox
        email.insert(0, "Email")
        email.place(x = 680, y = 150, width = 203, height = 41)

        self.register_password = StringVar()
        password = Entry(self.window, textvariable = self.register_password)             #Creates username entrybox
        password.insert(0, "Password")
        password.place(x = 680, y = 200, width = 203, height = 41)

        self.register_first_name = StringVar()
        first_name = Entry(self.window, textvariable = self.register_first_name)             #Creates username entrybox
        first_name.insert(0, "First name")
        first_name.place(x = 680, y = 250, width = 203, height = 41)

        self.register_last_name = StringVar()
        last_name = Entry(self.window, textvariable = self.register_last_name)             #Creates username entrybox
        last_name.insert(0, "Last name")
        last_name.place(x = 680, y = 300, width = 203, height = 41)
        
        self.register_phone_number = StringVar()
        phone_number = Entry(self.window, textvariable = self.register_phone_number)             #Creates username entrybox
        phone_number.insert(0, "Phone number")
        phone_number.place(x = 680, y = 350, width = 203, height = 41)

        self.register_address = StringVar()
        address = Entry(self.window, textvariable = self.register_address)             #Creates username entrybox
        address.insert(0, "Address")
        address.place(x = 680, y = 400, width = 203, height = 41)

        login_button = Button(self.window, text = "Register", background = "white",
            command = lambda: self.send_user_data()) 
        login_button.place(x = 680, y = 450, width = 100, height = 41)

        self.window.mainloop()

