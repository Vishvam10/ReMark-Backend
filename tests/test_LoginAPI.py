import sys
import unittest
import logging
import requests

class TokenApiTest(unittest.TestCase):
        
    BASE_API_URL = "http://127.0.0.1:5000/api"
    LOGIN_API_URL = "{}/login".format(BASE_API_URL)
    
    LOGIN_USER_DATA = {
        "username" : "testing_user",
        "password" : "testing123",
        "authority" : "user"
    }

    INCORRECT_LOGIN_USER_DATA = []

    ALLOWED_ERRORS = ["Email ID is required", "Password is required", "Username is required", "Authority is incorrectly specified", "Duplicate user"]

    for k, v in LOGIN_USER_DATA.items() :
        d = LOGIN_USER_DATA.copy()
        d[k] = ""
        INCORRECT_LOGIN_USER_DATA.append(d)


    ALLOWED_ERRORS = ["Invalid username or no such user exists", "Invalid authority", "Incorrect Password"]

    # POST : Login
    # @unittest.skip
    def test_login(self):
        r = requests.post(self.LOGIN_API_URL, json=self.LOGIN_USER_DATA).json()
        self.assertEqual(r.get("status"), 200)
        self.assertEqual(r.get("message"), "Logged in successfully")

    # POST : Login With Error
    def test_login_with_errors(self):
        for data in self.INCORRECT_LOGIN_USER_DATA :
            r = requests.post(self.LOGIN_API_URL, json=data).json()
            check = r.get("error_message") in self.ALLOWED_ERRORS
            self.assertEqual(check, True)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("UserApiTestLogger").setLevel(logging.DEBUG)
    unittest.main()