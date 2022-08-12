from random import random
import sys
import unittest
import logging
import requests

from faker import Faker

fake = Faker()
# Faker.seed(4981308123)

class UserApiTest(unittest.TestCase):

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name}.{last_name}@{fake.domain_name()}"
        
    BASE_API_URL = "http://127.0.0.1:5000/api"
    USER_API_URL = "{}/user".format(BASE_API_URL)

    GET_ALL_USERS_API_URL = "{}/all".format(USER_API_URL)

    USER_DATA = {
        "email_id": email,
        "username": "testing_user",
        "password": "testing123",
        "bio": "Hello World !",
        "authority": "user",
    }

    ADMIN_DATA = {
        "email_id": "testing_email@gmail.com",
        "username": "testing_admin",
        "password": "testing123",
        "bio": "Hello World !",
        "authority": "admin",
    }

    INCORRECT_USER_DATA = []

    ALLOWED_ERRORS = ["Email ID is required", "Password is required", "Username is required", "Authority is incorrectly specified", "Duplicate user"]
    HEADER_MISSING_ERROR = "Request header 'API_KEY' missing"

    for k, v in USER_DATA.items() :
        d = USER_DATA.copy()
        d[k] = ""
        INCORRECT_USER_DATA.append(d)


    
    # POST : Create User
    @unittest.skip
    def test_create_user(self):
        r = requests.post(self.USER_API_URL, json=self.USER_DATA).json()
        self.assertEqual(r.get("status"), 201)

    # POST : Create Admin
    @unittest.skip
    def test_create_admin(self):
        r = requests.post(self.USER_API_URL, json=self.ADMIN_DATA).json()
        self.assertEqual(r.get("status"), 201)

    # POST : Create User With Error
    @unittest.skip
    def test_create_user_with_error(self):
        for data in self.INCORRECT_USER_DATA :
            r = requests.post(self.USER_API_URL, json=data).json()
            check = r.get("error_message") in self.ALLOWED_ERRORS
            self.assertEqual(check, True)
    

    # GET : (FOR DEBUG ONLY) Get All Users 
    @unittest.skip
    def test_get_all_user(self) :
        r = requests.get(self.GET_ALL_USERS_API_URL).json()
        logger = logging.getLogger("UserApiTestLogger")
        logger.debug(r.get("error_message"))
    
    # GET : Get All Users Without API_KEY Header
    @unittest.skip
    def test_get_all_user_2b(self) :
        r = requests.get(self.GET_ALL_USERS_API_URL).json()
        self.assertEqual(r.get("error_message"), self.HEADER_MISSING_ERROR)

    # 


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("UserApiTestLogger").setLevel(logging.DEBUG)
    unittest.main()