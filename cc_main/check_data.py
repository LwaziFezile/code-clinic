import json
from .download_calendar_data import download_calendar_data
from .text_colors import TextColors
from halo import Halo
import googleapiclient.discovery as google_api_discovery

def check_calender_data(serviceObject : google_api_discovery.Resource, user_calendar_data : str,home_directory : str,code_clinic_data: dict, userName : str, CC_ID : str, campus : str):
    """
    Check user calendar data against local storage and update if necessary.

    This function compares the provided user calendar data with the data stored locally. If they match,
    it prints a success message indicating that the local data is up to date. If they differ, it prints
    a  message "Downloading User data to local file..."and downloads the latest user data using the provided service object. It updates
    the local storage with the new data and returns the updated calendar data, code clinic data and user name.
    """
    path_user_calendar_data = f'{home_directory}/.config/code_clinic/user_calendar_data.json'
    spinner_user = Halo(text=f'{TextColors.CYAN}Checking user data...{TextColors.RESET}', spinner="dots").start()
    
    with open(path_user_calendar_data,'r') as calender:
        calender_data = json.load(calender)
    if calender_data == user_calendar_data:
        spinner_user.succeed(f'{TextColors.GREEN}User Local data is up to date{TextColors.RESET}\n')
        return user_calendar_data, code_clinic_data, userName
    else:
        spinner_user.warn(f"{TextColors.YELLOW}User data out dated{TextColors.RESET}")
        spinner = Halo(text=f'{TextColors.CYAN}Downloading User data to local file...{TextColors.RESET}', spinner="dots").start()
        calender_data,code_clinic,username, state = download_calendar_data(serviceObject,CC_ID, campus)
        with open(path_user_calendar_data, "w+") as outfile:
            json.dump(calender_data, outfile, indent=2)
        spinner.succeed("User Data saved locally\n")
        return calender_data,code_clinic,username

def check_CodeClinic_data(serviceObject,user_calendar_data,home_directory,code_clinic_data, userName, CC_ID, campus):
    """
    This function compares the provided Code Clinic data with the data stored locally. If they match,
    it prints a success message indicating that the local data is up to date. If they differ, it prints
    a message "Downloading Code Clinic data to local file..." and downloads the latest Code Clinic data using the provided service object. It updates
    the local storage with the new data and returns the updated user calendar data, updated Code Clinic data and username.
    """
    path_code_clinic_data = f'{home_directory}/.config/code_clinic/code_clinic_data.json'
    spinner_user = Halo(text=f'{TextColors.CYAN}Checking Coding Clinic data...{TextColors.RESET}', spinner="dots").start()

    with open(path_code_clinic_data,'r') as code_clinic:
        clinic_data = json.load(code_clinic)
    if clinic_data == code_clinic_data:
        spinner_user.succeed(f'{TextColors.GREEN}Code Clinic local data is up to date{TextColors.RESET}\n')
        
        return user_calendar_data, clinic_data, userName
    else:
        spinner_user.warn(f"{TextColors.YELLOW}Coding Clinic data out dated{TextColors.RESET}")
        spinner = Halo(text=f'{TextColors.CYAN}Downloading Code Clinic data to local file...{TextColors.RESET}', spinner="dots").start()
        
        calender_data,clinic_data,username, state = download_calendar_data(serviceObject,CC_ID, campus)
        with open(path_code_clinic_data, "w+") as outfile:
            json.dump(clinic_data, outfile, indent=2)
        spinner.succeed(f'{TextColors.GREEN}Coding Clinic Data saved locally{TextColors.RESET}\n')

        return calender_data,clinic_data,username









