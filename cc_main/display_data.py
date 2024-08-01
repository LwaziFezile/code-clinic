from prettytable import PrettyTable
from .text_colors import TextColors
from prettytable.colortable import ColorTable, Themes
import datetime
from halo import Halo
from time import sleep
def display_user_data(user_calendar: dict) -> None:
    """
    Display calendar data in a PrettyTable format.

    Args:
    - user_calendar (dict): The user's calendar data.
    - code_clinic_calendar (dict): The Code Clinic calendar data.

    Returns:
    None
    """
    datetime_now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+02:00'), '%Y-%m-%dT%H:%M:%S+02:00')
    

    # Create a PrettyTable
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)
    # Set column names
    table.field_names = ["Date", "Summary", "Campus", "Start Time", "End Time"]
    counter = 0
    # Populate the table with user_calendar data
    for event_id in user_calendar.keys():
        event_info = user_calendar[event_id]
        if event_info['startTime'] != "N/A":
            event_datetime = datetime.datetime.strptime(event_info['startTime'], '%Y-%m-%dT%H:%M:%S+02:00')
        if event_info["startTime"] == "N/A" and event_info["summary"] == "N/A" and event_info["endTime"] == "N/A":
            counter += 1
            continue
        elif datetime_now > event_datetime:
            continue
        try:
            if 'durban' in event_info['location'].lower():
                event_location = "Durban"
            elif 'johannesburg' in event_info['location'].lower():
                event_location = "Johannesburg"
            elif 'cape town' in event_info['location'].lower():
                event_location = 'Cape Town'
            table.add_row([event_info["startTime"][0:10],
                        event_info["summary"],
                        event_location,
                        event_info["startTime"][11:16],
                        event_info["endTime"][11:16]], divider=True)
        except KeyError as ke:
            table.add_row([event_info["startTime"][0:10],
            event_info["summary"],
            'N/A',
            event_info["startTime"][11:16],
            event_info["endTime"][11:16]], divider=True)
    
    # Print user table
    if counter == len(user_calendar.keys()):
        spinner = Halo(text="No future events in the Coding Clinic calendar. Returning to Main Menu...", spinner="dots").start()
        
        sleep(2)
        return spinner.succeed()
    print(table)

def display_code_clinic(code_clinic_calendar: dict):
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)
    counter = 0
    datetime_now = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+02:00'), '%Y-%m-%dT%H:%M:%S+02:00')
    table.field_names = ["Date", "Summary", 'Campus', "Start Time", "End Time"]
    # Populate the table with code_clinic_calendar data
    for event_id in code_clinic_calendar.keys():
        event_info = code_clinic_calendar[event_id]
        if event_info['startTime'] != "N/A":
            event_datetime = datetime.datetime.strptime(event_info['startTime'], '%Y-%m-%dT%H:%M:%S+02:00')
        if event_info["startTime"] == "N/A" and event_info["summary"] == "N/A" and event_info["endTime"] == "N/A":
            counter += 1
            continue
        elif datetime_now > event_datetime:
            continue
        if 'durban' in event_info['location'].lower():
            event_location = "Durban"
        elif 'johannesburg' in event_info['location'].lower():
            event_location = "Johannesburg"
        elif 'cape town' in event_info['location'].lower():
            event_location = 'Cape Town'
        table.add_row([event_info["startTime"][0:10],
                       event_info["summary"],
                       event_location,
                       event_info["startTime"][11:16],
                       event_info["endTime"][11:16]], divider=True)
    
    # Print Code Clinic table
    if counter == len(code_clinic_calendar.keys()):
        spinner = Halo(text="No future events in the Coding Clinic calendar. Returning to Main Menu...", spinner="dots").start()
        
        sleep(2)
        return spinner.succeed()
    print(table)
    # return table

def command_list():
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)
    table.add_column("Coding Clinic Commands", [
        f'{TextColors.YELLOW}[{TextColors.END}1{TextColors.YELLOW}]{TextColors.END} View Personal Calendar',f'{TextColors.YELLOW}[{TextColors.END}2{TextColors.YELLOW}]{TextColors.END} View Coding Clinic Calendar', 
        f'{TextColors.YELLOW}[{TextColors.END}3{TextColors.YELLOW}]{TextColors.END} Book or Volunteer for a Slot',
        f'{TextColors.YELLOW}[{TextColors.END}4{TextColors.YELLOW}]{TextColors.END} Cancel a slot',
        f'{TextColors.YELLOW}[{TextColors.END}5{TextColors.YELLOW}]{TextColors.END} Change User Type',
        f'{TextColors.YELLOW}[{TextColors.END}6{TextColors.YELLOW}]{TextColors.END} Change Campus',
        f'{TextColors.YELLOW}[{TextColors.END}7{TextColors.YELLOW}]{TextColors.END} Clear Terminal']
        ,"l", "t")
    print(f'{TextColors.GREEN}NOTE{TextColors.RESET}: Type {TextColors.BLUE}{TextColors.ITALICS}Menu{TextColors.END}{TextColors.RESET} from any operation to go back to Main Menu')
    return table
    
