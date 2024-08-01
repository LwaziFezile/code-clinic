import unittest
from cc_main.book_slot_student import *



class TestBookStudent(unittest.TestCase):
    def test_is_time_valid(self):
        self.assertEqual(is_time_valid("10:00"), True)
        self.assertEqual(is_time_valid("12:00"), True)
        
    
    def test_is_time_not_valid(self):
        self.assertEqual(is_time_valid("abc"), False)
        self.assertEqual(is_time_valid("10:ccbb"),False)
        self.assertEqual(is_time_valid("10"), False)
        self.assertEqual(is_time_valid("10pm"), False)
        self.assertEqual(is_time_valid("28:00"), False)
        self.assertEqual(is_time_valid("10:00pm"), False)
    
    def test_is_date_valid(self):
        self.assertEqual(is_date_valid("28/02/2024"),True)
        self.assertEqual(is_date_valid("28/02"), True)
        self.assertEqual(is_date_valid("28-02-2024"), True)
        self.assertEqual(is_date_valid("28 Feb"), True)
        self.assertEqual(is_date_valid("28 FEBRUARY"), True)
        self.assertEqual(is_date_valid("28 FEB"), True)
        self.assertEqual(is_date_valid("28 February 2024"), True)
        
