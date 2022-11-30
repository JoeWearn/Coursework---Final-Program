# Imports

from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import date
import sqlite3

# Def

class MenuHandler():

    def __init__(self):
        """
        Creates window for the buttons for the seperate rooms.
        """
        self.room_number = 0
        self.button_press = False

    def create_window(self):
        self.unloop = False
        self.window = Tk()
        self.window.title("Menu")
        self.window.geometry("215x50")
        self.window.configure(background = "#CEEAF6")

        room_1 = Button(self.window, text = "Room 1", bg = "white", command = lambda: self.show(1))        #Creates a button to login
        room_1.grid(padx = 10, pady = 10, row = 2, column = 1)

        room_2 = Button(self.window, text = "Room 2", bg = "white", command = lambda: self.show(2))        #Creates a button to login
        room_2.grid(padx = 10, row = 2, column = 2)

        room_3 = Button(self.window, text = "Room 3", bg = "white", command = lambda: self.show(3))        #Creates a button to login
        room_3.grid(padx = 10, row = 2, column = 3)

        self.window.mainloop()

    def show(self, room_number):
        self.window.destroy()
        self.button_press = True
        self.room_number = room_number
