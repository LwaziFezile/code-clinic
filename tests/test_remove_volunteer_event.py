import unittest
import json
from unittest.mock import patch, MagicMock
import builtins
import os
from cc_main.cancel_booking import remove_event

class TestRemoveEventFunction(unittest.TestCase):
    
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
        self.user_cal = calender_data  # Your sample user calendar data
        self.cc_cal = clinic_data    # Your sample coding clinic calendar data

    @patch('builtins.input', side_effect=['2024-03-01', '15:00', 'durban', 'y'])
    def test_remove_event_volunteer(self, mock_input):
        
        user_name = 'lluswazi023'
        user_type = 'Volunteer'
        campus = 'durban'

        remove_event(self.user_cal, self.cc_cal, self.mock_service, self.mock_service_email, user_name, user_type, self.cc_id,campus)
        self.mock_service.events().delete.assert_called_with(calendarId='primary', eventId='2ugqj7u888dlt58ao6ok558dmc')
    @patch('builtins.input', side_effect=['2024-03-01', '15:00', 'durban', 'n'])
    def test_remove_event_volunteer_cancelled_operation(self, mock_input):
        
        user_name = 'lluswazi023'
        user_type = 'Volunteer'
        campus = 'durban'

        remove_event(self.user_cal, self.cc_cal, self.mock_service, self.mock_service_email, user_name, user_type, self.cc_id,campus)
        self.mock_service.events().delete.assert_not_called()
        # self.mock_service.events().delete.assert_called_with(calendarId='primary', eventId='2ugqj7u888dlt58ao6ok558dmc')       

if __name__ == '__main__':
    unittest.main()
