import pytest
import json

from application.database.database import db
from application.models.User import User
from application.models.Token import Token

from faker import Faker
fake = Faker()

first_name = fake.first_name()
last_name = fake.last_name()
email = f"{first_name}.{last_name}@{fake.domain_name()}"

BASE_API_URL = "/api"
USER_API_URL = "{}/user".format(BASE_API_URL)

USER_DATA = {
    "username": first_name,
    "email_id": email,
    "password": last_name + "1234!",
    "bio": "Hello World !",
    "authority": "user",
}

ADMIN_DATA = {
    "username": "admin" + last_name,
    "email_id": "admin" + email,
    "password": last_name + "1234!",
    "bio": "Hello World !",
    "authority": "admin",
}

INCORRECT_USER_DATA = []

TESTING_USER_ID = ""
TESTING_USER = {}
TESTING_API_KEY = ""

def create_dummy_user(client) :
    STATIC_USER_DATA = {
        "username": "test_user",
        "email_id": "testing1234@gmail.com",
        "password": "Test1234!",
        "bio": "Hello World !",
        "authority": "user",
    }
    res = client.post("/api/user", json=STATIC_USER_DATA)
    return STATIC_USER_DATA

def test_0_db_cleanup(app) :
    with app.app_context() :
        db.session.query(User).delete()
        db.session.query(Token).delete()
        db.session.commit()

def test_1a_create_new_user(client) :   
    res = json.loads(client.post(USER_API_URL, json=USER_DATA).data)
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "New user created"

def test_1b_create_new_admin(client) :
    global TESTING_USER_ID
    USER_DATA["authority"] = "admin"
    res = json.loads(client.post(USER_API_URL, json=ADMIN_DATA).data)
    TESTING_USER_ID = res.get("data").get("user_id")
    print("TEST 1b RESPONSE : ", TESTING_USER_ID)
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "New admin created"

@pytest.mark.skip()
def test_2_create_duplicate_user(client) :
    res = json.loads(client.post(USER_API_URL, json=USER_DATA).data)
    assert res is not None
    assert res.status == 400
    assert res.error_message == "Duplicate user"
def test_3a_get_user(client) :
    global TESTING_USER_ID
    global TESTING_USER
    url = "{}/{}".format(USER_API_URL, TESTING_USER_ID)
    res = json.loads(client.get(url, json=USER_DATA).data)
    TESTING_USER = res
    print("TEST 3a RESPONSE : ", res)
    assert res is not None
    assert res.get("user_id") is not None

def test_3b_get_admin_and_store_api_key(client) :
    global TESTING_API_KEY
    url = "api/token/{}".format(TESTING_USER_ID)
    res = json.loads(client.get(url).data)
    TESTING_API_KEY = res.get("data").get("api_key")

# def test_4a_update_user(client, auth) :
#     global TESTING_API_KEY
#     user_data = create_dummy_user(client)
#     data = {
#         "username": user_data["username"],
#         "password" : user_data["password"],
#         "authority" : user_data["authority"]
#     }
#     res = auth.login(data)
#     # login_data = {
#     #     "username" : STATIC_USER_DATA["username"],
#     #     "password" : STATIC_USER_DATA["password"],
#     #     "authority" : STATIC_USER_DATA["authority"]
#     # }
 
#     # access_token = auth.login(login_data)
#     # headers = {
#     #     "Content-Type" : "application/json",
#     #     "Authorization" : "Bearer {}".format(access_token),
#     #     "API_KEY" : TESTING_API_KEY,
#     # }
#     print("TEST 4b RESPONSE : ", data)
#     # url = "{}/{}".format(USER_API_URL, TESTING_USER_ID)
#     # print("TEST 4b RESPONSE : ", url, data, headers)
#     # assert res is not None
#     # assert res.get("msg") == "Missing Authorization Header"

# def test_5_delete_user(client, auth) :
#     global TESTING_API_KEY
#     user_data = create_dummy_user(client)
#     data = {
#         "username": user_data["username"],
#         "password" : user_data["password"],
#         "authority" : user_data["authority"]
#     }
#     res = auth.login(data)

#     print("TEST 5 RESPONSE : ", res)

def test_6_final_db_cleanup() :
    db.session.query(User).delete()
    db.session.query(Token).delete()
    db.session.commit()
