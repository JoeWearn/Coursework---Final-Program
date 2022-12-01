# Imports

from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import date
import sqlite3
import math


# Def

admin_ID = 1

"""
The admin is the first account created - This will assume so, and thus the account with the first ID in the Customer_ID table in the 
database will be the admin. If you want to change the admin account, change this variable to match the appropriate account ID.
"""

class CalendarGUIHandler:
    def __init__(self,
    room_number
    ):
        """
        Creates a display for dates booked for a room.
        Works by calculating the month (and therefore the appropriate amount of days for that month), and then
        generates buttons for each day. It then SQL queries the database to see if a date is booked. If it is
        booked, the button can be clicked but will do nothing. If it is not booked, the button can be
        clicked to book it. The admin (client) andthe user (customer) who creates the booking will be able to
        cancel all/ their own bookings respectively.
        """
        self.room_number = room_number      # Locally defines self.room_number as room_number passes in program_logic
        self.month = (
            date.today().month
        )                                   # Sets the month and year variable based on the current date
        self.year = (
            date.today().year
        )
        self.go_back = False                # Boolean for going back to menu

    # Initial method called
    def class_run(self,
        credentials
    ):
        self.window = Tk()

        self.window.title("Calendar")
        self.window.geometry("1536x864")
        self.window.configure(
            background = "#CEEAF6"
        )

        self.window.columnconfigure(    # Centres window
            0, weight=1
        )                       

        self._frame = Frame(            # Creates frame
            self.window,
            background = "#fde3d4",
            highlightbackground = "black",
            highlightthickness = 1,
        )                      

        self._frame.grid(       # Creates grid for frame
        )                     

        self.dates_dict = []    # Creates dict for dates booked (to append when booking new dates)

        self.go_back = False

        connection = sqlite3.connect("sql_database_bookings.db")    # Connects to database                               
        crsr = connection.cursor()      # Creates Cursor for database
        select_id_sql = f""" \
            SELECT (Customer_ID)    \
            FROM (Customer_details) \
            WHERE Email = ("{credentials[0]}") \
            AND Password = ("{credentials[1]}") \
        """                             # Retrieves Customer ID for the account with the user's credentials
        crsr.execute(select_id_sql)     # Executes SQL command                              
        user_ID = crsr.fetchone()       # Defines variable with selected Customer_ID

        update = Button(                # Creates a button to update bookings in database
            self.window,
            text = "Update", background = "white",
            command = lambda: self.update_func(user_ID)
        )                              
        update.place(
            x = 1070, y = 700,
            width = 100, height = 41
        )

        back = Button(                  # Creates a button to go back to menu
            self.window,    
            text = "Back", background = "white",
            command = lambda: self.back()
        )                              
        back.place(
            x = 365, y = 700,
            width = 100, height = 41
        )

        self.run(                       # Calls method that executes calendar GUI generation
            self.month, self.year, user_ID              
        )
        self.window.mainloop()

    # Method to close window & go_back becomes True
    def back(self):                              
        self.window.destroy()
        self.go_back = True

     # Method to update database with new bookings
    def update_func(self,
        user_ID
    ):
        connection = sqlite3.connect("sql_database_bookings.db")    # Connects to database
        crsr = connection.cursor()              # Creates cursor for database
        for booking in self.dates_dict:         # Loops for each element in dictionary
            insert_bookings = f"""      \
                INSERT INTO Bookings    \
                (Customer_ID, Room_Number, Year, Month, Day) \
                VALUES  \
                ("{user_ID[0]}",    \
                "{self.room_number}",   \
                "{booking[0]}", \
                "{booking[1]}", \
                "{booking[2]}")    \
            """
            connection.execute(
                insert_bookings
            )                                           # Executes SQL command
        connection.commit()                             # Commits changes to database
        connection.close()                              # Closes connection

    # Calls methods needed to generate calendar GUI.  
    def run(self,
        month, year, user_ID
    ):
        self.print_month_year(      # Calls method for months at top of GUI
            month, year
        )
        self.make_buttons(          # Calls method to create buttons for going to previous and next month
            month, year, user_ID
        )
        self.month_generator(       # Calls method to create bulk of GUI
            self.day_month_starts(
                month, year
            ),
            self.days_in_month(
                month, year
            ),
            month, year, user_ID
        )

    # Creates method to output the month and year at top of calendar
    def print_month_year(self,
        month, year           
    ):

        month_list = [
            'January', 'February', 'March',
            'April', 'May', 'June',
            'July', 'August', 'September',
            'October', 'November', 'December']

        title_month = month_list[int(month)-1]

        # Output month and year at top of calendar
        month_year = Label(
            self._frame,        
            bg = "#fde3d4",
            text = title_month + " " + str(year),
            font = ("Times New Roman", 20),
        )
        month_year.grid(
            column = 2, row = 0, columnspan = 3
        )

    # Function to switch calendar's month (1 for forwards and -1 for backwards)
    def switch_months(self,
        direction,
        month, year,
        user_ID  
    ):

        # Check if we are going to next year
        if (
            month == 12
            and
            direction == 1
        ):                      
            month = 1
            year += 1

        # Check if we are going to previous year
        elif (
            month == 1
            and
            direction == -1
        ):
            month = 12
            year -= 1

        # If neither are true, just adds or subtracts from month
        else:
            month += direction


        self._frame.destroy()        # Destroys _frame
        self._frame = Frame(         # Remakes _frame
            self.window,
            bg = "#fde3d4",
            highlightbackground = "black",
            highlightthickness = 1
        )
        self._frame.grid()           # Remakes grid
        self.run(                    # Re-runs method to create GUI
            month, year, user_ID
        )  

     # Method to create buttons to change month
    def make_buttons(self,
        month, year, user_ID        
    ):
        # Last month
        go_back = Button(                  
            self._frame,
            text = "Previous",
            width = 10,
            bg = "white",
            command = lambda: self.switch_months(-1,
                month, year, user_ID
            )
        )
        go_back.grid(
            column=0, row=0
        )

        # Next month
        go_forward = Button(               
            self._frame,
            text = "Next",
            width = 10,
            bg = "white",
            command = lambda: self.switch_months(1,
                month, year, user_ID
            )
        )
        go_forward.grid(
            column = 6, row = 0
        )

    def month_generator(self,
        start_date, number_of_days,
        month, year, user_ID
    ):
        """
        Generates a button for each day for the month displayed. 
        """
        # List of days
        days = [            
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        # Places the days of the week on the top of the calender
        for n in range(7):
            names = Label(
                self._frame,
                text = days[n], fg = "black", bg = "#fde3d4"
            )
            names.grid(
                column = n, row = 1, sticky = "nsew"
            )

        index = 0   # For below loop
        day = 1

        dict = {}   # Dict for buttons

        r_no = self.room_number

        for row in range(6):
            for column in range(7):     # 7 cross for days of week
                if (
                    index >= start_date                         # Creates a frame that will hold each day and button
                    and
                    index <= start_date + number_of_days - 1
                ):

                    day_frame = Frame(
                        self._frame, bg = "#fde3d4"
                    )

                    # Extended generic Tkinter button for all buttons generated in calendar
                    button = CalendarDayButton(self,
                        year, month, day,
                        user_ID, r_no,
                        day_frame,
                        width = 15, height = 5,
                        bg = "#ccffc9",
                        text = "Available"
                    )
                    button.grid(
                        row = 1
                    )

                    # Adds the text object to the dict
                    dict[day] = button

                    # Formats dayframe correctly
                    day_frame.grid(
                        row = row + 2,column = column, sticky = "nsew"
                    )    
                    day_frame.columnconfigure(
                        0, weight = 1
                    )
                    day_number = Label(
                        day_frame, text = day, bg = "#fde3d4"
                    )
                    day_number.grid(
                        row = 0
                    )
                    day += 1
                index += 1

        booking_data = self.load_bookings()
        for date in booking_data:
            if self.room_number == date[3]:
                if year == date[0]:
                    if month == date[1]:
                        dict[date[2]].set_booked()

    def load_bookings(self
    ):
        connection = sqlite3.connect("sql_database_bookings.db")
        crsr = connection.cursor()
        select_bookings = f"""  \
            SELECT Year,Month,Day,Room_Number   \
            FROM Bookings   \
        """
        crsr.execute(select_bookings)
        output = crsr.fetchall()
        connection.close()

        return output

    # Create function for calculating if it is a leap year
    def is_leap_year(self,
        year
    ):
        # Calculation for if leap year
        if (
            year % 4 == 0         
            and (year % 100 != 0
            or year % 400 == 0)):
            return True
        else:
            return False


    def day_month_starts(self,
        month, year
    ):
        """
        Calculates the weekday any given month starts on using Zeller's congruence. Zeller's congruence accounts for the inconsistent
        lengths of February by treating it and January as being part of the previous year (therefore year - 1) and considers them to be
        the 13th and 14th month, hence the if statements. Assuming neither Jan or Feb, the algorithm runs as expected.
        """
        if month == 1:
            months_math = 13
            years_math = year - 1
        elif month == 2:
            months_math = 14
            years_math = year - 1
        else:
            months_math = month
            years_math = year

        zc = ((1 + math.floor(13 * (months_math + 1) / 5)
            + math.floor(years_math % 100)
            + math.floor(math.floor(years_math % 100) / 4)) % 7)
        zc = ((zc + 5) % 7)
        return zc

    def days_in_month(self,
        month, year
):
        """
        Calculates the number of days for the given month accounting for leap years.
        """
        # Months that have 31 days
        if (                  
            month == 1
            or month == 3
            or month == 5
            or month == 7
            or month == 8
            or month == 12
            or month == 10
        ):                      
            number_of_days = 31

        # Months that have 30 days
        elif (                  
            month == 4 
            or month == 6
            or month == 9
            or month == 11
        ):                      
            number_of_days = 30

        # Check to see if leap year to determine how many days in February
        else:                   
            leap_year = self.is_leap_year(year)             

            if leap_year:
                number_of_days = 29

            else:
                number_of_days = 28

        return number_of_days


class CalendarDayButton(Button):
    def __init__(self,
        calendar,
        year, month, day,
        user_ID, r_no,
        *args, **kwargs,
    ):
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
        super().__init__(*args, **kwargs)           # Inherits __init__ from generic Tkiner Button class
        self.config(command = self.button_click)    # When button clicked  -> runs button_click()

        self.selected = False       # Boolean for whether a date has been selected (NOT booked)
        self.booked = False         #   "      "     "    "   "   "    "  booked

        self.year = year            # Locally defines passed variables
        self.month = month          #   "       "       "       "
        self.day = day              # ...
        self.calendar = calendar    # ...
        self.user_ID = user_ID      # ...         
        self.r_no = r_no            # ...

    def button_click(self):                             # On button click ...

        if self.booked == False:                        # If this date isn't booked
            if self.selected == False:                      # And if they have not already selected it
                self.calendar.dates_dict.append(                # Append relevant information for booking (y,m,d) to dict
                    (self.year, self.month, self.day)   
                )
                self.config(    
                    bg = "#fbe3e3", activebackground = "#fbe3e3"
                )                                               # Changes button colour
                self.selected = True                            # Changes selected to True
            else:                                           # If it is selected
                self.calendar.dates_dict.remove(                # Remove relevant information for booking (y,m,d) from dict
                    (self.year, self.month, self.day)
                )
                self.config(
                    bg = "#ccffc9", activebackground = "#ccffc9"
                )                                               # Reverts button colour to normal
                self.selected = False                           # Reverts selected to False
        if self.booked == True:                         # If it is booked
            connection = sqlite3.connect("sql_database_bookings.db")
                                                            # Retrieves the Customer_ID for the booking
            crsr = connection.cursor()
            select_ID = f"""  \
                SELECT Customer_ID  \
                FROM (Bookings) \
                WHERE Year = ("{self.year}")    \
                AND Month = ("{self.month}")    \
                AND Day = ("{self.day}")    \
                AND Room_Number = ("{self.r_no}")   \
            """
            crsr.execute(select_ID)
            booking_customer_ID_1 = crsr.fetchone()         # Stores output of query as booking_customer_ID_1
            connection.close()

            # Note - SQL retrieves as Tuple data types - therefore must specify position of data in Tuple - e.g. [0] 
            if ((int(self.user_ID[0]) == booking_customer_ID_1[0])      # If ID of user is the same as the person who made the booking
                or
                (int(self.user_ID[0]) == admin_ID)                      # Or if user is on the Admin account
            ):
                """
                If the user is the person who booked the date, they can delete the booking. If they are the admin, they can delete any
                booking. If they aren't they cannot (obviously).
                """
                connection = sqlite3.connect(
                    "sql_database_bookings.db"
                )
                crsr = connection.cursor()                  # Deletes booking from database
                sql_command = f"""  \
                    DELETE FROM Bookings    \
                    WHERE Year = ("{self.year}")    \
                    AND Month = ("{self.month}")    \
                    AND Day = ("{self.day}")    \
                    AND Room_Number = ("{self.r_no}")
                """
                crsr.execute(
                    sql_command
                )
                connection.commit()                         # Commits change
                connection.close()

    def set_booked(             # If the day is booked
        self
    ):
        self.booked = True      # Booked set to True
        self.config(            # Configures button to make it distinct and obviously unable to be booked
            bg = "#ffcccb", activebackground = "#ffcccb", text = "Booked"
        )