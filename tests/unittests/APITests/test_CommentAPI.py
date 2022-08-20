import json

from application.database.database import db
from application.models.User import User
from application.models.Token import Token
from application.models.Website import Website
from application.models.Annotation import Annotation
from application.models.Comment import Comment

BASE_API_URL = "/api"
USER_API_URL = "{}/user".format(BASE_API_URL)
WEBSITE_API_URL = "{}/website".format(BASE_API_URL)
ANNOTATION_API_URL = "{}/annotation".format(BASE_API_URL)
COMMENT_API_URL = "{}/comment".format(BASE_API_URL)

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

COMMENT_DATA = {
    "annotation_id" : "",
    "content" : "Sample text here.",
    "content_html" : "<p>Sample text here.</p>",
    "parent_node" : None,
    "user_id" : "",
    "user_name" : "test_admin"
}

HEADERS = None

TESTING_ADMIN_ID = ""
TESTING_WEBSITE_ID = ""
TESTING_ANNOTATION_ID = ""
TESTING_COMMENT_ID = ""

def test_0_init(client, auth) :
    global TESTING_ADMIN_ID
    global TESTING_WEBSITE_ID
    global TESTING_ANNOTATION_ID
    global WEBSITE_DATA
    global ANNOTATION_DATA
    global COMMENT_DATA
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
    
    COMMENT_DATA["user_id"] = TESTING_ADMIN_ID

    TESTING_ANNOTATION_ID = json.loads(client.post(ANNOTATION_API_URL, json=ANNOTATION_DATA, headers=HEADERS).data).get("data").get("annotation_id")

    COMMENT_DATA["annotation_id"] = TESTING_ANNOTATION_ID

def test_1_create_comment(client) :
    global COMMENT_DATA
    global TESTING_COMMENT_ID
    res = json.loads(client.post(COMMENT_API_URL, json=COMMENT_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "New Comment Created"

    TESTING_COMMENT_ID = res.get("data").get("comment_id")

def test_2_get_comment(client) :
    global COMMENT_DATA
    url = "{}/{}".format(COMMENT_API_URL, TESTING_COMMENT_ID)
    res = json.loads(client.get(url, headers=HEADERS).data)    
    assert res is not None

def test_3_edit_comment(client) :
    global COMMENT_DATA
    global TESTING_COMMENT_ID
    url = "{}/{}".format(COMMENT_API_URL, TESTING_COMMENT_ID)
    NEW_COMMENT_DATA = {
		"user_id" : TESTING_ADMIN_ID,
		"comment_id" : TESTING_COMMENT_ID,
		"new_content" : "The comment is EDITED !",
		"new_content_html" : "<p>The comment is EDITED !</p>"
    }
    res = json.loads(client.put(url, json=NEW_COMMENT_DATA, headers=HEADERS).data)
    assert res is not None
    assert res.get("comment_id") == TESTING_COMMENT_ID
    assert res.get("content") == NEW_COMMENT_DATA["new_content"]

def test_4_delete_comment(client) :
    global COMMENT_DATA
    global TESTING_COMMENT_ID
    url = "{}/{}".format(COMMENT_API_URL, TESTING_COMMENT_ID)
    res = json.loads(client.delete(url, headers=HEADERS).data)
    assert res is not None
    assert res.get("comment_id") == TESTING_COMMENT_ID
    assert res.get("status") == 200
    assert res.get("message") == "Comment deleted successfully"

def test_5_cleanup() :
    global TESTING_ADMIN_ID
    db.session.query(Comment).delete()
    db.session.query(Annotation).filter(Annotation.annotation_id == TESTING_ANNOTATION_ID).delete()
    db.session.query(Website).filter(Website.website_id == TESTING_WEBSITE_ID).delete()
    db.session.query(Token).filter(Token.user_id == TESTING_ADMIN_ID)
    db.session.query(User).filter(User.user_id == TESTING_ADMIN_ID)
    db.session.commit()
