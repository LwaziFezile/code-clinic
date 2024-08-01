import datetime
def add_non_event_days(event_dates : list[dict], difference : int) -> dict:
    """
    Add non-event days to a dictionary of event dates.

    Args:
    - event_dates (dict): A dictionary containing event dates as keys.
        Each key represents a date string, and the values are dictionaries with event details.
    - difference (int): The desired number of non-event days to add.

    Returns:
    dict: An updated dictionary with additional non-event days.
        The keys are date strings, and the values are either dictionaries with event details or the string "No Events".

    Note:
    This function adds non-event days to the input dictionary until the specified 'difference' is reached.
    It checks for existing event dates and ensures that non-event days do not conflict with existing events.
    """
    now = datetime.datetime.now().date()
    date_format_no_time = '%Y-%m-%d'
    x_days = [datetime.datetime.strftime(now + datetime.timedelta(x), date_format_no_time) for x in range(difference)]

    for item in x_days:
        found_date = False
        for key in event_dates.keys():
            if item in event_dates.keys():
                found_date = True
                break
            elif f'{item}T' in key:
                found_date = True
                break
        if found_date == False:
            event_dates[item] = {
                "summary": "N/A",
                "startTime": "N/A",
                "endTime": "N/A",
                'creator' : "N/A",
                'campus' : "N/A"
                }
        else:
            found_date = False
    return event_dates