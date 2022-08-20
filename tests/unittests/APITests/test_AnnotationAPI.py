import json

from application.database.database import db
from application.models.User import User
from application.models.Token import Token
from application.models.Website import Website
from application.models.Annotation import Annotation

BASE_API_URL = "/api"
USER_API_URL = "{}/user".format(BASE_API_URL)
WEBSITE_API_URL = "{}/website".format(BASE_API_URL)
ANNOTATION_API_URL = "{}/annotation".format(BASE_API_URL)

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

ANNOTATION_DATA = {
    "website_id" : "",
    "website_uri" : "127.0.0.1:5000/",
    "annotation_name" : "Sample Title",
    "node_xpath" : "//html/body/div[0]",
    "html_id" : "sampleTest",
    "html_tag" : "div",
    "html_text_content" : "Sample",
    "user_id" : "",
    "user_name" : "test_admin",
    "tags" : "test1,test2,test3"
}

HEADERS = None

TESTING_ADMIN_ID = ""
TESTING_WEBSITE_ID = ""
TESTING_ANNOTATION_ID = ""

def test_0_init(client, auth) :
    global TESTING_ADMIN_ID
    global TESTING_WEBSITE_ID
    global ANNOTATION_DATA
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
    TESTING_WEBSITE_ID = json.loads(client.post(WEBSITE_API_URL, json=WEBSITE_DATA, headers=HEADERS).data).get("data").get("website_id")
    ANNOTATION_DATA["user_id"] = TESTING_ADMIN_ID
    ANNOTATION_DATA["website_id"] = TESTING_WEBSITE_ID
    
def test_1_create_annotation(client) :
    global ANNOTATION_DATA
    global TESTING_ANNOTATION_ID
    res = json.loads(client.post(ANNOTATION_API_URL, json=ANNOTATION_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "New Annotation Created"

    TESTING_ANNOTATION_ID = res.get("data").get("annotation_id")

def test_2a_get_annotation_by_annotation_id(client) :
    url = "{}/{}".format(ANNOTATION_API_URL, TESTING_ANNOTATION_ID)
    res = json.loads(client.get(url, headers=HEADERS).data)
    assert res is not None
    assert res.get("annotation_id") == TESTING_ANNOTATION_ID

def test_2b_get_annotation_by_website_id(client) :
    global TESTING_WEBSITE_ID
    url = "{}/all/{}".format(ANNOTATION_API_URL, TESTING_WEBSITE_ID)
    res = json.loads(client.get(url, headers=HEADERS).data)
    assert res is not None
    assert type(res) == list

def test_3a_edit_annotation_name(client) :
    global ANNOTATION_DATA
    url = "{}/{}".format(ANNOTATION_API_URL, TESTING_ANNOTATION_ID)
    NEW_ANNOTATION_DATA = {
		"action_type" : "edit_name",
		"new_name" : "Edited Title",
		"new_tags" : "",
		"new_resolved" : ""
    }
    res = json.loads(client.put(url, json=NEW_ANNOTATION_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "Annotation edited successfully !"

def test_3b_edit_annotation_tags(client) :
    global ANNOTATION_DATA
    url = "{}/{}".format(ANNOTATION_API_URL, TESTING_ANNOTATION_ID)
    NEW_ANNOTATION_DATA = {
		"action_type" : "edit_tags",
		"new_name" : "",
		"new_tags" : "edit1,edit2",
		"new_resolved" : ""
    }
    res = json.loads(client.put(url, json=NEW_ANNOTATION_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "Annotation edited successfully !"

def test_3c_edit_annotation_resolve(client) :
    global ANNOTATION_DATA
    url = "{}/{}".format(ANNOTATION_API_URL, TESTING_ANNOTATION_ID)
    NEW_ANNOTATION_DATA = {
		"action_type" : "edit_resolved",
		"new_name" : "",
		"new_tags" : "",
		"new_resolved" : True
    }
    res = json.loads(client.put(url, json=NEW_ANNOTATION_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 201

def test_3d_edit_annotation_resolve(client) :
    global ANNOTATION_DATA
    url = "{}/{}".format(ANNOTATION_API_URL, TESTING_ANNOTATION_ID)
    NEW_ANNOTATION_DATA = {
		"action_type" : "edit_resolved",
		"new_name" : "",
		"new_tags" : "",
		"new_resolved" : True
    }
    res = json.loads(client.put(url, json=NEW_ANNOTATION_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 201

def test_4_cleanup() :
    global TESTING_ADMIN_ID
    db.session.query(Annotation).delete()
    db.session.query(Website).filter(Website.website_id == TESTING_WEBSITE_ID).delete()
    db.session.query(Token).filter(Token.user_id == TESTING_ADMIN_ID)
    db.session.query(User).filter(User.user_id == TESTING_ADMIN_ID)
    db.session.commit()