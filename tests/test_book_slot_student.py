import unittest
import json
from unittest.mock import patch, MagicMock
import os
from cc_main.book_slot_student import book_slot_student

class TestBookSlotStudentFunction(unittest.TestCase):

    def setUp(self):
        home_dir = os.path.expanduser('~')
        path_user_calendar_data = f'{home_dir}/student_work/dbn_23_code_clinics/tests/user_calendar_data.json'
        path_code_clinic_data = f'{home_dir}/student_work/dbn_23_code_clinics/tests/code_clinic_data.json'

        with open(path_user_calendar_data,'r') as calender:
            calender_data = json.load(calender)
        with open(path_code_clinic_data,'r') as code_clinic:
            clinic_data = json.load(code_clinic)
        
        self.mock_service = MagicMock()
        self.cc_id = MagicMock()
        self.mock_service_email = MagicMock()
        self.user_cal = calender_data  
        self.cc_cal = clinic_data    

    @patch('builtins.input', side_effect=['01 Mar', '15:00', '10'])
    def test_book_event_student(self, mock_input):
        user_name = 'lluswazi023'
        campus = 'durban'
        book_slot_student(self.mock_service, self.mock_service_email, self.cc_cal, user_name, campus)
        self.mock_service.events().update.assert_not_called()