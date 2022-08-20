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
        db.session.query(Token).filter(Token.user_id == user_id)
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
