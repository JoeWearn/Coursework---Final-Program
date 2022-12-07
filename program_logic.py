# Imports

import login_screen
import detail_screen
import rooms_menu
import calendar_display

"""
Run this file for program to work.
"""

# Defines Booleans
loop = True
loop2 = True

# Instantiates classes for the login screen, the register screen, and the menu screen
login = login_screen.LoginHandler()
register = detail_screen.RegisterHandler()
menu = rooms_menu.MenuHandler()


login.login_visuals()       #   Runs login_visuals method from login object

while loop == True:         # Creates a loop to allow user to cycle between 'login_screen' and 'register_screen'

    if login.register_account:          # If the user clicks the register button on the login screen, runs the register_user method
        login.register_account = False  # from register object
        register.register_user()

        if register.registered:         # Once they successfully register an account, return to original login screen
            login.login_visuals()

        if register.registered == False:    # If they have not successfully created an account, this will run. The only circumstance
            break                           # where this should run is if the register window is closed - therefore, it will not loop
                                            # back to the login screen as presume they wish to exit program

    elif login.register_account == False:   # Likewise, but for login screen instead of register screen
        break

    if login.login_successful:              # Once they successfully login, the loop breaks as user cannot go back to login screen
        break

if login.login_successful:                  # Onced logged in, retrieves credentials input by user and stores locally
    credentials = login.credentials


    while loop2 == True:            # Creates a loop to allow user to cycle between 'room_no_buttons' and 'calendar_display'
        menu.create_window()        # Runs create_window method from menu object
        if menu.button_press:       # If they press one of the three buttons on the menu
            calendar = calendar_display.CalendarGUIHandler(menu.room_number)     # Instantiates classes for the 'calendar_display'
            calendar.class_run(credentials)     # Runs class_run method from calendar object, and passes credentials to the calendar

            if calendar.go_back:        # If they click the back button, loops, and therefore goes back to menu
                pass

            elif calendar.go_back == False:     # If they have not clicked the back button, presume closed window and therefore
                break                           # break loop

        elif menu.button_press == False:        # Likewise but for menu screen instead of calendar screen
            break