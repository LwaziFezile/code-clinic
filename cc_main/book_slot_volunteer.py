from googleapiclient.errors import HttpError
import googleapiclient.discovery as google_api_discovery
from .download_calendar_data import download_calendar_data
from .text_colors import TextColors
from halo import Halo
import datetime
CAMPUS_LOCATIONS = ['WeThinkCode_, Durban Club Pl, Durban Central, Durban, 4001, South Africa','WeThinkCode_, 331 Albert Rd, Woodstock, Cape Town, 7915, South Africa','WeThinkCode_, 84 Albertina Sisulu Rd, Johannesburg, 2000, South Africa']

def book_slot(user_cal : dict, cc_cal : dict, user : str, serviceObj : google_api_discovery.Resource, userName : str, CC_ID : str, campus : str) -> None:
    """
    The function `book_slot` prompts the user to book a slot by specifying the date and time. It handles various scenarios such as returning to the main menu, checking for existing bookings, and inserting new events into the calendars.

    Parameters:
    - user_cal (dict): A dictionary containing user's calendar data.
    - cc_cal (dict): A dictionary containing the Coding Clinic calendar data.
    - user (str): Specifies the type of user, whether "Volunteer" or not.
    - serviceObj (google_api_discovery.Resource): Google API service object for calendar operations.
    - userName (str): Name of the user booking the slot.
    - CC_ID (str): ID of the Coding Clinic calendar.
    - campus (str): Campus location where the session is booked.

    Returns:
    None

    Raises:
    HttpError: If an error occurs during calendar event insertion.

    Functionality:
    - If the user is a "Volunteer", it prompts the user to specify the date and time for booking a session.
    - If the user enters 'Menu', it returns to the main menu after updating the calendar data.
    - Checks if the slot is already booked. If booked, notifies the user; otherwise, creates a new event on both calendars.
    - Returns the updated calendar data after booking.
    - Raises HttpError if an error occurs during calendar event insertion.

    """
    
    try:
        if user == "Volunteer":
            summary = f'Available Coding Clinic session by {userName} as Volunteer'
            format_check = False
            date = input(f"What date do you want to book your session as a {user}? Use yyyy-mm-dd format: ")
            
            while format_check != True:
                if date.capitalize() == 'Menu':
                    spinner = Halo(text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...", spinner="dots").start()
            
                    user_cal, cc_cal, userName, state = download_calendar_data(serviceObj, CC_ID, campus)
                    spinner.succeed()
                    return user_cal, cc_cal, userName, state
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                    format_check = True
                except ValueError as ve:
                    date = input(f'Invalid format. Enter date of session you want to book for {TextColors.BLUE}{TextColors.BOLD}"YYYY-MM-DD"{TextColors.END}{TextColors.RESET} format: ')
            
            format_check = False
            time = input("Enter time in 'HH:MM': ")
                
            
            while format_check != True:
                if time.capitalize() == 'Menu':
                    spinner = Halo(text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...", spinner="dots").start()
            
                    user_cal, cc_cal, userName, state = download_calendar_data(serviceObj, CC_ID, campus)
                    spinner.succeed()
                    return user_cal, cc_cal, userName, state
                try:
                    datetime.datetime.strptime(time, '%H:%M')
                    format_check = True
                except ValueError as ve:
                    time = input(f'Invalid format. Enter time of session you want to delete for {TextColors.BLUE}{TextColors.BOLD}{date}{TextColors.END}{TextColors.RESET} in "HH:MM" format: ')
                
            format_check = False
            mins = time[3:5]
            hour = time[0:2]

            mins = int(mins) + 30
            if int(mins) > 60:
                hour = int(time[0:2]) + 1
                mins = '15'
            elif int(mins) == 60:
                hour = int(time[0:2]) + 1
                mins = '00'
            date_time = f'{date}T{time}:00+02:00'
            date_time_end = f'{date}T{hour}:{mins}:00+02:00'
            check_booked = False
            for i in user_cal:
                
                check_sum = user_cal[i]['summary']
                check_time = user_cal[i]['startTime']
                if summary == check_sum and check_time == date_time:
                    print('You cannot Book for a slot you already booked')
                    check_booked = True
                    break
            if check_booked == False:
                new_event = {
                    'summary' : summary,
                    'description' : '',
                    'start' : {
                        'dateTime' : date_time,
                        'timeZone' : 'Africa/Johannesburg',
                    }, 
                    'end' : {
                        "dateTime" : date_time_end,
                        'timeZone' : 'Africa/Johannesburg',
                },'creator': 
                {
                    'email': f'{userName}@student.wethinkcode.co.za', 
                    'self': True}
                }
                for wtc_campus in CAMPUS_LOCATIONS:
                    if campus in wtc_campus.lower():
                        new_event['location'] = wtc_campus 
                new_event = serviceObj.events().insert(calendarId ='primary', body = new_event).execute()
                new_event = serviceObj.events().insert(calendarId = CC_ID, body = new_event).execute()
                print("Session created successfully.")
            
    except HttpError as e:
        print(e)
        return user_cal, cc_cal, userName, False
    return download_calendar_data(serviceObj, CC_ID, campus)
