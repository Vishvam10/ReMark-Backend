import json
import pytest

from application.database.database import db
from application.models.User import User
from application.models.Token import Token

BASE_API_URL = "/api"
USER_API_URL = "{}/user".format(BASE_API_URL)
TOKEN_API_URL = "{}/token".format(BASE_API_URL)

TEST_DATA = {
    "username": "test",
    "email_id": "asdf@asdf.gmail.com",
    "password": "Test1234!",
    "bio": "Hello World !",
    "authority": "user",
}

TESTING_USER_ID = ""

def test_1_create_token(client) :   
    global TESTING_USER_ID
    # Create dummy user - not an admin since tokens 
    # are automatically created for them
    TESTING_USER_ID = json.loads(client.post(USER_API_URL, json=TEST_DATA).data).get("data").get("user_id")
    
    url = "{}/{}".format(TOKEN_API_URL, TESTING_USER_ID)
    
    res = json.loads(client.post(url).data)
    
    assert res is not None
    assert res.get("status") == 201
    assert res.get("message") == "New Token Created"

def test_2_get_token(client) :
    
    url = "{}/{}".format(TOKEN_API_URL, TESTING_USER_ID)
    
    res = json.loads(client.get(url).data)
    
    assert res is not None
    assert res.get("status") == 200
    assert res.get("data").get("api_key") is not None

def test_3_delete_token(client) :
    
    url = "{}/{}".format(TOKEN_API_URL, TESTING_USER_ID)
    
    res = json.loads(client.delete(url).data)
    
    assert res is not None
    assert res.get("status") == 200
    assert res.get("message") == "Token deleted successfully"

# NOT USED IN THE APP. IT IS JUST PRESENT 
# FOR THE SAKE OF API COMPLETTION
@pytest.mark.skip
def test_4_update_token() :
    return

# CLEANUP

def test_5_cleanup() :
    db.session.query(User).filter(User.user_id == TESTING_USER_ID).delete()
    db.session.query(Token).delete()
    db.session.commit()

