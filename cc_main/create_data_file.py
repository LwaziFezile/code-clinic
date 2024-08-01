def create_data_file(items : list[dict], campus : str) -> dict:
    """
    Process a list of calendar events and create a dictionary with relevant information.

    Args:
    - items (list[dict]): A list of calendar events, each represented as 'creator' : event['creator']
    """

    data = {}
    for event in items:
        if event['status'] == 'cancelled':
            pass
        elif event['status'] == 'confirmed' and 'start' in event.keys():
            creator_slice = slice_str(event['creator']['email'])
            
            if 'date' in event['start'].keys():
                key = event['start']['date']
                if key in data.keys():
                    del data[key]
                data[key] = {
                    'summary' : event['summary'],
                    'startTime' : event['start']['date'],
                    'endTime' : event['end']['date'],
                    'creator' : event['creator'],
                    'eventId' : event['id'],
                }
                if 'location' in event.keys():
                    data[key]['location'] = event['location']
            elif 'dateTime' in event['start'].keys():   
                key = event['start']['dateTime'] + creator_slice
                if key in data.keys():
                    del data[key]
                data[key] = {
                    'summary' : event['summary'],
                    'startTime' : event['start']['dateTime'],
                    'endTime' : event['end']['dateTime'],
                    'creator' : event['creator'],
                    'eventId' : event['id'],
                }
                if 'location' in event.keys():
                    data[key]['location'] = event['location']
                if 'attendees' in event.keys():
                    attendees_slice = slice_str(event['attendees'])
                    data[key]['attendees'] = attendees_slice
    
    return data

def slice_str(string : str | list[str]) -> str | list[str]:
    if type(string) == str:
        index = string.index('@')
        string = string[0:index]
        return string
    elif type(string) == list:
        attendees = []
        for user in string:
            index = user['email'].index('@')
            string = string[0:index]
            attendees.append(string)
        return string