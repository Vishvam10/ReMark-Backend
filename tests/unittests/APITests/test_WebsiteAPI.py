import json

from application.database.database import db
from application.models.User import User
from application.models.Token import Token
from application.models.Website import Website

BASE_API_URL = "/api"
USER_API_URL = "{}/user".format(BASE_API_URL)
WEBSITE_API_URL = "{}/website".format(BASE_API_URL)

ADMIN_DATA = {
    "username": "test_admin",
    "email_id": "test_admin@gmail.com",
    "password": "Test1234!",
    "bio": "Hello World !",
    "authority": "admin",
}

WEBSITE_DATA = {
    "website_url" : "127.0.0.1:5500/",
    "admin_id" : "",
    "admin_type" : "BASIC"
}

HEADERS = None

TESTING_ADMIN_ID = ""
TESTING_WEBSITE_ID = ""

def test_0_init_admin(client, auth) :
    global TESTING_ADMIN_ID
    global WEBSITE_DATA
    global HEADERS
    user = db.session.query(User).filter(User.username == ADMIN_DATA["username"]).first()
    if(user is not None) :
        user_id = user.__dict__["user_id"]
        db.session.query(User).filter(User.username == ADMIN_DATA["username"]).delete()
        db.session.commit()
    res = json.loads(client.post(USER_API_URL, json=ADMIN_DATA).data)
    TESTING_ADMIN_ID = res.get("data").get("user_id")
    WEBSITE_DATA["admin_id"] = TESTING_ADMIN_ID
    API_KEY = db.session.query(Token).filter(Token.user_id == TESTING_ADMIN_ID).first().__dict__["api_key"]

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

def test_1a_create_new_website(client) :   
    global WEBSITE_DATA
    global TESTING_WEBSITE_ID
    res = json.loads(client.post(WEBSITE_API_URL, json=WEBSITE_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 200
    assert res.get("message") == "New website created"

    TESTING_WEBSITE_ID = res.get("data").get("website_id")

def test_2a_get_website_by_website_id(client) :
    global WEBSITE_DATA
    global TESTING_WEBSITE_ID
    url = "{}?website_id={}".format(WEBSITE_API_URL, TESTING_WEBSITE_ID)
    res = json.loads(client.get(url, headers=HEADERS).data)
    assert res is not None
    assert res.get("website_url") != -1

    TESTING_WEBSITE_ID = res.get("website_id")

def test_2b_get_website_by_website_url(client) :
    global WEBSITE_DATA
    url = "{}?website_url={}".format(WEBSITE_API_URL, WEBSITE_DATA["website_url"])
    res = json.loads(client.get(url, headers=HEADERS).data)
    assert res is not None
    assert res.get("website_url") == WEBSITE_DATA["website_url"]

def test_2c_get_website_by_user_id(client) :
    global WEBSITE_DATA
    global TESTING_WEBSITE_ID
    url = "{}/all/{}".format(WEBSITE_API_URL, TESTING_ADMIN_ID)
    res = json.loads(client.get(url, headers=HEADERS).data)
    print("TEST 2c RESPONSE : ", res, type(res))
    
    assert res is not None
    assert type(res) == list

def test_3_delete_website(client) :
    global WEBSITE_DATA
    global TESTING_WEBSITE_ID
    url = "{}/{}".format(WEBSITE_API_URL, TESTING_WEBSITE_ID)
    res = json.loads(client.delete(url, headers=HEADERS).data)
    print("TEST 3 RESPONSE : ", res, type(res))
    
    assert res is not None
    assert res.get("status") == 200
    assert res.get("message") == "Website deleted successfully"

def test_4_cleanup() :
    db.session.query(Website).delete()
    db.session.query(User).filter(User.user_id == TESTING_ADMIN_ID).delete()
    db.session.query(Token).filter(Token.user_id == TESTING_ADMIN_ID).delete()
    db.session.commit()