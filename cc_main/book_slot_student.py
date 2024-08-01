# imports for standard library modules
from datetime import datetime

# imports for third-party modules
import googleapiclient.discovery as google_api_discovery
from googleapiclient.errors import HttpError
from halo import Halo
import emoji
from time import sleep

# email imports
import base64
from email.message import EmailMessage

from .download_calendar_data import download_calendar_data
from .display_data import topics_list

# imports for local modules
from cc_main.text_colors import TextColors

DAYS = {
    1: 31,
    2: 29,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}


MONTHS = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def book_slot_student(service, serviceObjMail, cc_calendar_id, user_name, campus):
    """
    Book a slot for a student to attend a coding clinic session.

    Args:
    - service: Google Calendar service object.
    - serviceObjMail: Service object for sending emails.
    - cc_calendar_id: ID of the coding clinic calendar.
    - user_name: Name of the student booking the slot.
    - campus: Campus location of the student.

    Returns:
    - user_cal: User's calendar.
    - cc_cal: Coding clinic calendar.
    - userName: User's name.
    - campus: campus of the booking student.

    Raises:
    - ValueError: If an invalid input is provided.
    - IOError: If there is an issue accessing the calendars or sending the email.
    """

    volunteer_events = get_events(service, cc_calendar_id)

    location_found = False

    for event in volunteer_events:
        if campus in event["location"].lower() and "attendees" not in event.keys():
            location_found = True
    if location_found:

        date = input_date("Enter date of booking in (DD-MM) format, eg 14 Mar:\n")
        if date.capitalize() == "Menu":
            spinner = Halo(
                text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...",
                spinner="dots",
            ).start()

            user_cal, cc_cal, userName, state = download_calendar_data(
                service, cc_calendar_id, campus
            )
            spinner.succeed()
            return user_cal, cc_cal, userName, state
        time_booked = input_time("Enter time of booking in (HH:MM) format:\n")

        if time_booked.capitalize() == "Menu":
            spinner = Halo(
                text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...",
                spinner="dots",
            ).start()

            user_cal, cc_cal, userName, state = download_calendar_data(
                service, cc_calendar_id, campus
            )
            spinner.succeed()
            return user_cal, cc_cal, userName, state

        date_time = split_datetime(date, time_booked, MONTHS)
        booked_datetime = convert_to_iso(*date_time)
        cc_events = get_events(service, cc_calendar_id)
        volunteer_primary_id = get_volunteer_calendar_id(cc_events, booked_datetime)
        
        for event in cc_events:
            if event["creator"]:
                vol_name = event["creator"]["email"][
                    0 : event["creator"]["email"].index("@")
                ]
            else:
                spinner = Halo(
                    text=f"{TextColors.ITALICS}{TextColors.END}No Available Volunteers. Returning to Main Menu...",
                    spinner="dots",
                ).start()
                user_cal, cc_cal, userName, state = download_calendar_data(
                    service, cc_calendar_id, campus
                )
                spinner.fail()
                return download_calendar_data(service, cc_calendar_id, campus)

        if is_slot_available(cc_events, booked_datetime, user_name):
            description = input(
                f"Enter Number corresponding with the topic you need help with:\n{topics_list()}\n >> "
            )
            
            if description.capitalize() == "Menu":
                spinner = Halo(
                    text=f"{TextColors.ITALICS}{TextColors.END}Returning to Main Menu...",
                    spinner="dots",
                ).start()
                user_cal, cc_cal, userName, state = download_calendar_data(
                    service, cc_calendar_id, campus
                )
                spinner.fail()
                return download_calendar_data(service, cc_calendar_id, campus)
            if description == "1":
                description = "Data Types and Variables"
            elif description == "2":
                description = "Operators"
            elif description == "3":
                description = "Control Structures (IF statements, Loops)"
            elif description == "4":
                description = "Basic Data Structures"
            elif description == "5":
                description = "Functions"
            elif description == "6":
                description = "Modules and Packages"
            elif description == "7":
                description = "File Handling"
            elif description == "8":
                description = "Error and Exception Handling"
            elif description == "9":
                description = "Classes and Object-Oriented Programming (OOP)"
            elif description == "10":
                description = "Regular Expressions"
            else:
                spinner = Halo(
                text=f"{TextColors.ITALICS}{TextColors.END}Invalid Topic. Returning to Main Menu...",
                spinner="dots",
                ).start()
                user_cal, cc_cal, userName, state = download_calendar_data(
                    service, cc_calendar_id, campus
                )
                sleep(2)
                spinner.fail()
                return user_cal, cc_cal, userName, False
            spinner = Halo(
                text=f"Booking a coding clinic session with {vol_name}. Topic: {description}",
                spinner="dots",
            )
            
            spinner.start()
            # update code clinics calendar
            update_event(
                service,
                cc_events,
                booked_datetime,
                description,
                cc_calendar_id,
                user_name,
            )

            spinner.succeed("Successfully booked slot")
            user_cal, cc_cal, userName, state = download_calendar_data(
                service, cc_calendar_id, campus
            )
            send_mail_to_volunteer(
                serviceObjMail,
                volunteer_primary_id,
                description,
                date,
                time_booked,
                user_name,
            )
            print()
            user_cal, cc_cal, userName, state = download_calendar_data(
                service, cc_calendar_id, campus
            )
            return user_cal, cc_cal, userName, state
        else:
            user_cal, cc_cal, userName, state = download_calendar_data(
                service, cc_calendar_id, campus
            )
            return user_cal, cc_cal, userName, state
    else:
        spinner = Halo(
            text=f"{TextColors.ITALICS}{TextColors.END}There are no available volunteers at your campus. Returning to Main Menu...",
            spinner="dots",
        ).start()
        user_cal, cc_cal, userName, state = download_calendar_data(
            service, cc_calendar_id, campus
        )
        sleep(2)
        spinner.fail()
        return user_cal, cc_cal, userName, state


