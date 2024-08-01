import os
import googleapiclient.discovery as google_api_discovery
from .download_calendar_data import download_calendar_data
import json
from .check_data import check_calender_data
from .check_data import check_CodeClinic_data
from .display_data import *
from .book_slot_volunteer import book_slot
from .book_slot_student import book_slot_student
from .cancel_booking import remove_event
from .text_colors import TextColors
from halo import Halo

CODE_CLINIC_ID = "c_e27465c4923cd0e24cb652b0c3c52f792d8d5a11ead9dbfb6f078ac11a4be28d@group.calendar.google.com"

def code_clinic_program(serviceObject: google_api_discovery.Resource, serviceObjMail: google_api_discovery.Resource):
    user_type = input(
        "Are you logging in as a student or as a volunteer? "
    ).capitalize()

    print()
    VALID_USER_TYPES = ["Student", "Volunteer"]
    VALID_CAMPUSES = ["durban", "johannesburg", "cape town"]
    while user_type not in VALID_USER_TYPES:
        print("Invalid User Type.")
        user_type = input(
            "Are you logging in as a student or as a volunteer? "
        ).capitalize()
    campus = input(
        "Enter current WTC campus: "
    ).lower()
    print()

    while campus not in VALID_CAMPUSES:
        campus = input(
            "Invalid Campus. Enter current WTC campus you are enrolled in: "
        ).lower()

    spinner = Halo(text="Logging in", spinner="dots").start()
    user_calendar_data, code_clinic_data, userName, state = download_calendar_data(
        serviceObject, CODE_CLINIC_ID, campus
    )
    spinner.succeed(f"{TextColors.GREEN}Logged In{TextColors.RESET}")
    
    # Creating json files containing user and coding clinic data
    home_directory = os.path.expanduser("~")
    if os.path.exists(
        f"{home_directory}/.config/code_clinic/user_calendar_data.json"
    ) and os.path.exists(f"{home_directory}/.config/code_clinic/code_clinic_data.json"):
        user_calendar_data, code_clinic_data, userName = check_calender_data(
            serviceObject,
            user_calendar_data,
            home_directory,
            code_clinic_data,
            userName,
            CODE_CLINIC_ID, campus
            
        )
        user_calendar_data, code_clinic_data, userName = check_CodeClinic_data(
            serviceObject,
            user_calendar_data,
            home_directory,
            code_clinic_data,
            userName,
            CODE_CLINIC_ID, campus
            
        )
    else:
        print(f"{TextColors.YELLOW}Creating {user_type} and Code Clinic Calendar Data{TextColors.RESET}")
        with open(f"{home_directory}/.config/code_clinic/user_calendar_data.json", "w") as json_file:
            json.dump(user_calendar_data, json_file, indent=2)

        with open(f"{home_directory}/.config/code_clinic/code_clinic_data.json", "w") as json_file:
            json.dump(code_clinic_data, json_file, indent=2)
    print()

    print(f"{TextColors.PURPLE}{TextColors.BOLD}{TextColors.ITALICS}Welcome to Code Clinic. ({userName} - {user_type}){TextColors.END}{TextColors.END}{TextColors.RESET}\n")
    print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
    print(f"Select command on the table represented by a {TextColors.YELLOW}{TextColors.BOLD}number{TextColors.END}{TextColors.RESET}")
    print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
    print(command_list())
    command = input(f"{TextColors.PURPLE}>>{TextColors.RESET} ").lower()
    
    while command != "quit":
        if command not in ['1', '2', '3', '4', '5', '6', '7']:
            print("Invalid Command. Refer to the Main Menu Box")
        elif command == '1':
            print(f"{TextColors.BLUE}{TextColors.BOLD}Viewing Personal Calendar{TextColors.END}{TextColors.RESET}")
            display_user_data(user_calendar_data)
        elif command == '2':
            print(f"{TextColors.BLUE}{TextColors.BOLD}Viewing Coding Clinic Calendar{TextColors.END}{TextColors.RESET}")
            display_code_clinic(code_clinic_data)
        elif command == "3":
            if user_type == "Volunteer":
                print(f"{TextColors.BLUE}{TextColors.BOLD}Booking or Volunteering for a slot{TextColors.END}{TextColors.RESET}")
                user_calendar_data, code_clinic_data, userName, state = book_slot(
                    user_calendar_data,
                    code_clinic_data,
                    user_type,
                    serviceObject,
                    userName,
                    CODE_CLINIC_ID, campus
                )
                if state:
                    check_calender_data(
                    serviceObject,
                    user_calendar_data,
                    home_directory,
                    code_clinic_data,
                    userName,
                    CODE_CLINIC_ID, campus
                )

                check_CodeClinic_data(
                    serviceObject,
                    user_calendar_data,
                    home_directory,
                    code_clinic_data,
                    userName,
                    CODE_CLINIC_ID, campus
                )
                
            elif user_type == "Student":
                msg, campus_volunteers = code_clinic_schedule(code_clinic_data, campus)
                if campus_volunteers == False:
                    user_calendar_data, code_clinic_data, userName, state = download_calendar_data(
                    serviceObject, CODE_CLINIC_ID, campus)
                
                elif campus_volunteers:
                    print(msg)
                    user_calendar_data, code_clinic_data, userName, state = book_slot_student(serviceObject, serviceObjMail, CODE_CLINIC_ID, userName, campus)
                    if state :
                        check_calender_data(
                            serviceObject,
                            user_calendar_data,
                            home_directory,
                            code_clinic_data,
                            userName,
                            CODE_CLINIC_ID, campus
                            
                        )
                        check_CodeClinic_data(
                            serviceObject,
                            user_calendar_data,
                            home_directory,
                            code_clinic_data,
                            userName,
                            CODE_CLINIC_ID, campus
                            
                        )

            os.system('clear')
            print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
            print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
            print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
            print(command_list())
        
        elif command == "4":
            print(f"{TextColors.RED}{TextColors.BOLD}Cancelling a Booking/Slot{TextColors.END}{TextColors.RESET}")
            user_calendar_data, code_clinic_data, userName, state = remove_event(user_calendar_data,
                    code_clinic_data,
                    serviceObject, serviceObjMail,
                    userName,
                    user_type,
                    CODE_CLINIC_ID, campus)
            if state:
                check_calender_data(
                serviceObject,
                user_calendar_data,
                home_directory,
                code_clinic_data,
                userName,
                CODE_CLINIC_ID, campus
                
                )
                check_CodeClinic_data(
                serviceObject,
                user_calendar_data,
                home_directory,
                code_clinic_data,
                userName,
                CODE_CLINIC_ID, campus
                )
            
            os.system('clear')
            print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
            print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
            print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
            print(command_list())

        elif command == '5':
            if user_type == "Student":

                valid_input = ['Y', 'N']
                change_user_type = input(f"Change User Type to Volunteer? [Y/N]: ").capitalize()
                while change_user_type not in valid_input:
                    change_user_type = input("Invaild Input, Enter Y for Yes, N for No: ")
                
                if change_user_type == 'Y':
                    user_type = "Volunteer"
                    os.system('clear')
                    print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
                    print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
                    print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
                    print(command_list())
                elif change_user_type == 'N':
                    os.system('clear')
                    print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
                    print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
                    print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
                    print(command_list())

            elif user_type == 'Volunteer':
                valid_input = ['Y', 'N']
                change_user_type = input(f"Change User Type to Student? [Y/N]: ").capitalize()
                
                while change_user_type not in valid_input:
                    change_user_type = input("Invaild Input, Enter Y for Yes, N for No: ")
                if change_user_type == 'Y':
                    user_type = "Student"
                    os.system('clear')
                    print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
                    print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
                    print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
                    print(command_list())
                elif change_user_type == 'N':
                    os.system('clear')
                    print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
                    print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
                    print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
                    print(command_list())
        elif command == '6':
            campus = input(
        "Enter WTC campus, [Durban, Johannesburg, Cape Town]: "
            ).lower()
            print()
            while campus not in VALID_CAMPUSES:
                campus = input(
                    "Invalid Campus. Enter WTC campus, [Durban, Johannesburg, Cape Town]: "
                ).lower()

            os.system('clear')
            print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
            print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
            print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
            print(command_list())

        elif command == '7':
            os.system('clear')
            print(f'{TextColors.BLUE}{TextColors.BOLD}Main Menu ({userName} - {user_type}){TextColors.RESET}{TextColors.END}')
            print(f'{TextColors.PURPLE}{TextColors.BOLD}{campus.capitalize()} Campus{TextColors.RESET}{TextColors.END}')
            print(f"Type {TextColors.RED}{TextColors.BOLD}quit{TextColors.END}{TextColors.RESET} to close application")
            print(command_list())
        command = input(f"{TextColors.PURPLE}>>{TextColors.RESET} ").lower()
    spinner = Halo(text="Shutting Down...", spinner="dots").start()    
    sleep(3)
    spinner.succeed()
    os.system('clear')