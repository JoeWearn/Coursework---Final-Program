# Imports

from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import date
import sqlite3


# Def         

admin_ID = 1

"""
The admin is the first account created - This will assume so, and thus the account with the first ID in the Customer_ID table in the 
database will be the admin. If you want to change the admin account, change this variable to match the appropriate account ID.
"""



class CalendarGUIHandler():

    def __init__(self, room_number):
        """
        Creates a display for dates booked for a room.
        Works by calculating the month (and therefore the appropriate amount of days for that month), and then 
        generates buttons for each day. It then SQL queries the database to see if a date is booked. If it is
        booked, the button can be clicked but will do nothing. If it is not booked, the button can be
        clicked to book it. The admin (client) andthe user (customer) who creates the booking will be able to
        cancel all/ their own bookings respectively.
        """
        self.room_number = room_number
        self.month = date.today().month              # Sets the month and year variable based on the current date
        self.year = date.today().year
        self.go_back = False

    def class_run(self,credentials):
        self.window = Tk()
        self.window.title("Calender")
        self.window.geometry("1536x864")
        self.window.configure(background = "#CEEAF6")
        
        self.window.columnconfigure(0, weight = 1)     # Centers the calendar

        self._frame = Frame(self.window, background = '#fde3d4',
            highlightbackground = "black",  highlightthickness=1)       # Creates frames from the window.
        self._frame.grid()                                      # This makes the grid object appea

        self.dates_dict = []
        
        self.go_back = False

        connection = sqlite3.connect("sql_database_bookings.db")
        crsr = connection.cursor()
        sql_command2 = f'SELECT Customer_ID FROM (Customer_details) WHERE Email = ("{credentials[0]}") AND Password = ("{credentials[1]}")'
        crsr.execute(sql_command2)
        user_ID = crsr.fetchone()


        update = Button(self.window, text = "Update", background = "white", command = lambda: self.update_func(user_ID))        #Creates a button to login
        update.place(x = 1070, y = 700, width = 100, height = 41)

        back = Button(self.window, text = "Back", background = "white", command = lambda: self.back())        #Creates a button to go back
        back.place(x = 365, y = 700, width = 100, height = 41)

        self.run(self.month, self.year, user_ID)

        self.window.mainloop()

    def back(self):
        self.window.destroy()
        self.go_back = True

    def update_func(self, user_ID):
        connection = sqlite3.connect("sql_database_bookings.db")
        crsr = connection.cursor()
        for booking in self.dates_dict:
            sql_command = f'INSERT INTO Bookings (Customer_ID,Room_Number, Year, Month, Day) VALUES ("{user_ID[0]}","{self.room_number}","{booking[0]}","{booking[1]}","{booking[2]}")'
            connection.execute(sql_command)
        connection.commit()
        connection.close()

    def run(self, month, year, user_ID):
        """
        Calls functions needed to generate calendar GUI.
        """
        self.print_month_year(month, year)
        self.make_buttons(month, year, user_ID)
        self.month_generator(self.day_month_starts(month, year),
            self.days_in_month(month, year),
            month, year, user_ID)

    def print_month_year(self, month, year):      # Creates function to output the month and year at top of calendar

        if month == 1:                     
            written_month = "January"
        elif month == 2:
            written_month = "February"
        elif month == 3:
            written_month = "March"
        elif month == 4:
            written_month = "April"
        elif month == 5:
            written_month = "May"
        elif month == 6:
            written_month = "June"
        elif month == 7:
            written_month = "July"
        elif month == 8:
            written_month = "August"
        elif month == 9:
            written_month = "September"
        elif month == 10:
            written_month = "October"
        elif month == 11:
            written_month = "November"
        else:
            written_month = "December"
        
        month_year = Label(self._frame,    # Output month and year at top of calendar
            bg = '#fde3d4',
            text = written_month + " " + str(year),
            font= ("Times New Roman", 20))                   
        month_year.grid(column = 2, row = 0, columnspan = 3)


    def switch_months(self, direction, month, year, user_ID):   # Function to switch calendar's month (1 for forwards and -1 for backwards)

        if month == 12 and direction == 1:  # Check if we are going to a new year
            month = 1
            year += 1
        elif month == 1 and direction == -1:
            month = 12 
            year -= 1
        else:
            month += direction

        # Reprints the calendar with the new values

        self._frame.destroy()
        self._frame = Frame(self.window, bg = '#fde3d4', highlightbackground = "black",  highlightthickness=1)
        self._frame.grid()
        self.run(month,year, user_ID)
    
    
    def make_buttons(self, month, year, user_ID):           # Changes month buttons at top of the page  
        go_back = Button(self._frame,      
            text = "Previous",
            width = 10,
            bg = "white",
            command = lambda : self.switch_months(-1,
                month,
                year,
                user_ID))

        go_back.grid(column = 0, row = 0)

        go_forward = Button(self._frame,
            text = "Next",
            width = 10,
            bg = "white",
            command = lambda : self.switch_months(1,
                month,
                year,
                user_ID))

        go_forward.grid(column = 6, row = 0)


    # Creates most of the calendar
    def month_generator(self, start_date, number_of_days, month, year, user_ID):
        # Holds the names for each day of the week 
        day_names = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Places the days of the week on the top of the calender
        for name_number in range(7):
            names = Label(self._frame, text = day_names[name_number], fg = "black", bg = '#fde3d4')
            names.grid(column = name_number, row = 1, sticky = 'nsew')

        index = 0
        day = 1

        dict = {}

        r_no = self.room_number
        for row in range(6):
            for column in range(7):
                if index >= start_date and index <= start_date + number_of_days-1:
                    # Creates a frame that will hold each day and button
                    day_frame = Frame(self._frame, bg = '#fde3d4')

                    button = CalendarDayButton(self,
                        year, month, day,
                        user_ID, r_no, 
                        day_frame,
                        width = 15, height = 5,
                        bg = '#ccffc9', text = 'Available')
                    button.grid(row = 1)

                    # Adds the text object to the dict
                    dict[day] = button

                    # Changes changes dayframe to be formated correctly
                    day_frame.grid(row=row + 2, column=column, sticky = 'nsew')
                    day_frame.columnconfigure(0, weight = 1)
                    day_number = Label(day_frame, text = day, bg = '#fde3d4')
                    day_number.grid(row = 0)
                    day += 1
                index += 1

        booking_data = self.load_bookings()
        for date in booking_data:
            if self.room_number == date[3]:
                if month == date[1]:
                    dict[date[2]].set_booked()
                    


    def load_bookings(self):
        connection = sqlite3.connect("sql_database_bookings.db")
        crsr = connection.cursor()
        sql_command = f'SELECT Year,Month,Day,Room_Number FROM Bookings'
        crsr.execute(sql_command)
        output = crsr.fetchall()
        connection.close()

        return output
        

    # Create function for calculating if it is a leap year
    def is_leap_year(self, year):
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return True
        else:
            return False


    # Create function for calculating what day month starts
    def day_month_starts(self, month, year):
        day_month_starts_var = ((year - 2000) // 4) + 1
        if month == 1 or month == 10:
            day_month_starts_var += 1
        elif month == 2 or month == 3 or month == 11:
            day_month_starts_var += 4
        elif month == 5:
            day_month_starts_var += 2
        elif month == 6:
            day_month_starts_var += 5
        elif month == 8:
            day_month_starts_var += 3
        elif month == 9 or month == 12:
            day_month_starts_var += 6
        else:
            day_month_starts_var += 0
        
        leap_year = self.is_leap_year(year)
        if leap_year and (month == 1 or month == 2):
            day_month_starts_var -= 1
        day_month_starts_var += 6                               
        day_month_starts_var += (year - 2000)                      
        day_of_week = day_month_starts_var % 7

        return day_of_week

    def days_in_month (self, month, year):
        """
        Calculates the number of days for the given month accounting for leap years.
        """
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 12 or month == 10:    # Months that have 31 days
            number_of_days = 31
        elif month == 4 or month == 6 or month == 9 or month == 11:     # Months that have 30 days
            number_of_days = 30
        else:
            leap_year = self.is_leap_year(year)              # Check to see if leap year to determine how many days in February
            if leap_year:
                number_of_days = 29
            else:
                number_of_days = 28

        return number_of_days


class CalendarDayButton(Button):
    
    def __init__(self, calendar, year, month, day, user_ID, r_no, *args, **kwargs, ):
        """
        This class essentially serves as a customised Tkinter 'Button' class. The buttons created instantiating this instead of the
        generic Tkinter button will have certain parameters (e.g. - calendar, year, month, etc.) explicitly, alongside an 'on click'
        function. This function runs upon being clicked (obviously) and checks if each button instantiated from this class matches the
        dates in the database for bookings.
        If they are not, they have a button click 'toggle' that allows them to be selected. The dates toggled as selected are appended
        to the booked dictionary, which defines all booked dates. When the 'update' button created in the __init__ for the
        CalendarGUIHandler class, all items in the dictionary are added to the database.
        If the button's date equivalent is booked, it is considered 'booked', which means that the button for that date cannot be
        booked again. However, another 'if' check is ran to see if the person clicking is either the person who made the booking or the
        account with the admin ID. If either of the cases are true, clicking the button will result in its removal from the database.
        """
        super().__init__(*args, **kwargs)
        self.config(command = self.button_click)
        self.selected = False
        self.year = year
        self.month = month
        self.day = day
        self.calendar = calendar
        self.user_ID = user_ID
        self.booked = False
        self.r_no = r_no

    def button_click(self):

        if self.booked == False:
            if self.selected == False:
                self.calendar.dates_dict.append((self.year, self.month, self.day))
                self.config(bg = '#fbe3e3', activebackground = '#fbe3e3')
                self.selected = True
            else:
                self.calendar.dates_dict.remove((self.year, self.month, self.day))
                self.config(bg = '#ccffc9', activebackground = '#ccffc9')
                self.selected = False
        if self.booked == True:
            connection = sqlite3.connect("sql_database_bookings.db")
            crsr = connection.cursor()
            sql_command = f'SELECT Customer_ID FROM (Bookings) WHERE Year = ("{self.year}") AND Month = ("{self.month}") AND Day = ("{self.day}") AND Room_Number = ("{self.r_no}")'
            crsr.execute(sql_command)
            booking_customer_ID_1 = crsr.fetchone()
            connection.close()

            booking_customer_ID_2 = (booking_customer_ID_1[0])
            if (int(self.user_ID[0]) == booking_customer_ID_2[0]) or (int(self.user_ID[0]) == admin_ID):
                """
                If the user is the person who booked the date, they can delete the booking. If they are the admin, the can delete any
                booking.
                """
                print("works2")
                connection = sqlite3.connect("sql_database_bookings.db")
                crsr = connection.cursor()
                sql_command = f'DELETE FROM Bookings WHERE Year = ("{self.year}") AND Month = ("{self.month}") AND Day = ("{self.day}") AND Room_Number = ("{self.r_no}")'
                crsr.execute(sql_command)
                connection.commit()
                connection.close()


    def set_booked(self):
        self.booked = True
        self.config(bg = '#ffcccb', activebackground = '#ffcccb', text = 'Booked')
