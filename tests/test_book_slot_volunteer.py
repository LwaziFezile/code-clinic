import unittest
import json
from unittest.mock import patch, MagicMock
import builtins
import os
from cc_main.book_slot_volunteer import book_slot

class TestBookEventFunction(unittest.TestCase):

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

    @patch('builtins.input', side_effect=['2024-03-02', '15:00'])
    def test_book_event_volunteer(self, mock_input):
        
        user_name = 'lluswazi023'
        user_type = 'Volunteer'
        campus = 'durban'

        book_slot(self.user_cal, self.cc_cal, user_type, self.mock_service, user_name, self.cc_id, campus)
        self.mock_service.events().insert.assert_called()
    
    
    @patch('builtins.input', side_effect=['2024-03-01', '15:00'])
    def test_book_event_volunteer_duplicate(self, mock_input):
        
        user_name = 'lluswazi023'
        user_type = 'Volunteer'
        campus = 'durban'

        book_slot(self.user_cal, self.cc_cal, user_type, self.mock_service, user_name, self.cc_id, campus)
        self.mock_service.events().insert.assert_not_called()