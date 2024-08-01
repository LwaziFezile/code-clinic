import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from .create_config import create_config_file
from .text_colors import TextColors


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar", 'https://www.googleapis.com/auth/gmail.send']


def authorize_user():
    """
    Authorize user so they can access google calanders and 
    saves token data to .config json in the users home directory
    """

    creds = None
    home_directory = os.path.expanduser("~/.config")

    if os.path.exists(f'{home_directory}/code_clinic/token.json'):
        with open(f'{home_directory}/code_clinic/token.json', 'r') as json_file:
            data = json_file.readlines()
        if len(data) > 0:
            creds = Credentials.from_authorized_user_file(f'{home_directory}/code_clinic/token.json', SCOPES)
        elif len(data) == 0:
            # print("REQUEST NEW TOKEN")
            flow = InstalledAppFlow.from_client_secrets_file(
                "config_system/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0, authorization_prompt_message="Please allow google authorization for coding clinic application")
            create_config_file(f'{home_directory}/code_clinic/token.json', creds)
        # Save the credentials for the next run
            

    if os.path.exists(f"{home_directory}/code_clinic"):
        config_file_path = os.path.join(f'{home_directory}/code_clinic', 'token.json')
    else:
        os.mkdir(f'{home_directory}/code_clinic')
        home_directory = os.path.expanduser("~/.config/code_clinic")
        config_file_path = os.path.join(home_directory, 'token.json')
    # The file .config.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(config_file_path):
        creds = Credentials.from_authorized_user_file(config_file_path, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "config_system/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        create_config_file(config_file_path, creds)
    print(TextColors.GREEN + 'Login successful.' + TextColors.RESET)
    return creds


if __name__ == '__main__':
    authorize_user()
