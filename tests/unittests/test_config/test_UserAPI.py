import pytest
import json
from faker import Faker
fake = Faker()


first_name = fake.first_name()
last_name = fake.last_name()
email = f"{first_name}.{last_name}@{fake.domain_name()}"

BASE_API_URL = "/api"
USER_API_URL = "{}/user".format(BASE_API_URL)
LOGIN_API_URL = "{}/login".format(BASE_API_URL)

USER_DATA = {
    "email_id": email,
    "username": first_name,
    "password": last_name + "1234!",
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

LOGIN_USER_DATA = {
    "username": USER_DATA["username"],
    "password": USER_DATA["password"],
    "authority": USER_DATA["authority"]
}

INCORRECT_USER_DATA = []

ALLOWED_ERRORS = ["Email ID is required", "Password is required",
                    "Username is required", "Authority is incorrectly specified", "Duplicate user"]
HEADER_MISSING_ERROR = "Request header 'API_KEY' missing"

for k, v in USER_DATA.items():
    d = USER_DATA.copy()
    d[k] = ""
    INCORRECT_USER_DATA.append(d)

TESTING_USER_ID = ""

# @pytest.mark.skip()
def test_1_create_new_user(client) :   
    global TESTING_USER_ID 
    res = json.loads(client.post(USER_API_URL, json=USER_DATA).data)
    TESTING_USER_ID = res.get("data").get("user_id")
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "New user created"

@pytest.mark.skip()
def test_2_create_duplicate_user(client) :
    res = json.loads(client.post(USER_API_URL, json=USER_DATA).data)
    assert res is not None
    assert res.status == 400
    assert res.error_message == "Duplicate user"


def test_3_get_user(client) :
    global TESTING_USER_ID
    url = "{}/{}".format(USER_API_URL, TESTING_USER_ID)
    print("URL : ", url)
    res = client.get(url, json=USER_DATA)
    print("RESPONSE : ", res)
    # assert res is not None
    # assert res.status == 400
    # assert res.error_message == "Duplicate user"