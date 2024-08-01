import googleapiclient.discovery as google_api_discovery
import datetime
import sys
from .create_data_file import slice_str
from .create_data_file import create_data_file
from .add_non_event import add_non_event_days

def download_calendar_data(serviceObject : google_api_discovery.Resource, code_clinic_id : str, campus : str) -> dict:
    """
    Download calendar data for a specified number of days from the current date.

    Args:
    - serviceObject (googleapiclient.discovery.Resource): The Google Calendar service object.

    Returns:
    dict: A dictionary containing calendar data.
    """
    today = datetime.datetime.now()
    if len(sys.argv) > 1 and type(sys.argv[1]) == int:
        day_difference = datetime.timedelta(days=int(sys.argv[1]))
    else:    
        day_difference = datetime.timedelta(days=7)

    # dateRange is used as the max date, determined by today + timedelta(days=x)
    # x representing the number of days we have to download.
    dateRange = today + day_difference
    today = f'{datetime.datetime.now().date()}T00:00:00+02:00'
    max_date = f'{dateRange.date()}T00:00:00+02:00'
    primary_obj = serviceObject.events().list(
        calendarId = 'primary',
        timeMin = today,
        timeMax = max_date,
        singleEvents=False,
        ).execute()
    
    code_clinic_obj = serviceObject.events().list(
        calendarId = code_clinic_id,
        timeMin = today,
        timeMax = max_date,
        singleEvents=False,
        ).execute()
    
    user_name = slice_str(primary_obj['summary'])
    code_clinic_dictionary = create_data_file(code_clinic_obj.get('items', []), campus)
    primary_dictionary = create_data_file(primary_obj.get('items', []), campus)
    
    # Because Google Calendar API doesn't have a days Resource,
    # a work around of finding the days that do not have a single
    # event to them and adding them to primary_dictionary was necessary
    # this is done by add_non_event_days() 
    
    if len(sys.argv) == 2 and len(primary_dictionary.keys()) < int(sys.argv[1]):
        return add_non_event_days(primary_dictionary, int(sys.argv[1])), add_non_event_days(code_clinic_dictionary, int(sys.argv[1])), user_name, True
    else:
        return add_non_event_days(primary_dictionary, 7), add_non_event_days(code_clinic_dictionary, 7), user_name, True