def get_volunteer_calendar_id(code_clinic_events, user_datetime):
    """
    Retrieve the email address of the volunteer associated with a specific event datetime.

    Parameters:
    - code_clinic_events (list): List of events from the code clinics calendar.
    - user_datetime (str): Datetime string entered by the user.

    Returns:
    - str: Email address of the volunteer associated with the specified event datetime.

    Note:
    - This function iterates through the code clinics events to find the event matching the user datetime.
    - Once found, it retrieves the email address of the volunteer associated with that event.
    - The email address serves as the ID for the volunteer's primary calendar.

    Example Usage:
    ```python
    volunteer_calendar_id = get_volunteer_calendar_id(code_clinic_events, user_datetime)
    ```

    """
    for event in code_clinic_events:
        if event["start"]["dateTime"].split("+")[0] == user_datetime:
            return event["creator"]["email"]


def get_events(serviceObject, calendar_id):
    """
    Retrieve upcoming events from a specific calendar using the Google Calendar API.

    Parameters:
    - serviceObject: An authenticated Google Calendar service object.
    - calendar_id (str): The ID of the calendar from which to retrieve events.

    Returns:
    - events (list): A list of upcoming events from the specified calendar.

    Note:
    - This function queries the Google Calendar API to fetch upcoming events.
    - It retrieves events starting from the current UTC time up to the next 7 events.
    - Events are sorted by their start time.

    Raises:
    - HttpError: If an error occurs while accessing the Google Calendar API.
    """
    try:
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            serviceObject.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=7,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
    except HttpError as error:
        print(f"An error occurred: {error}")
    return events


def is_slot_available(events, user_datetime, user_name):
    """
    Check if a slot is available for booking based on provided events, user datetime, and user name.

    Parameters:
    - events (list): List of events to check availability against.
    - user_datetime (str): Datetime string of the user's desired slot.
    - user_name (str): Name of the user.

    Returns:
    - bool: True if the slot is available; False otherwise.

    Note:
    - The function iterates through the provided events to identify booked and available dates.
    - It also checks if the user is trying to book a slot where they are the volunteer.
    - Returns True if the slot is available, False otherwise.

    Example Usage:
    ```python
    is_available = is_slot_available(events, user_datetime, user_name)
    """

    booked_dates = []
    available_dates = []

    for event in events:
        event_datetime = event["start"].get("dateTime")
        if "Booked" in event["summary"]:
            booked_dates.append(event_datetime.split("+")[0])
        elif "Available" in event["summary"]:
            available_dates.append(event_datetime.split("+")[0])
    if user_name in event["creator"]["email"]:
        print(emoji.emojize(":x:", language="alias"), end=" ")
        print(
            TextColors.RED
            + "You cannot book a slot where you are the volunteer!"
            + TextColors.RESET
        )
        return False
    if user_datetime in booked_dates:
        print(emoji.emojize(":x:", language="alias"), end=" ")
        print(TextColors.RED + "slot is already booked!" + TextColors.RESET)
        return False
    elif user_datetime in available_dates:
        return True
    else:
        print(emoji.emojize(":x:", language="alias"), end=" ")
        print(TextColors.RED + "slot is unavailable!" + TextColors.RESET)
        print(
            TextColors.YELLOW
            + "A slot can only be booked if there is a volunteer allocated to it."
            + TextColors.RESET
        )
        return False


