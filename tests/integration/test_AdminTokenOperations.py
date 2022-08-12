import sys
import unittest
import logging
import requests

import random

class AdminTokenOperations(unittest.TestCase):
    

    BASE_API_URL = "http://127.0.0.1:5000/api"
    LOGIN_API_URL = "{}/login".format(BASE_API_URL)
    USER_API_URL = "{}/user".format(BASE_API_URL)
    TOKEN_API_URL = "{}/token".format(BASE_API_URL)

    ADMIN_DATA = {
        "email_id": "testing_email_{}".format(random.randint(0, 100000)),
        "username": "testing_user_{}".format(random.randint(0, 100000)),
        "password": "testing123",
        "bio": "Hello World !",
        "authority": "admin",
    }
    
    LOGIN_USER_DATA = {
        "username" : ADMIN_DATA["username"],
        "password" : ADMIN_DATA["password"],
        "authority" : ADMIN_DATA["authority"]
    }

    TESTING_ADMIN_ID = ""
    TESTING_ADMIN_API_KEY = ""
    TESTING_ADMIN_ACCESS_TOKEN = ""

    INCORRECT_USER_ID = "asf0iqnefm0qiemfqwe"

    ALLOWED_ERRORS = ["Invalid User ID", "Token already exists", "Token does not exist"]

    HEADER_MISSING_ERROR = "Request header 'API_KEY' missing"

    # POST : Create New Token ( Happens Automatically When An Admin Is Created )
    
    def test_1_create_token_with_admin(self):        

        r1 = requests.post(self.USER_API_URL, json=self.ADMIN_DATA).json()
        
        self.assertEqual(r1.get("status"), 201)
        self.__class__.TESTING_ADMIN_ID = r1.get("data").get("user_id")

        r2 = requests.post("{}/{}".format(self.TOKEN_API_URL, self.TESTING_ADMIN_ID)).json()

        self.assertEqual(r2.get("status"), 400)

    # GET : Get Token Using user_id

    def test_2_get_token_with_admin(self) :
        url = "{}/{}".format(self.TOKEN_API_URL, self.__class__.TESTING_ADMIN_ID)
        r = requests.get(url).json()  
        self.assertEqual(r.get("status"), 200)
        
        logger = logging.getLogger("TokenApiTestLogger")
        logger.debug(url)
        logger.debug(self.__class__.TESTING_ADMIN_ID)
        self.__class__.TESTING_ADMIN_API_KEY = r.get("data").get("api_key")
        
    # GET : Get Token Using user_id With Error

    def test_3_get_token_with_error(self) :
        r = requests.get("{}/{}".format(self.TOKEN_API_URL, self.INCORRECT_USER_ID)).json()
        
        self.assertEqual(r.get("status"), 400)
        
        check = r.get("error_message") in self.ALLOWED_ERRORS
        self.assertEqual(check, True)
  
    # DELETE : Delete Token Using user_id

    def test_4_delete_token_with_admin(self) :

        # Login
        r2 = requests.post(self.LOGIN_API_URL, json=self.LOGIN_USER_DATA).json()
        logger = logging.getLogger("TokenApiTestLogger")
        logger.debug(r2.get("status"))
        logger.debug(self.TESTING_ADMIN_ID)
        self.__class__.TESTING_ADMIN_ACCESS_TOKEN = r2.get("access_token")
        self.assertEqual(r2.get("status"), 200)
        self.assertEqual(r2.get("message"), "Logged in successfully")

        # Delete the admin

        url = "{}/{}".format(self.USER_API_URL, self.__class__.TESTING_ADMIN_ID)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.TESTING_ADMIN_ACCESS_TOKEN),
            "API_KEY" : "{}".format(self.__class__.TESTING_ADMIN_API_KEY)
        }

        r2 = requests.delete(url=url, headers=headers).json()
        self.assertEqual(r2.get("status"), 200)
        self.assertEqual(r2.get("message"), "Admin deleted successfully")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("AdminTokenOperations").setLevel(logging.DEBUG)
    unittest.main()