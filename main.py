from config_system.config_system import setup_system
from googleapiclient.discovery import build
from cc_main.code_clinic_program import code_clinic_program

cred = setup_system()

serviceObject = build('calendar', 'v3', credentials = cred)
service_mail = build('gmail', 'v1', credentials = cred)


if __name__ == '__main__':
    code_clinic_program(serviceObject, service_mail)