import unittest
from unittest.mock import patch
import sys
from cc_main.book_slot_student import *
from config_system.config_system import setup_system
from main import code_clinic_program, build,cred

cred = setup_system()
serviceObject = build('calendar', 'v3', credentials = cred)
service_mail = build('gmail', 'v1', credentials = cred)


class TestMyFunction(unittest.TestCase):

    @patch('builtins.input', side_effect=['student','Durban', '1', 'quit'])
    def test_update_event(self, mock_input):
        code_clinic_program(serviceObject, service_mail)

if __name__ == '__main__':
    unittest.main()