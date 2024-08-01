from .download_calendar_data import download_calendar_data
import googleapiclient.discovery as google_api_discovery
from .display_data import generate_calendar_table
from googleapiclient.errors import HttpError
import datetime
from .text_colors import TextColors
from halo import Halo
from time import sleep
import base64
from email.message import EmailMessage

def remove_event(user_cal: dict, cc_cal : dict, serviceObj : google_api_discovery.Resource, serviceObjMail : google_api_discovery.Resource,  user_name : str, user_type : str, CC_ID, campus):
    """
    Remove an event from the user's calendar or the Code Clinic calendar.
    Parameters:
    - user_cal (dict): The user's calendar data.
    - cc_cal (dict): The Code Clinic calendar data.
    - serviceObj (google_api_discovery.Resource): The service object used for accessing the Google Calendar API.
    - serviceObjMail (google_api_discovery.Resource): The service object used for accessing the Gmail API.
    - user_name (str): The name of the user.
    - user_type (str): The type of user, either "Volunteer" or "Student".
    - CC_ID (str): The ID related to the Code Clinic calendar.
    - campus (str): The campus information.

    This function allows either a volunteer or a student to remove an event from their respective calendars.
    If the user is a volunteer, they can remove a session from the Code Clinic calendar. If the user is a student,
    they can remove a session from their own calendar, and notify the volunteer about the cancellation via email.
    """
    user_code_clinic_events = {}
    
    try:
        if user_type == "Volunteer":    
            # Iterate through the keys (event identifiers) in the Code Clinic calendar.
            for key in cc_cal.keys():
                # Check if the user's name is contained in the event key.
                if user_name in key:
                    # If the user's name is found in the event key, add the event to the user's dictionary.
                    user_code_clinic_events[key] = cc_cal[key]
            if user_code_clinic_events != {}:
                print(f"{user_name}'s Coding Clinic Events for {datetime.datetime.now().date()} ")
                print(generate_calendar_table(user_code_clinic_events))
                
                format_check = False
                date_ = input(f'Enter date of session you want to delete in {TextColors.BLUE}{TextColors.BOLD}"YYYY-MM-DD"{TextColors.END}{TextColors.RESET} format: ')
                while format_check != True:
                    if date_.capitalize() == 'Menu':
                        spinner = Halo(text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...", spinner="dots").start()
            
                        user_cal, cc_cal, userName, state = download_calendar_data(serviceObj, CC_ID, campus)
                        spinner.succeed()
                        return user_cal, cc_cal, userName, state
                    try:
                        datetime.datetime.strptime(date_, '%Y-%m-%d')
                        format_check = True
                    except ValueError as ve:
                        date_ = input(f'Invalid format. Enter date of session you want to delete in {TextColors.BLUE}{TextColors.BOLD}"YYYY-MM-DD"{TextColors.END}{TextColors.RESET} format: ')
                
                format_check = False
                time_ = input(f'Enter time of session you want to delete for {TextColors.BLUE}{TextColors.BOLD}{date_}{TextColors.END}{TextColors.RESET} in "HH:MM" format: ')
                while format_check != True:
                    if time_.capitalize() == 'Menu':
                        spinner = Halo(text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...", spinner="dots").start()
            
                        user_cal, cc_cal, userName, state = download_calendar_data(serviceObj, CC_ID, campus)
                        spinner.succeed()
                        return user_cal, cc_cal, userName, state
                    try:
                        datetime.datetime.strptime(time_, '%H:%M')
                        format_check = True
                    except ValueError as ve:
                        time_ = input(f'Invalid format. Enter time of session you want to delete for {TextColors.BLUE}{TextColors.BOLD}{date_}{TextColors.END}{TextColors.RESET} in "HH:MM" format: ')
                
                format_check = False
                location = input(f'Enter campus you booked the session in: ')
                while format_check != True:
                    if location.capitalize() == 'Menu':
                        spinner = Halo(text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...", spinner="dots").start()
            
                        user_cal, cc_cal, userName, state = download_calendar_data(serviceObj, CC_ID, campus)
                        spinner.succeed()
                        return user_cal, cc_cal, userName, state
                    if location.lower() in ["durban", "johannesburg", "cape town"]:
                        format_check = True
                    else:
                        location = input(f'Invaild Campus, Enter campus you booked the session in: ')
                format_check = False
                if f'{date_}T{time_}:00+02:00{user_name}' in cc_cal.keys() and user_type == "Volunteer" and location.lower() in cc_cal[f'{date_}T{time_}:00+02:00{user_name}']['location'].lower():
                    
                    userkey = f'{date_}T{time_}:00+02:00{user_name}'
                    if 'attendees' in cc_cal[userkey].keys():
                        spinner = Halo(text="Session has already been booked by a Student. Returning to Main Menu...", spinner="dots").start()
                        spinner.fail()
                        sleep(3)
                        return user_cal, cc_cal, user_name, False 
                    else:
                        yes_no = input(f"Are you sure you want to {TextColors.RED}{TextColors.BOLD}DELETE{TextColors.RESET}{TextColors.END} this session for {location.capitalize()} campus? [Y/N] ")
                        if yes_no.lower() == 'y':

                            serviceObj.events().delete(calendarId=CC_ID, eventId = cc_cal[userkey]['eventId']).execute()
                            serviceObj.events().delete(calendarId='primary', eventId = cc_cal[userkey]['eventId']).execute()
                            
                            print("Session successfully deleted.")
                            return download_calendar_data(serviceObj, CC_ID, campus)
                        else:
                            spinner = Halo(text="Cancelling Operation, Returning to Main Menu...", spinner="dots").start()
                            user_cal, cc_cal, user_name, state = download_calendar_data(serviceObj, CC_ID, campus)
                            sleep(2)
                            spinner.succeed()
                            return user_cal, cc_cal, user_name, False
                else:
                    spinner = Halo(text="Invalid Event, Check the above table to see your events and enter prompts correctly Returning to Main Menu...", spinner="dots").start()
                    user_cal, cc_cal, user_name, state = download_calendar_data(serviceObj, CC_ID, campus)
                    sleep(3)
                    spinner.succeed()
                    return user_cal, cc_cal, user_name, False
            else:
                print("No Events on your calendar to delete")
                spinner = Halo(text="Returning to Main Menu...", spinner="dots").start()
                sleep(2)
                spinner.succeed()
                return user_cal, cc_cal, user_name, False
                   
        elif user_type == "Student":
            
            key, vol_key, user_name, attendees_dict = find_student_in_email(cc_cal, user_name)
            if key != False:

                print(f"Events for {user_type} {user_name}")
                print(generate_calendar_table(attendees_dict))

                format_check = False
                date_ = input(f'Enter date of session you want to delete in {TextColors.BLUE}{TextColors.BOLD}"YYYY-MM-DD"{TextColors.END}{TextColors.RESET} format: ')
                while format_check != True:
                    if date_.capitalize() == 'Menu':
                        return download_calendar_data(serviceObj, CC_ID, campus)
                    try:
                        datetime.datetime.strptime(date_, '%Y-%m-%d')
                        format_check = True
                    except ValueError as ve:
                        date_ = input(f'Invalid format. Enter date of session you want to delete in {TextColors.BLUE}{TextColors.BOLD}"YYYY-MM-DD"{TextColors.END}{TextColors.RESET} format: ')
                
                format_check = False
                time_ = input(f'Enter time of session you want to delete for {TextColors.BLUE}{TextColors.BOLD}{date_}{TextColors.END}{TextColors.RESET} in "HH:MM" format: ')
                while format_check != True:
                    if time_.capitalize() == 'Menu':
                        return download_calendar_data(serviceObj, CC_ID, campus)
                    try:
                        datetime.datetime.strptime(time_, '%H:%M')
                        format_check = True
                    except ValueError as ve:
                        time_ = input(f'Invalid format. Enter time of session you want to delete for {TextColors.BLUE}{TextColors.BOLD}{date_}{TextColors.END}{TextColors.RESET} in "HH:MM" format: ')
                
                format_check = False
                vol_key = input(f'Enter username of {TextColors.BLUE}{TextColors.BOLD}Volunteer{TextColors.END}{TextColors.RESET} you were booked to: ').lower()
                while format_check != True:
                    if vol_key.capitalize() == 'Menu':
                        return download_calendar_data(serviceObj, CC_ID, campus)
                    if f'{date_}T{time_}:00+02:00{vol_key}' in user_cal.keys():
                        format_check = True
                    else:
                        vol_key = input(f'{TextColors.RED}{TextColors.BOLD}Invalid Username{TextColors.END}{TextColors.RESET} or slot doesnt exist, check if there\'s a typo in your input and enter username of volunteer you were assigned to.\nType menu to exit operation: ').lower()

                
                if user_type == "Student":
                    yes_no = input(f"Are you sure you want to delete session {date_} @ {time_} with {vol_key}? [Y/N] ")
                    if yes_no.capitalize() == 'Menu':
                        return download_calendar_data(serviceObj, CC_ID, campus)
                    if yes_no.lower() == 'y':

                        deleted_key = f'{date_}T{time_}:00+02:00{vol_key}'
                        evnt = serviceObj.events().get(calendarId=CC_ID, eventId = user_cal[deleted_key]['eventId']).execute()
                        if 'attendees' in evnt.keys():
                            del evnt['attendees']

                        volunteer_mail = evnt["creator"]["email"]
                        volunteer_name = volunteer_mail[0:volunteer_mail.index('@')]
                        evnt['summary'] = f'Available Coding Clinic session by {volunteer_name} as Volunteer'
                        del evnt['description']

                        serviceObj.events().update(calendarId=CC_ID, eventId = user_cal[deleted_key]['eventId'], body = evnt).execute()
                        send_mail_to_volunteer(serviceObjMail, evnt['creator']['email'], date_, time_, user_name)
                        print("Session successfully deleted.")

                        return download_calendar_data(serviceObj, CC_ID, campus)
                    elif yes_no == 'n':
                        spinner = Halo(text="Cancelling operation, Returning to Main Menu...", spinner="dots").start()
                        user_cal, cc_cal, user_name, state = download_calendar_data(serviceObj, CC_ID, campus)
                        spinner.succeed()
                        return user_cal, cc_cal, user_name, False
            else:
                print('No Events.')
                spinner = Halo(text="Returning to Main Menu...", spinner="dots").start()
                user_cal, cc_cal, user_name, state = download_calendar_data(serviceObj, CC_ID, campus)
                sleep(2)
                spinner.succeed()
                return user_cal, cc_cal, user_name, False
    except HttpError as e:
        print(e)
        return user_cal, cc_cal, user_name, False

def find_student_in_email(cc_cal : dict, user_name : str):

    attendees_dict = {}
    attendees_bool = False
    
    for key in cc_cal.keys():
        if user_name != key[25:]:
            try:
                for email in cc_cal[key]['attendees']:
                    content =  list(email.values())
                    if f'{user_name}@student.wethinkcode.co.za' in content:
                        attendees_bool = True            
                        attendees_dict[key] = cc_cal[key]
            except KeyError as ke:
                continue

    if attendees_bool:
        return True, key[25:], user_name, attendees_dict
    else:
        return False, False, False, False
    
def send_mail_to_volunteer(srvce_email : google_api_discovery.Resource, to_volunteer : str, date_time : str,time_booked: str, user_name : str):
    """
    Send an email notification to a volunteer about a cancelled Code Clinic session.

    This function constructs and sends an email message to notify a volunteer about the cancellation
    of a booked Code Clinic session. The email includes details such as the volunteer's name, the date
    and time of the cancelled session, and a thank you message.
    """
    message = EmailMessage()

    message.set_content(f"""Good Day {to_volunteer[0:to_volunteer.index('@')]}

The session that was booked by {user_name} on {date_time} @ {time_booked} has been cancelled.

Thank You
""")
    try:
        message["To"] = to_volunteer
        message["From"] = f"{user_name}@student.wethinkcode.co.za"
        message["Subject"] = "Booked Code Clinic Session Cancelled"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        sent = srvce_email.users().messages().send(userId="me", body=create_message).execute()
        print(f"{TextColors.BOLD}{TextColors.BLUE}An Email has been sent to the Volunteer to notify them about the cancellation.{TextColors.END}{TextColors.RESET}")
        return sent
    except HttpError as e:
        print(e)