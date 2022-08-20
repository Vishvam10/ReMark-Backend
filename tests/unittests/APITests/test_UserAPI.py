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
    "username": "admin1234",
    "email_id": "admin1234@gmail.com" ,
    "password": "Test1234!",
    "bio": "Hello World !",
    "authority": "admin",
}

TESTING_USER_ID = ""
TESTING_USER = {}
TESTING_API_KEY = ""

def test_0_init(client, auth) :
    global TESTING_USER_ID
    global HEADERS
    user = db.session.query(User).filter(User.username == ADMIN_DATA["username"]).first()
    if(user is not None) :
        user_id = user.__dict__["user_id"]
        db.session.query(User).filter(User.username == ADMIN_DATA["username"]).delete()
        db.session.commit()
    res = json.loads(client.post(USER_API_URL, json=ADMIN_DATA).data)
    TESTING_USER_ID = res.get("data").get("user_id")
    API_KEY = db.session.query(Token).filter(Token.user_id == TESTING_USER_ID).first().__dict__["api_key"]

    login_data = {
        "username" : ADMIN_DATA["username"],
        "password" : ADMIN_DATA["password"],
        "authority" : ADMIN_DATA["authority"]
    }

    TESTING_ACCESS_TOKEN = auth.login(login_data).get("access_token")
    
    HEADERS = {
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {}".format(TESTING_ACCESS_TOKEN),
        "API_KEY" : API_KEY
    }

@pytest.mark.skip()
def test_1a_create_new_user(client) :   
    res = json.loads(client.post(USER_API_URL, json=USER_DATA).data)
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "New user created"

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
    assert res is not None
    assert res.get("user_id") is not None

def test_4a_update_user(client, auth) :
    global TESTING_USER
    url = "{}/{}".format(USER_API_URL, TESTING_USER_ID)
    
    NEW_USER_DATA = {
        "username" : "EDITtest1234",
        "email_id" : "EDIT1234@gmail.com",
        "bio" : "Changed Blah"
    }

    res = json.loads(client.put(url, json=NEW_USER_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("username") == NEW_USER_DATA["username"]
    assert res.get("email_id") == NEW_USER_DATA["email_id"]
    assert res.get("bio") == NEW_USER_DATA["bio"]

def test_5_delete_user(client, auth) :
    global TESTING_API_KEY
    url = "{}/{}".format(USER_API_URL, TESTING_USER_ID)
    res = json.loads(client.delete(url, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 200
    check = res.get("message") == "Admin deleted successfully" or res.get("message") == "User deleted successfully"
    assert check == True

def test_6_cleanup() :
    db.session.query(User).delete()
    db.session.query(Token).delete()
    db.session.commit()