def input_time(prompt):
    """
    Prompt the user to input a valid time.

    Parameters:
    - prompt (str): The prompt message to display to the user.

    Returns:
    - str: Valid time entered by the user in 'HH:MM' format or 'Menu' if the user wants to return to the main menu.

    Note:
    - This function continuously prompts the user to enter a time in 'HH:MM' format until a valid time is entered.
    - It allows the user to enter 'Menu' to return to the main menu.
    - It relies on the helper function `is_time_valid` to validate the entered time.

    Example Usage:
    ```python
    time_input = input_time("Enter time in 'HH:MM': ")
    """
    while True:
        booked_time = input(prompt)
        if booked_time.capitalize() == "Menu":
            return booked_time
        if is_time_valid(booked_time):
            break
    return booked_time


def date_separator(date):
    separator = None
    if "/" in date:
        separator = "/"
    elif "-" in date:
        separator = "-"
    elif " " in date:
        separator = " "
    return separator


def is_time_valid(time):
    """
    Check if a given time is valid for booking a slot.

    Parameters:
    - booked_time (str): The time to be validated in 'HH:MM' format.

    Returns:
    - bool: True if the time is valid; False otherwise.

    Note:
    - This function checks if the provided time is in the correct format and falls within the valid booking hours and intervals.
    - The code clinic closes at 5:00 PM, and slots are available every 30 minutes.
    - If the time is valid, it returns True. Otherwise, it prints an error message and returns False.

    Example Usage:
    ```python
    is_valid = is_time_valid("14:30")
    ```
    """

    if ":" not in time:
        return False
    hour, minute = time.split(":")[:2]

    if hour.isdecimal() and minute.isdecimal():
        minute = int(minute)
        hour = int(hour)

        # Check if the time falls within a valid range code clinic closes at 5 and 30 min a session
        if hour > 0 and hour < 17 and minute == 0 or minute == 30:
            return True

    return False


def input_date(prompt):
    """
    Prompt the user to input a valid date.

    Parameters:
    - prompt (str): The prompt message to display to the user.

    Returns:
    - str: Valid date entered by the user in 'yyyy-mm-dd' format or 'Menu' if the user wants to return to the main menu.

    Note:
    - This function continuously prompts the user to enter a date in 'yyyy-mm-dd' format until a valid date is entered.
    - It allows the user to enter 'Menu' to return to the main menu.
    - It relies on the helper function `is_date_valid` to validate the entered date.

    Example Usage:
    ```python
    date_input = input_date("Enter date in 'yyyy-mm-dd' format: ", MONTHS)
    ```
    """
    while True:
        date = input(prompt)
        if date.capitalize() == "Menu":
            return date
        if is_date_valid(date):
            break
        print(TextColors.RED + "Invalid Date" + TextColors.RESET)
    return date


def is_date_valid(date):
    """
    Check if a given date is valid.

    Parameters:
    - date (str): The date to be validated.
    - MONTHS (list): List of valid month names.

    Returns:
    - bool: True if the date is valid; False otherwise.

    Note:
    - This function checks if the provided date is in the correct format and corresponds to a valid month and day.
    - It splits the date string to extract the month and day components.
    - It validates the month against the provided list of valid month names.
    - It checks if the day is a valid number (less than 31).
    - If the date is valid, it returns True. Otherwise, it prints an error message and returns False.

    Example Usage:
    ```python
    is_valid = is_date_valid("2024-03-01", MONTHS)
    ```
    """

    sep = date_separator(date)

    if sep is not None:
        day, month = date.split(sep)[:2]

        if day.strip().isdecimal():
            day = int(day)

        if month.strip().isdecimal():
            month = int(month)
        else:
            month = MONTHS.get(month.capitalize()[:3], None)

        # check if month is in valid range
        if month is not None and month > 0 and month <= 12:
            days = DAYS.get(month, None)
            # check if days is in valid range
            if day > 0 and day <= days:
                return True
    return False


