import sys
import unittest
import logging
import requests

from faker import Faker

fake = Faker()
# Faker.seed(4981308123)
fixed_name = fake.unique.first_name()

class TokenApiTest(unittest.TestCase):
        
    BASE_API_URL = "http://127.0.0.1:5000/api"
    TOKEN_API_URL = "{}/token".format(BASE_API_URL)
    
    HEADER_MISSING_ERROR = "Request header 'API_KEY' missing"
    
    # POST : Create User
    @unittest.skip
    def test_create_token(self):
        r = requests.post(self.USER_API_URL, json=self.USER_DATA).json()
        self.assertEqual(r.get("status"), 201)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("UserApiTestLogger").setLevel(logging.DEBUG)
    unittest.main()