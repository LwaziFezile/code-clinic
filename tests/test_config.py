import unittest
import os.path
from config_system import oauth_user

class TestConfig(unittest.TestCase):
    
    def test_create_config_file(self):
        creds = oauth_user.authorize_user()
        config_file_path = os.path.expanduser('~')
        result = os.path.exists(f"{config_file_path}/.config/code_clinic/token.json")
        self.assertTrue(result)

    def test_creds(self):
        creds = oauth_user.authorize_user()
        self.assertNotEqual(creds, None)

    def test_creds_valid(self):
        creds = oauth_user.authorize_user()
        self.assertEqual(creds.valid,True)