def update_event(service, events, user_datetime, description, calendar_id, user_name):
    """
    Update a specific event in the calendar with booking details.

    Parameters:
    - service: Google Calendar service object.
    - events (list): List of events to search for the event to update.
    - user_datetime (str): Datetime string entered by the user.
    - description (str): Description of the session required by the student.
    - calendar_id (str): ID of the calendar containing the event to be updated.
    - user_name (str): Name of the user.

    Returns:
    - None

    Note:
    - This function retrieves the event ID corresponding to the provided datetime from the list of events.
    - It then retrieves the student's email address and updates the event details.
    - The event summary and description are modified to reflect the booking details.
    - The student and volunteer are added as attendees with 'accepted' response status.
    - If an error occurs during the update process, it prints an error message.

    Example Usage:
    ```python
    update_event(service, events, user_datetime, description, calendar_id, user_name)
    ```
    """
    event_id = ""
    for event in events:
        if event["start"]["dateTime"].split("+")[0] == user_datetime:
            event_id = event["id"]

    # get calendar list to get students email address
    primary_calendar = service.calendarList().get(calendarId="primary").execute()
    student_email = primary_calendar["id"]

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        vol_name = event["creator"]["email"]
        event["summary"] = (
            f"Booked Coding Clinic Session with {vol_name[0:vol_name.index('@')]}"
        )
        event["description"] = (
            f"{student_email.split('@')[0][:-3]} has booked a coding clinic session requiring assistance with {description}"
        )
        event["attendees"] = [
            {"email": event["creator"]["email"], "responseStatus": "accepted"},
            {"email": student_email, "self": True, "responseStatus": "accepted"},
        ]
        updated_event = (
            service.events()
            .update(calendarId=calendar_id, eventId=event["id"], body=event)
            .execute()
        )
    except HttpError as error:
        print(f"An error occurred: {error}")


def convert_to_iso(day, month, hours, minutes):
    """
    Convert the given date and time components to ISO 8601 format.

    Parameters:
    - day (int): The day of the month.
    - month (int): The month of the year.
    - hours (int): The hour component of the time.
    - minutes (int): The minute component of the time.

    Returns:
    - str: The ISO 8601 formatted datetime string.

    Note:
    - This function constructs a datetime object using the provided components and the current year.
    - It then returns the ISO 8601 formatted string representation of the datetime object.

    Example Usage:
    ```python
    iso_datetime = convert_to_iso(1, 3, 12, 30)
    """
    year = datetime.now().year
    user_datetime = datetime(
        year, month, int(day), hour=int(hours), minute=int(minutes)
    )
    return user_datetime.isoformat()


def date_separator(date):
    separator = None
    if "/" in date:
        separator = "/"
    elif "-" in date:
        separator = "-"
    elif " " in date:
        separator = " "
    return separator


def split_datetime(date, time, MONTHS):
    """
    Split the date and time components and convert them to appropriate data types.

    Parameters:
    - date (str): The date string to be split.
    - time (str): The time string to be split.
    - MONTHS (dict): Dictionary mapping month names to their numeric representations.

    Returns:
    - tuple: A tuple containing day, month, hours, and minutes components.

    Note:
    - This function splits the date string into day and month components.
    - It converts the month to its numeric representation using the provided MONTHS dictionary.
    - It splits the time string into hours and minutes components.
    - It returns a tuple containing the day, month, hours, and minutes components.

    Example Usage:
    ```python
    day, month, hours, minutes = split_datetime("01/03", "12:30", MONTHS)
    ```
    """
    sep = date_separator(date)
    date = date.split(sep)
    month = date[1][1] if date[1].startswith("0") else date[1]
    month = month = int(month) if month.isdecimal() else month.capitalize()[:3]
    day = date[0]
    hours, minutes = time.split(":")
    if type(month) == str:
        month = MONTHS[month.capitalize()[:3]]
    return (day, month, hours, minutes)


def send_mail_to_volunteer(
    srvce_email: google_api_discovery.Resource,
    to_volunteer: str,
    descrpt: str,
    date_time: str,
    time_booked: str,
    user_name: str,
):
    """
    Send an email notification to the volunteer about the booked session.

    Parameters:
    - srvce_email (google_api_discovery.Resource): Google service object for sending emails.
    - to_volunteer (str): Email address of the volunteer.
    - descrpt (str): Description of the booked session.
    - date_time (str): Date of the booked session.
    - time_booked (str): Time of the booked session.
    - user_name (str): Name of the user booking the session.

    Returns:
    - dict: Details of the sent email.

    Note:
    - This function constructs an email message with details about the booked session.
    - It sends the email to the volunteer using the provided service object.
    - The email contains information about the session topic, date, and time.
    - It prints a notification after sending the email.

    Example Usage:
    ```python
    sent_email = send_mail_to_volunteer(srvce_email, to_volunteer, descrpt, date_time, time_booked, user_name)
    ```
    """
    message = EmailMessage()

    message.set_content(
        f"""Good Day {to_volunteer[0:to_volunteer.index('@')]}

The session that you booked has a Student.

Topic: {descrpt}

The time for this session is {date_time} @ {time_booked}

Thank You
"""
    )
    try:
        message["To"] = to_volunteer
        message["From"] = f"{user_name}@student.wethinkcode.co.za"
        message["Subject"] = "Code Clinic Booked Session"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        sent = (
            srvce_email.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(
            f"{TextColors.BOLD}{TextColors.BLUE}An Email has been sent to the Volunteer to notify them about the booking.{TextColors.END}{TextColors.RESET}"
        )
        return sent
    except HttpError as e:
        print(e)