def topics_list():
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)
    table.add_column("Coding Clinic Commands", [
        f'{TextColors.YELLOW}[{TextColors.END}1{TextColors.YELLOW}]{TextColors.END} Data Types and Variables',f'{TextColors.YELLOW}[{TextColors.END}2{TextColors.YELLOW}]{TextColors.END} Operators', 
        f'{TextColors.YELLOW}[{TextColors.END}3{TextColors.YELLOW}]{TextColors.END} Control Structures (IF statements, Loops)',
        f'{TextColors.YELLOW}[{TextColors.END}4{TextColors.YELLOW}]{TextColors.END} Basic Data Structures',
        f'{TextColors.YELLOW}[{TextColors.END}5{TextColors.YELLOW}]{TextColors.END} Functions',
        f'{TextColors.YELLOW}[{TextColors.END}6{TextColors.YELLOW}]{TextColors.END} Modules and Packages',
        f'{TextColors.YELLOW}[{TextColors.END}7{TextColors.YELLOW}]{TextColors.END} File Handling',
        f'{TextColors.YELLOW}[{TextColors.END}8{TextColors.YELLOW}]{TextColors.END} Error and Exception Handling',
        f'{TextColors.YELLOW}[{TextColors.END}9{TextColors.YELLOW}]{TextColors.END} Classes and Object-Oriented Programming (OOP)',
        f'{TextColors.YELLOW}[{TextColors.END}10{TextColors.YELLOW}]{TextColors.END} Regular Expressions'
        ], "l", "t")
    return table


def code_clinic_schedule(cc_dict : dict, campus : str):
    """
    Generate and display the Code Clinic schedule for today.

    Parameters:
    - cc_dict (dict): A dictionary containing the Code Clinic schedule.

    Returns:
    - str or PrettyTable: If there are no volunteers available, returns
      "No Volunteers Available". Otherwise, returns a PrettyTable object
      displaying the schedule for the available time slots.

    The function extracts today's events from the provided Code Clinic schedule
    and formats them into a PrettyTable for easy display. The table includes
    available time slots and indicates if they are booked or available for
    volunteering.

    Example:
    cc_dict = {'2023-01-17T09:00:00Z': {'attendees': ['volunteer1']},
               '2023-01-17T10:00:00Z': {'attendees': ['volunteer2']},
               '2023-01-17T11:00:00Z': {}}
    code_clinic_schedule(cc_dict)
    """
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)
    now = datetime.datetime.now().date()
    table.field_names = ["Date", "Volunteer Username", 'Campus', "Start Time"]
    today_events = [x for x in cc_dict.keys()]
    
    today_time_slots = [[x[11:16], x] for x in today_events if len(x) > 10]
    # print(cc_dict.keys())
    booked_slot = 0
    different_location = 0
    if today_time_slots == []:
        spinner = Halo(text=f"{TextColors.ITALICS}{TextColors.END}No Coding Clinic events available. Returning to Main Menu...", spinner="dots").start()
        sleep(2)
        spinner.succeed()
        return f"{TextColors.ITALICS}No Volunteers Available{TextColors.END}", False
    else:
        for time in today_time_slots:
            for event in today_events:
                if time[0] in event:
                    try:
                        if campus not in cc_dict[event]['location'].lower() :
                            different_location += 1
                            pass
                        elif "attendees" in cc_dict[event].keys():
                            booked_slot += 1
                            pass       
                        else:
                            if 'durban' in cc_dict[event]['location'].lower():
                                event_location = "Durban"
                            elif 'johannesburg' in cc_dict[event]['location'].lower():
                                event_location = "Johannesburg"
                            elif 'cape town' in cc_dict[event]['location'].lower():
                                event_location = 'Cape Town'
                            
                            table.add_row([
                                time[1][0:10],
                                time[1][25:],
                                event_location,
                                time[0]], divider=True)
                            break
                    except KeyError as ke:
                        return f"{TextColors.ITALICS}Please contact admin: display_data.py\n\n{ke}\n{TextColors.END}", False
                
        
        if booked_slot == len(today_time_slots) or different_location == len(today_time_slots):
            spinner = Halo(text=f"{TextColors.ITALICS}No Available Volunteers in your campus.{TextColors.END} Returning to Main Menu...", spinner="dots").start()
            spinner.fail()
            return sleep(2), False
        print(f"{TextColors.BLUE}{TextColors.BOLD}Available Coding Clinic Volunteers - {campus} campus{TextColors.END}{TextColors.RESET}")
        return table, True
    
def generate_calendar_table(calendar_dict : dict) -> PrettyTable:
    table = PrettyTable()
    table = ColorTable(theme=Themes.OCEAN)
    
    try:
        calendar_dict_field_name = ['Date', 'Summary', 'Start Time', 'End Time', 'Campus']

        table.field_names = calendar_dict_field_name
        
        # Runs only when the command to display it is input
        # Removing Both creator and attendees value or only creator value 
        # from field names and when inserting a row.
        # ValueError if there is an event made on the google calendar web/mobile app
        # Consider including a try catch statement for that possibility
        for i in calendar_dict:
            insert_row = []
            for x in range(3):
                insert_row.append(list(calendar_dict[i].values())[x])
            # print(list(calendar_dict[i].values()))
            if 'durban' in calendar_dict[i]['location'].lower():
                insert_row.append('Durban')
            elif 'johannesburg' in calendar_dict[i]['location'].lower():
                insert_row.append('Johannesburg')
            elif 'cape town' in calendar_dict[i]['location'].lower():
                insert_row.append('Cape Town')
            if insert_row[0] != 'N/A':
                insert_row[1] = insert_row[1][11:16]
                insert_row[2] = insert_row[2][11:16]
                insert_row.insert(0, i[0:10])
                table.add_row(insert_row, divider=True)
    except ValueError as ve:
        return f"Please contact admin.\n{ve}"
    
    return table