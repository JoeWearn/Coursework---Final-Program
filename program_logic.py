import login_screen
import detail_screen
import room_no_buttons
import calendar_display

"""
Run this file for program to work.
"""

# Defines Booleans

loop = True
loop2 = True

# Instantiates classes
login = login_screen.LoginHandler()
register = detail_screen.RegisterHandler()
menu = room_no_buttons.MenuHandler()


login.login_visuals()

while loop == True:
    
    if login.register_account:
        login.register_account = False
        register.register_user()

        if register.registered:
            login.login_visuals()

        if register.registered == False:
            print('HEY!')
            loop = False

    elif login.register_account == False:
        loop = False

    if login.login_successful:
        break

if login.login_successful:
    credentials = login.credentials

    while loop2 == True:
        menu.create_window()

        if menu.button_press:
            calendar = calendar_display.CalendarGUIHandler(menu.room_number)
            calendar.class_run(credentials)

            if calendar.go_back:
                pass

            if calendar.go_back == False:
                loop2 = False

        elif menu.button_press == False:
            loop2 = False
                        
