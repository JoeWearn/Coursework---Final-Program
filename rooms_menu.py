# Imports

from tkinter import *
import tkinter as tk


# Defs

class MenuHandler:
    def __init__(self):
        """
        Creates window for the buttons for the seperate rooms.
        """

        self.room_number = 0
        self.button_press = False       # Boolean used to return whether user pressed the button for the next window

    def create_window(self):
        """
        Creates three buttons for the user to click on - passes 1, 2, or 3 to the room_number variable accepted in the 'show' function
        This is then taken by the program_logic file to pass to the calendar_display file.
        """

        self.button_press = False

        self.window = Tk()
        
        self.window.title("Menu")
        self.window.geometry("215x50")
        self.window.configure(
            bg = "#CEEAF6"
        )

        room_1 = Button(
            self.window,
            text = "Room 1", bg = "white",
            command = lambda: self.show(1)
        )                               # Creates a button to see room 1 bookings
        room_1.grid(
            padx = 10, pady = 10, row = 2, column = 1
        )

        room_2 = Button(
            self.window,
            text = "Room 2", bg = "white",
            command  =lambda: self.show(2)
        )                               # Creates a button to see room 2 bookings
        room_2.grid(
            padx = 10, row = 2, column = 2
        )

        room_3 = Button(
            self.window,
            text = "Room 3",
            bg = "white",
            command = lambda: self.show(3)
        )                               # Creates a button to see room 3 bookings
        room_3.grid(
            padx = 10, row = 2, column = 3
        )

        self.window.mainloop()

    def show(self,
        room_number
    ):
        """
        Function for the button in order to pass room number and button_press (= True) to program_logic.
        """
        
        self.window.destroy()
        self.button_press = True
        self.room_number = room_number